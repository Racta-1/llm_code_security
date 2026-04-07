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

    Keeps:
    - old detailed correctness/security breakdown
    Adds:
    - Pass Rate (%)
    - Security Score (%)
    - Overall Score (%)
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
            "| Model | Mode | Syntax | Func Success | Pass Rate | Security Score | Overall Score | Exec Tests | Skipped | Bandit | Semgrep | Combined Score |",
            "|-------|------|:------:|:------------:|:---------:|:--------------:|:-------------:|:----------:|:-------:|:------:|:-------:|:--------------:|",
        ]

        for r in results:
            syntax_str = "Yes" if r.get("syntax_valid") else "No"
            func_str = "Yes" if r.get("functional_success") else "No"

            pass_rate = r.get("pass_rate", 0.0)
            security_score = r.get("security_score", 0.0)
            overall_score = r.get("overall_score", 0.0)

            executed = r.get("executed_total", r.get("tests_executed_total", 0))
            skipped = r.get("skipped", r.get("tests_skipped", 0))

            bandit_count = r.get("bandit_count", r.get("bandit_vuln_count", 0))
            semgrep_count = r.get("semgrep_count", r.get("semgrep_vuln_count", 0))
            combined_score = r.get(
                "combined_weighted_score",
                r.get("bandit_weighted_score", r.get("bandit_weighted_vuln_score", 0))
                + r.get("semgrep_weighted_score", r.get("semgrep_weighted_vuln_score", 0))
            )

            lines.append(
                f"| {r['model']} | {r['mode']} | {syntax_str} | {func_str} | "
                f"{pass_rate:.1f}% | {security_score:.1f}% | {overall_score:.1f}% | "
                f"{executed} | {skipped} | {bandit_count} | {semgrep_count} | {combined_score} |"
            )

        lines += ["", "## Detailed Breakdown", ""]

        for r in results:
            syntax_str = "Yes" if r.get("syntax_valid") else "No"
            func_str = "Yes" if r.get("functional_success") else "No"
            secure_str = "Yes" if r.get("secure_success") else "No"

            pass_rate = r.get("pass_rate", 0.0)
            security_score = r.get("security_score", 0.0)
            overall_score = r.get("overall_score", 0.0)

            executed = r.get("executed_total", r.get("tests_executed_total", 0))
            skipped = r.get("skipped", r.get("tests_skipped", 0))
            passed = r.get("passed", r.get("tests_passed", 0))
            failed = r.get("failed", r.get("tests_failed", 0))
            errors = r.get("errors", r.get("tests_errors", 0))

            bandit_count = r.get("bandit_count", r.get("bandit_vuln_count", 0))
            bandit_density = r.get("bandit_density", r.get("bandit_vuln_density", 0.0))
            bandit_weighted = r.get("bandit_weighted_score", r.get("bandit_weighted_vuln_score", 0))
            bandit_weighted_density = r.get("bandit_weighted_density", r.get("bandit_weighted_vuln_density", 0.0))
            bandit_issues = r.get("bandit_issues", r.get("bandit_vuln_issues", []))
            bandit_cwe_categories = r.get("bandit_cwe_categories", [])
            bandit_cwe_breakdown = r.get("bandit_cwe_breakdown", {})
            severity_breakdown = r.get("severity_breakdown", {})

            semgrep_count = r.get("semgrep_count", r.get("semgrep_vuln_count", 0))
            semgrep_density = r.get("semgrep_density", r.get("semgrep_vuln_density", 0.0))
            semgrep_weighted = r.get("semgrep_weighted_score", r.get("semgrep_weighted_vuln_score", 0))
            semgrep_weighted_density = r.get("semgrep_weighted_density", r.get("semgrep_weighted_vuln_density", 0.0))
            semgrep_rule_ids = r.get("semgrep_rule_ids", [])
            semgrep_issues = r.get("semgrep_issues", r.get("semgrep_vuln_issues", []))
            semgrep_cwe_categories = r.get("semgrep_cwe_categories", [])
            semgrep_cwe_breakdown = r.get("semgrep_cwe_breakdown", {})

            combined_count = r.get("security_findings", bandit_count + semgrep_count)
            combined_score = r.get("combined_weighted_score", bandit_weighted + semgrep_weighted)

            lines.append(f"### {r['model']} ({r['mode']})")
            lines.append("")
            lines.append(f"- **Source file:** `{r.get('source_code_file', 'N/A')}`")
            lines.append(f"- **Snapshot file:** `{r.get('snapshot_file', 'N/A')}`")
            lines.append(f"- **Syntax valid:** {syntax_str}")

            if r.get("syntax_error"):
                lines.append(f"- **Syntax error:** `{r['syntax_error']}`")

            lines.append("")
            lines.append("#### Headline Scores")
            lines.append("")
            lines.append(f"- **Pass Rate:** {pass_rate:.1f}%")
            lines.append(f"- **Security Score:** {security_score:.1f}%")
            lines.append(f"- **Overall Score:** {overall_score:.1f}%")
            lines.append(f"- **Functional success:** {func_str}")
            lines.append(f"- **Secure success:** {secure_str}")
            lines.append("")

            lines.append("#### Correctness Breakdown")
            lines.append("")
            lines.append(f"- **Executed tests:** {executed}")
            lines.append(f"- **Skipped tests:** {skipped}")
            lines.append(f"- **Passed / Failed / Errors:** {passed} / {failed} / {errors}")
            lines.append(f"- **Correctness status:** {r.get('correctness_status', 'N/A')}")

            if r.get("correctness_note"):
                lines.append(f"- **Correctness note:** {r['correctness_note']}")

            lines.append("")
            lines.append("#### Security Breakdown")
            lines.append("")
            lines.append(f"- **Combined security findings:** {combined_count}")
            lines.append(f"- **Combined weighted security score:** {combined_score}")
            lines.append(f"- **LOC:** {r.get('loc', 0)}")
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
                f"- **Bandit CWE categories:** "
                f"{', '.join(bandit_cwe_categories) if bandit_cwe_categories else 'None'}"
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
                f"- **Semgrep rules triggered:** "
                f"{', '.join(semgrep_rule_ids) if semgrep_rule_ids else 'None'}"
            )
            lines.append(
                f"- **Semgrep CWE categories:** "
                f"{', '.join(semgrep_cwe_categories) if semgrep_cwe_categories else 'None'}"
            )

            if semgrep_cwe_breakdown:
                formatted = ", ".join(f"{k}={v}" for k, v in sorted(semgrep_cwe_breakdown.items()))
                lines.append(f"- **Semgrep CWE breakdown:** {formatted}")

            lines.append("")
            lines.append("#### Semgrep Findings")
            lines.append("")

            if semgrep_issues:
                for issue in semgrep_issues:
                    cwes = issue.get("cwe_categories", [])
                    cwe_text = f" — {', '.join(cwes)}" if cwes else ""
                    lines.append(
                        f"- **[{issue.get('severity', 'INFO')}]** "
                        f"{issue.get('rule_id', 'unknown')} "
                        f"(line {issue.get('line', 0)}): "
                        f"{issue.get('message', '')}{cwe_text}"
                    )
            else:
                lines.append("- No Semgrep issues detected ✅")

            lines.append("")

        path = self.out_dir / f"{self.task_name}_report.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  📊 Markdown report: {path}")

    def _print_summary(self, results: list[dict[str, Any]]):
        print(f"\n{'─' * 126}")
        print(f"  SUMMARY — {self.task_name}")
        print(f"{'─' * 126}")
        print(
            f"  {'Model':<10} {'Mode':<16} {'Syntax':<8} {'Func OK':<10} "
            f"{'Pass Rate':>10} {'Sec.Score':>11} {'Overall':>10} "
            f"{'Exec':>6} {'Bandit':>8} {'Semgrep':>9} {'Comb.Score':>12}"
        )
        print(f"  {'─' * 122}")

        for r in results:
            syntax_str = "Yes" if r.get("syntax_valid") else "No"
            func_str = "Yes" if r.get("functional_success") else "No"

            pass_rate = r.get("pass_rate", 0.0)
            security_score = r.get("security_score", 0.0)
            overall_score = r.get("overall_score", 0.0)

            executed = r.get("executed_total", r.get("tests_executed_total", 0))
            bandit_count = r.get("bandit_count", r.get("bandit_vuln_count", 0))
            semgrep_count = r.get("semgrep_count", r.get("semgrep_vuln_count", 0))
            combined_score = r.get(
                "combined_weighted_score",
                r.get("bandit_weighted_score", r.get("bandit_weighted_vuln_score", 0))
                + r.get("semgrep_weighted_score", r.get("semgrep_weighted_vuln_score", 0))
            )

            print(
                f"  {r['model']:<10} {r['mode']:<16} {syntax_str:<8} {func_str:<10} "
                f"{pass_rate:>9.1f}% {security_score:>10.1f}% {overall_score:>9.1f}% "
                f"{executed:>6} {bandit_count:>8} {semgrep_count:>9} {combined_score:>12}"
            )

        print(f"{'─' * 126}")