"""
LLM Security Pipeline
Assessing Security of LLM-Generated Code in Programming Tasks

Usage:
    python pipeline.py --task tasks/task_fileio_01/task.json --mode both
    python pipeline.py --task tasks/task_fileio_01/task.json --mode baseline
    python pipeline.py --task tasks/task_fileio_01/task.json --mode security_aware
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from analysis.static_analyzer import StaticAnalyzer
from analysis.correctness import CorrectnessChecker
from analysis.reporter import Reporter
from analysis.syntax_checker import SyntaxChecker


MODELS = ["gpt", "claude", "gemini"]
PROMPT_MODES = ["baseline", "security_aware"]


def load_task(task_path: str) -> dict:
    with open(task_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_pipeline(task_path: str, modes: list[str], models: list[str]):
    task = load_task(task_path)
    task_name = task["name"]
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n{'=' * 60}")
    print("  LLM Security Pipeline")
    print(f"  Task: {task_name} | Run: {run_id}")
    print(f"  Models: {models} | Modes: {modes}")
    print(f"{'=' * 60}\n")

    all_results = []

    for mode in modes:
        prompt_file = Path("prompts") / mode / f"{task_name}.txt"
        if prompt_file.exists():
            print(f"[INFO] Found prompt: {prompt_file}")
        else:
            print(f"[WARN] Prompt not found: {prompt_file}")

        for model_name in models:
            print(f"\n[{mode.upper()}] Evaluating {model_name}...")

            code_file = Path(task["code_dir"]) / mode / f"{model_name}_code.py"
            if not code_file.exists():
                print(f"[WARN] Code file not found: {code_file} — skipping")
                continue

            code = code_file.read_text(encoding="utf-8")

            # Save a copy into outputs for traceability
            out_dir = Path("outputs") / model_name / mode / run_id
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{task_name}.py"
            out_file.write_text(code, encoding="utf-8")
            print(f"  ✓ Code loaded from: {code_file}")
            print(f"  ✓ Snapshot saved to: {out_file}")

            # 1. Syntax check
            syntax_checker = SyntaxChecker()
            syntax_result = syntax_checker.check(code)

            if syntax_result["syntax_valid"]:
                print("  ✓ Syntax: valid")
            else:
                print(f"  ✗ Syntax error: {syntax_result['syntax_error']}")

            # 2. Functional correctness
            checker = CorrectnessChecker(task)
            if syntax_result["syntax_valid"]:
                correctness = checker.check(code)
                pass_rate = correctness["pass_rate"] if correctness["pass_rate"] is not None else 0.0
                print(
                    f"  ✓ Correctness: {pass_rate:.1%} tests passing "
                    f"({correctness['passed']}/{correctness['total']})"
                )
                print(
                    f"  ✓ Functional success: "
                    f"{'Yes' if correctness['functional_success'] else 'No'}"
                )
            else:
                correctness = {
                    "pass_rate": 0.0,
                    "passed": 0,
                    "failed": 0,
                    "errors": 0,
                    "total": 0,
                    "details": [],
                    "functional_success": 0,
                    "status": "skipped_invalid_syntax",
                    "note": "Skipped because syntax is invalid.",
                }

            # 3. Static security analysis
            analyzer = StaticAnalyzer()
            vuln_report = analyzer.analyze(str(out_file))

            weighted_vuln_score = vuln_report.get("weighted_vuln_score", 0)
            cwe_categories = vuln_report.get("cwe_categories", [])

            print(f"  ✓ Vuln density: {vuln_report['density']:.2f} issues/100 LOC")
            print(f"  ✓ Vulnerability count: {vuln_report['count']}")
            print(f"  ✓ Weighted vuln score: {weighted_vuln_score}")
            print(
                f"  ✓ CWE categories: {', '.join(cwe_categories) if cwe_categories else 'None'}"
            )

            # 4. Combined success metric
            secure_success = 1 if (
                correctness["functional_success"] == 1 and
                vuln_report["count"] == 0
            ) else 0

            print(f"  ✓ Secure success: {'Yes' if secure_success else 'No'}")

            # 5. Aggregate result
            result = {
                "run_id": run_id,
                "task": task_name,
                "model": model_name,
                "mode": mode,
                "timestamp": datetime.now().isoformat(),
                "source_code_file": str(code_file),
                "snapshot_file": str(out_file),

                "syntax_valid": syntax_result["syntax_valid"],
                "syntax_error": syntax_result["syntax_error"],

                "tests_passed": correctness["passed"],
                "tests_failed": correctness["failed"],
                "tests_errors": correctness["errors"],
                "tests_total": correctness["total"],
                "correctness_pass_rate": correctness["pass_rate"],
                "correctness_details": correctness["details"],
                "functional_success": correctness["functional_success"],
                "correctness_status": correctness.get("status"),
                "correctness_note": correctness.get("note"),

                "vuln_density": vuln_report["density"],
                "vuln_count": vuln_report["count"],
                "weighted_vuln_score": weighted_vuln_score,
                "cwe_categories": cwe_categories,
                "vuln_issues": vuln_report["issues"],
                "loc": vuln_report["loc"],

                "secure_success": secure_success,
            }
            all_results.append(result)

            # Save per-sample JSON
            result_dir = Path("results") / "per_sample" / run_id
            result_dir.mkdir(parents=True, exist_ok=True)
            result_file = result_dir / f"{model_name}_{mode}_{task_name}.json"
            result_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

    # 6. Generate summary report
    reporter = Reporter(run_id, task_name)
    reporter.generate(all_results)

    print(f"\n{'=' * 60}")
    print("  Pipeline complete. Results in results/")
    print(f"  Run ID: {run_id}")
    print(f"{'=' * 60}\n")


def main():
    parser = argparse.ArgumentParser(description="LLM Security Pipeline")
    parser.add_argument("--task", required=True, help="Path to task JSON")
    parser.add_argument(
        "--mode",
        choices=["baseline", "security_aware", "both"],
        default="both",
        help="Prompt strategy mode",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        choices=MODELS,
        default=MODELS,
        help="Which models to analyze",
    )
    args = parser.parse_args()

    modes = PROMPT_MODES if args.mode == "both" else [args.mode]
    run_pipeline(args.task, modes, args.models)


if __name__ == "__main__":
    main()