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

    Supports:
    - correctness metrics
    - Bandit findings
    - Semgrep findings
    - combined security metrics
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
            "| Model | Mode | Syntax | Func Success | Test Pass | Exec Tests | Skipped | Bandit | Semgrep | Combined Score | Secure Success |",
            "|-------|------|:------:|:------------:|:---------:|:----------:|:-------:|:------:|:-------:|:--------------:|:--------------:|",
        ]

        for r in results:
            syntax_str = "Yes" if r.get("syntax_valid") else "No"
            func_str = "Yes" if r.get("functional_success") else "No"
            secure_str = "Yes" if r.get("secure_success") else "No"

            pass_rate = r.get("correctness_pass_rate")
            pass_rate_str = f"{pass_rate:.1%}" if pass_rate is not None else "N/A"

            executed = r.get("tests_executed_total", 0)
            skipped = r.get("tests_skipped", 0)

            bandit_count = r.get("bandit_vuln_count", r.get("vuln_count", 0))
            semgrep_count = r.get("semgrep_vuln_count", 0)
            combined_score = (
                r.get("bandit_weighted_vuln_score", r.get("weighted_vuln_score", 0))
                + r.get("semgrep_weighted_vuln_score", 0)
            )

            lines.append(
                f"| {r['model']} | {r['mode']} | {syntax_str} | {func_str} | "
                f"{pass_rate_str} | {executed} | {skipped} | "
                f"{bandit_count} | {semgrep_count} | {combined_score} | {secure_str} |"
            )

        lines += ["", "## Detailed Breakdown", ""]

        for r in results:
            syntax_str = "Yes" if r.get("syntax_valid") else "No"
            func_str = "Yes" if r.get("functional_success") else "No"
            secure_str = "Yes" if r.get("secure_success") else "No"

            pass_rate = r.get("correctness_pass_rate")
            pass_rate_str = f"{pass_rate:.1%}" if pass_rate is not None else "N/A"

            executed = r.get("tests_executed_total", 0)
            skipped = r.get("tests_skipped", 0)
            passed = r.get("tests_passed", 0)
            failed = r.get("tests_failed", 0)
            errors = r.get("tests_errors", 0)

            bandit_count = r.get("bandit_vuln_count", r.get("vuln_count", 0))
            bandit_density = r.get("bandit_vuln_density", r.get("vuln_density", 0.0))
            bandit_weighted = r.get("bandit_weighted_vuln_score", r.get("weighted_vuln_score", 0))
            bandit_weighted_density = r.get("bandit_weighted_density", r.get("weighted_density", 0.0))
            bandit_issues = r.get("bandit_vuln_issues", r.get("vuln_issues", []))
            bandit_cwe_categories = r.get("bandit_cwe_categories", r.get("cwe_categories", []))
            bandit_cwe_breakdown = r.get("bandit_cwe_breakdown", r.get("cwe_breakdown", {}))
            severity_breakdown = r.get("severity_breakdown", {})

            semgrep_count = r.get("semgrep_vuln_count", 0)
            semgrep_density = r.get("semgrep_vuln_density", 0.0)
            semgrep_weighted = r.get("semgrep_weighted_vuln_score", 0)
            semgrep_weighted_density = r.get("semgrep_weighted_density", 0.0)
            semgrep_rule_ids = r.get("semgrep_rule_ids", [])
            semgrep_issues = r.get("semgrep_vuln_issues", [])

            combined_count = bandit_count + semgrep_count
            combined_score = bandit_weighted + semgrep_weighted

            lines.append(f"### {r['model']} ({r['mode']})")
            lines.append("")
            lines.append(f"- **Source file:** `{r.get('source_code_file', 'N/A')}`")
            lines.append(f"- **Snapshot file:** `{r.get('snapshot_file', 'N/A')}`")
            lines.append(f"- **Syntax valid:** {syntax_str}")

            if r.get("syntax_error"):
                lines.append(f"- **Syntax error:** `{r['syntax_error']}`")

            lines.append(f"- **Test pass rate:** {pass_rate_str}")
            lines.append(f"- **Executed tests:** {executed}")
            lines.append(f"- **Passed / Failed / Errors:** {passed} / {failed} / {errors}")
            lines.append(f"- **Skipped tests:** {skipped}")
            lines.append(f"- **Functional success:** {func_str}")
            lines.append(f"- **Correctness status:** {r.get('correctness_status', 'N/A')}")

            if r.get("correctness_note"):
                lines.append(f"- **Correctness note:** {r['correctness_note']}")

            lines.append(f"- **LOC:** {r.get('loc', 0)}")
            lines.append(f"- **Combined security findings:** {combined_count}")
            lines.append(f"- **Combined weighted security score:** {combined_score}")
            lines.append(f"- **Secure success:** {secure_str}")
            lines.append("")

            lines.append("#### Bandit Summary")
            lines.append("")
            lines.append(f"- **Bandit findings:** {bandit_count}")
            lines.append(f"- **Bandit density:** {bandit_density:.2f}/100 LOC")
            lines.append(f"- **Bandit weighted score:** {bandit_weighted}")
            lines.append(f"- **Bandit weighted density:** {bandit_weighted_density:.2f}/100 LOC")

            if severity_breakdown:
                lines.append(
                    "- **Severity breakdown:** "
                    f"HIGH={severity_breakdown.get('HIGH', 0)}, "
                    f"MEDIUM={severity_breakdown.get('MEDIUM', 0)}, "
                    f"LOW={severity_breakdown.get('LOW', 0)}"
                )

            lines.append(
                f"- **Bandit CWE categories:** {', '.join(bandit_cwe_categories) if bandit_cwe_categories else 'None'}"
            )

            if bandit_cwe_breakdown:
                formatted = ", ".join(f"{k}={v}" for k, v in sorted(bandit_cwe_breakdown.items()))
                lines.append(f"- **Bandit CWE breakdown:** {formatted}")

            lines.append("")
            lines.append("#### Bandit Findings")
            lines.append("")

            if bandit_issues:
                for issue in bandit_issues:
                    lines.append(
                        f"- **[{issue.get('severity', 'LOW')}]** "
                        f"{issue.get('test_name', 'Unknown test')} "
                        f"(line {issue.get('line', 0)}) — "
                        f"{issue.get('cwe', 'OTHER')}: "
                        f"{issue.get('text', '')}"
                    )
            else:
                lines.append("- No Bandit issues detected ✅")

            lines.append("")
            lines.append("#### Semgrep Summary")
            lines.append("")
            lines.append(f"- **Semgrep findings:** {semgrep_count}")
            lines.append(f"- **Semgrep density:** {semgrep_density:.2f}/100 LOC")
            lines.append(f"- **Semgrep weighted score:** {semgrep_weighted}")
            lines.append(f"- **Semgrep weighted density:** {semgrep_weighted_density:.2f}/100 LOC")
            lines.append(
                f"- **Semgrep rules triggered:** {', '.join(semgrep_rule_ids) if semgrep_rule_ids else 'None'}"
            )

            lines.append("")
            lines.append("#### Semgrep Findings")
            lines.append("")

            if semgrep_issues:
                for issue in semgrep_issues:
                    lines.append(
                        f"- **[{issue.get('severity', 'INFO')}]** "
                        f"{issue.get('rule_id', 'unknown')} "
                        f"(line {issue.get('line', 0)}): "
                        f"{issue.get('message', '')}"
                    )
            else:
                lines.append("- No Semgrep issues detected ✅")

            lines.append("")

        path = self.out_dir / f"{self.task_name}_report.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  📊 Markdown report: {path}")

    def _print_summary(self, results: list[dict[str, Any]]):
        print(f"\n{'─' * 122}")
        print(f"  SUMMARY — {self.task_name}")
        print(f"{'─' * 122}")
        print(
            f"  {'Model':<10} {'Mode':<16} {'Syntax':<8} {'Func OK':<10} "
            f"{'Pass Rate':>10} {'Exec':>6} {'Skip':>6} {'Bandit':>8} {'Semgrep':>9} {'Comb.Score':>12} {'Secure':>10}"
        )
        print(f"  {'─' * 118}")

        for r in results:
            syntax_str = "Yes" if r.get("syntax_valid") else "No"
            func_str = "Yes" if r.get("functional_success") else "No"
            secure_str = "Yes" if r.get("secure_success") else "No"

            pass_rate = r.get("correctness_pass_rate")
            pass_rate_str = f"{pass_rate:.1%}" if pass_rate is not None else "N/A"

            bandit_count = r.get("bandit_vuln_count", r.get("vuln_count", 0))
            semgrep_count = r.get("semgrep_vuln_count", 0)
            combined_score = (
                r.get("bandit_weighted_vuln_score", r.get("weighted_vuln_score", 0))
                + r.get("semgrep_weighted_vuln_score", 0)
            )

            print(
                f"  {r['model']:<10} {r['mode']:<16} {syntax_str:<8} {func_str:<10} "
                f"{pass_rate_str:>10} {r.get('tests_executed_total', 0):>6} "
                f"{r.get('tests_skipped', 0):>6} {bandit_count:>8} "
                f"{semgrep_count:>9} {combined_score:>12} {secure_str:>10}"
            )

        print(f"{'─' * 122}")