"""
LLM Security Pipeline
Assessing Security of LLM-Generated Code in Programming Tasks

Usage:
    python pipeline.py --task tasks/task_input_01/task.json --mode both
    python pipeline.py --task tasks/task_input_01/task.json --mode baseline
    python pipeline.py --task tasks/task_input_01/task.json --mode security_aware
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from analysis.correctness import CorrectnessChecker
from analysis.reporter import Reporter
from analysis.static_analyzer import StaticAnalyzer
from analysis.syntax_checker import SyntaxChecker
from analysis.semgrep_analyzer import SemgrepAnalyzer


MODELS = ["gpt", "claude", "gemini"]
PROMPT_MODES = ["baseline", "security_aware"]


def load_task(task_path: str) -> dict:
    with open(task_path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_skipped_correctness_result() -> dict:
    return {
        "functional_success": 0,
        "evaluation_valid": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "executed_total": 0,
        "skipped": 0,
        "status": "skipped_invalid_syntax",
        "note": "Skipped because syntax is invalid.",
        "raw_output": "",
        "raw_error": "",
    }


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
            else:
                correctness = make_skipped_correctness_result()

            passed = correctness.get("passed", 0)
            failed = correctness.get("failed", 0)
            errors = correctness.get("errors", 0)
            executed_total = correctness.get("executed_total", 0)
            skipped = correctness.get("skipped", 0)
            evaluation_valid = correctness.get("evaluation_valid", 0)
            functional_success = correctness.get("functional_success", 0)

            pass_rate = 0.0
            if executed_total > 0:
                pass_rate = 100.0 * passed / executed_total

            print(
                f"  ✓ Pass rate: {pass_rate:.1f}% "
                f"({passed}/{executed_total} executed, {skipped} skipped)"
            )
            print(f"  ✓ Functional success: {'Yes' if functional_success else 'No'}")

            # 3. Bandit analysis
            bandit_analyzer = StaticAnalyzer()
            bandit_report = bandit_analyzer.analyze(str(out_file))

            bandit_count = bandit_report.get("count", 0)
            bandit_density = bandit_report.get("density", 0.0)
            bandit_weighted = bandit_report.get("weighted_vuln_score", 0)
            bandit_weighted_density = bandit_report.get("weighted_density", 0.0)
            severity_breakdown = bandit_report.get("severity_breakdown", {})
            bandit_cwe_categories = bandit_report.get("cwe_categories", [])
            bandit_cwe_breakdown = bandit_report.get("cwe_breakdown", {})
            bandit_issues = bandit_report.get("issues", [])
            loc = bandit_report.get("loc", 0)

            print(f"  ✓ Bandit findings: {bandit_count}")
            print(f"  ✓ Bandit density: {bandit_density:.2f} issues/100 LOC")
            print(f"  ✓ Bandit weighted score: {bandit_weighted}")
            print(
                f"  ✓ Bandit CWE categories: "
                f"{', '.join(bandit_cwe_categories) if bandit_cwe_categories else 'None'}"
            )

            # 4. Semgrep analysis
            semgrep_analyzer = SemgrepAnalyzer()
            semgrep_report = semgrep_analyzer.analyze(str(out_file))

            semgrep_count = semgrep_report.get("count", 0)
            semgrep_density = semgrep_report.get("density", 0.0)
            semgrep_weighted = semgrep_report.get("weighted_vuln_score", 0)
            semgrep_weighted_density = semgrep_report.get("weighted_density", 0.0)
            semgrep_rule_ids = semgrep_report.get("rule_ids", [])
            semgrep_issues = semgrep_report.get("issues", [])
            semgrep_cwe_categories = semgrep_report.get("cwe_categories", [])
            semgrep_cwe_breakdown = semgrep_report.get("cwe_breakdown", {})

            print(f"  ✓ Semgrep findings: {semgrep_count}")
            print(f"  ✓ Semgrep density: {semgrep_density:.2f} issues/100 LOC")
            print(f"  ✓ Semgrep weighted score: {semgrep_weighted}")
            print(
                f"  ✓ Semgrep rules: "
                f"{', '.join(semgrep_rule_ids) if semgrep_rule_ids else 'None'}"
            )

            # 5. Combined metrics
            combined_vuln_count = bandit_count + semgrep_count
            combined_weighted_score = bandit_weighted + semgrep_weighted
            secure_success = 1 if combined_vuln_count == 0 else 0

            print(f"  ✓ Combined security findings: {combined_vuln_count}")
            print(f"  ✓ Combined weighted score: {combined_weighted_score}")
            print(f"  ✓ Secure success: {'Yes' if secure_success else 'No'}")

            # 6. Aggregate result
            result = {
                "run_id": run_id,
                "task": task_name,
                "model": model_name,
                "mode": mode,
                "timestamp": datetime.now().isoformat(),
                "source_code_file": str(code_file),
                "snapshot_file": str(out_file),

                # new headline metrics
                "pass_rate": round(pass_rate, 1),
                "functional_success": functional_success,
                "security_findings": combined_vuln_count,

                # legacy / detailed fields
                "syntax_valid": syntax_result["syntax_valid"],
                "syntax_error": syntax_result["syntax_error"],
                "loc": loc,
                "evaluation_valid": evaluation_valid,

                "passed": passed,
                "failed": failed,
                "errors": errors,
                "executed_total": executed_total,
                "skipped": skipped,
                "correctness_status": correctness.get("status"),
                "correctness_note": correctness.get("note"),

                # compatibility aliases for older report sections
                "tests_passed": passed,
                "tests_failed": failed,
                "tests_errors": errors,
                "tests_skipped": skipped,
                "tests_executed_total": executed_total,

                # Bandit-specific fields
                "bandit_count": bandit_count,
                "bandit_density": bandit_density,
                "bandit_weighted_score": bandit_weighted,
                "bandit_weighted_density": bandit_weighted_density,
                "severity_breakdown": severity_breakdown,
                "bandit_cwe_categories": bandit_cwe_categories,
                "bandit_cwe_breakdown": bandit_cwe_breakdown,
                "bandit_issues": bandit_issues,

                # Semgrep-specific fields
                "semgrep_count": semgrep_count,
                "semgrep_density": semgrep_density,
                "semgrep_weighted_score": semgrep_weighted,
                "semgrep_weighted_density": semgrep_weighted_density,
                "semgrep_rule_ids": semgrep_rule_ids,
                "semgrep_cwe_categories": semgrep_cwe_categories,
                "semgrep_cwe_breakdown": semgrep_cwe_breakdown,
                "semgrep_issues": semgrep_issues,

                # combined fields for detailed breakdown
                "combined_security_findings": combined_vuln_count,
                "combined_weighted_score": combined_weighted_score,
                "secure_success": secure_success,
            }
            all_results.append(result)

            result_dir = Path("results") / "per_sample" / run_id
            result_dir.mkdir(parents=True, exist_ok=True)
            result_file = result_dir / f"{model_name}_{mode}_{task_name}.json"
            result_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

    # 7. Normalize security score within this task using max observed findings
    max_findings_for_task = max((r["security_findings"] for r in all_results), default=0)
    if max_findings_for_task == 0:
        max_findings_for_task = 1

    for r in all_results:
        security_score = 100.0 * (1.0 - (r["security_findings"] / max_findings_for_task))
        overall_score = (r["pass_rate"] + security_score) / 2.0

        r["security_score"] = round(max(0.0, security_score), 1)
        r["overall_score"] = round(max(0.0, overall_score), 1)

    # rewrite per-sample files with normalized scores included
    result_dir = Path("results") / "per_sample" / run_id
    for r in all_results:
        result_file = result_dir / f"{r['model']}_{r['mode']}_{task_name}.json"
        result_file.write_text(json.dumps(r, indent=2), encoding="utf-8")

    # 8. Print normalized metrics
    print(f"\n{'=' * 60}")
    print(f"  Final normalized scores for {task_name}")
    print(f"{'=' * 60}")
    for r in all_results:
        print(
            f"  {r['model']:<10} {r['mode']:<16} "
            f"Pass Rate: {r['pass_rate']:>5.1f}%   "
            f"Security Findings: {r['security_findings']:>2}   "
            f"Security Score: {r['security_score']:>5.1f}%   "
            f"Overall Score: {r['overall_score']:>5.1f}%"
        )

    # 9. Generate summary report
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