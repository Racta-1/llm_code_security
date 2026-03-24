"""
Reporter: aggregates all run results into a summary JSON + markdown table.
"""

import json
from pathlib import Path
from datetime import datetime


class Reporter:
    def __init__(self, run_id: str, task_name: str):
        self.run_id = run_id
        self.task_name = task_name
        self.out_dir = Path("results") / "reports" / run_id
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, results: list[dict]):
        self._save_json(results)
        self._save_markdown(results)
        self._print_summary(results)

    def _save_json(self, results):
        path = self.out_dir / f"{self.task_name}_summary.json"
        path.write_text(json.dumps(results, indent=2))
        print(f"\n  📄 JSON summary: {path}")

    def _save_markdown(self, results):
        lines = [
            f"# Security Pipeline Results",
            f"**Task:** {self.task_name}  ",
            f"**Run ID:** {self.run_id}  ",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Results",
            "",
            "| Model | Mode | Vuln Density | Correctness |",
            "|-------|------|:------------:|:-----------:|",
        ]

        for r in results:
            corr = r["correctness_pass_rate"]
            corr_str = f"{corr:.1%}" if corr is not None else "N/A"
            lines.append(
                f"| {r['model']} | {r['mode']} | "
                f"{r['vuln_density']:.2f}/100 LOC | {corr_str} |"
            )

        lines += ["", "## Vulnerability Breakdown by Model", ""]
        for r in results:
            lines.append(f"### {r['model']} ({r['mode']})")
            if r["vuln_issues"]:
                for issue in r["vuln_issues"]:
                    lines.append(
                        f"- **[{issue['severity']}]** {issue['test_name']} "
                        f"(line {issue['line']}) — {issue['cwe']}"
                    )
            else:
                lines.append("- No issues detected ✅")
            lines.append("")

        path = self.out_dir / f"{self.task_name}_report.md"
        path.write_text("\n".join(lines))
        print(f"  📊 Markdown report: {path}")

    def _print_summary(self, results):
        print(f"\n{'─'*50}")
        print(f"  SUMMARY — {self.task_name}")
        print(f"{'─'*50}")
        print(f"  {'Model':<10} {'Mode':<15} {'Vuln/100LOC':>12} {'Correctness':>12}")
        print(f"  {'─'*47}")
        for r in results:
            corr = r["correctness_pass_rate"]
            corr_str = f"{corr:.1%}" if corr is not None else "N/A"
            print(
                f"  {r['model']:<10} {r['mode']:<15} "
                f"{r['vuln_density']:>11.2f} {corr_str:>12}"
            )
        print(f"{'─'*50}")