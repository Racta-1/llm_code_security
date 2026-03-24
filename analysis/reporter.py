import json
from datetime import datetime
from pathlib import Path
from typing import Any


class Reporter:
    """
    Aggregates run results into:
    - summary JSON
    - markdown report
    - terminal summary
    """

    def __init__(self, run_id: str, task_name: str):
        self.run_id = run_id
        self.task_name = task_name
        self.out_dir = Path("results") / "reports" / run_id
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, results: list[dict[str, Any]]):
        self._save_json(results)
        self._save_markdown(results)
        self._print_summary(results)

    def _save_json(self, results: list[dict[str, Any]]):
        path = self.out_dir / f"{self.task_name}_summary.json"
        path.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"\n  📄 JSON summary: {path}")

    def _save_markdown(self, results: list[dict[str, Any]]):
        lines = [
            "# Security Pipeline Results",
            f"**Task:** {self.task_name}  ",
            f"**Run ID:** {self.run_id}  ",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Results",
            "",
            "| Model | Mode | Syntax | Func Success | Test Pass | Findings | Weighted Score | Secure Success |",
            "|-------|------|:------:|:------------:|:---------:|:--------:|:--------------:|:--------------:|",
        ]

        for r in results:
            syntax_str = "Yes" if r.get("syntax_valid") else "No"
            func_str = "Yes" if r.get("functional_success") else "No"
            secure_str = "Yes" if r.get("secure_success") else "No"

            pass_rate = r.get("correctness_pass_rate")
            pass_rate_str = f"{pass_rate:.1%}" if pass_rate is not None else "N/A"

            lines.append(
                f"| {r['model']} | {r['mode']} | {syntax_str} | {func_str} | "
                f"{pass_rate_str} | {r.get('vuln_count', 0)} | "
                f"{r.get('weighted_vuln_score', 0)} | {secure_str} |"
            )

        lines += [
            "",
            "## Detailed Breakdown",
            "",
        ]

        for r in results:
            lines.append(f"### {r['model']} ({r['mode']})")
            lines.append("")
            lines.append(f"- **Source file:** `{r.get('source_code_file', 'N/A')}`")
            lines.append(f"- **Snapshot file:** `{r.get('snapshot_file', 'N/A')}`")
            lines.append(f"- **Syntax valid:** {'Yes' if r.get('syntax_valid') else 'No'}")

            if r.get("syntax_error"):
                lines.append(f"- **Syntax error:** `{r['syntax_error']}`")

            lines.append(
                f"- **Tests passed:** {r.get('tests_passed', 0)}/{r.get('tests_total', 0)}"
            )
            lines.append(
                f"- **Functional success:** {'Yes' if r.get('functional_success') else 'No'}"
            )
            lines.append(f"- **Vulnerability count:** {r.get('vuln_count', 0)}")
            lines.append(
                f"- **Vulnerability density:** {r.get('vuln_density', 0.0):.2f}/100 LOC"
            )
            lines.append(
                f"- **Weighted vulnerability score:** {r.get('weighted_vuln_score', 0)}"
            )

            cwe_categories = r.get("cwe_categories", [])
            lines.append(
                f"- **CWE categories:** {', '.join(cwe_categories) if cwe_categories else 'None'}"
            )

            lines.append(
                f"- **Secure success:** {'Yes' if r.get('secure_success') else 'No'}"
            )
            lines.append("")

            vuln_issues = r.get("vuln_issues", [])
            if vuln_issues:
                lines.append("#### Vulnerability Findings")
                lines.append("")
                for issue in vuln_issues:
                    lines.append(
                        f"- **[{issue.get('severity', 'LOW')}]** "
                        f"{issue.get('test_name', 'Unknown test')} "
                        f"(line {issue.get('line', 0)}) — "
                        f"{issue.get('cwe', 'OTHER')}: "
                        f"{issue.get('text', '')}"
                    )
                lines.append("")
            else:
                lines.append("#### Vulnerability Findings")
                lines.append("")
                lines.append("- No issues detected ✅")
                lines.append("")

        path = self.out_dir / f"{self.task_name}_report.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  📊 Markdown report: {path}")

    def _print_summary(self, results: list[dict[str, Any]]):
        print(f"\n{'─' * 90}")
        print(f"  SUMMARY — {self.task_name}")
        print(f"{'─' * 90}")
        print(
            f"  {'Model':<10} {'Mode':<16} {'Syntax':<8} {'Func OK':<10} "
            f"{'Pass Rate':>10} {'Findings':>10} {'Wt.Score':>10} {'Secure':>10}"
        )
        print(f"  {'─' * 86}")

        for r in results:
            syntax_str = "Yes" if r.get("syntax_valid") else "No"
            func_str = "Yes" if r.get("functional_success") else "No"
            secure_str = "Yes" if r.get("secure_success") else "No"

            pass_rate = r.get("correctness_pass_rate")
            pass_rate_str = f"{pass_rate:.1%}" if pass_rate is not None else "N/A"

            print(
                f"  {r['model']:<10} {r['mode']:<16} {syntax_str:<8} {func_str:<10} "
                f"{pass_rate_str:>10} {r.get('vuln_count', 0):>10} "
                f"{r.get('weighted_vuln_score', 0):>10} {secure_str:>10}"
            )

        print(f"{'─' * 90}")