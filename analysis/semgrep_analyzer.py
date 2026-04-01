import json
import subprocess
from pathlib import Path
from typing import Any


SEVERITY_WEIGHTS = {
    "ERROR": 3,
    "WARNING": 2,
    "INFO": 1,
}


class SemgrepAnalyzer:
    """
    Static security analysis using Semgrep.
    Supports local custom rules and extracts CWE metadata from rule definitions.
    """

    def __init__(self, rules_path: str = "rules/semgrep/inputparsing_rules.yml"):
        self.rules_path = rules_path

    def analyze(self, file_path: str) -> dict[str, Any]:
        semgrep_output = self._run_semgrep(file_path)
        issues = self._parse_semgrep(semgrep_output)
        loc = self._count_loc(file_path)

        count = len(issues)
        density = (count / loc * 100) if loc > 0 else 0.0
        weighted_score = sum(SEVERITY_WEIGHTS.get(i["severity"], 1) for i in issues)
        weighted_density = (weighted_score / loc * 100) if loc > 0 else 0.0
        rule_ids = sorted({issue["rule_id"] for issue in issues})

        cwe_categories = sorted({
            cwe
            for issue in issues
            for cwe in issue.get("cwe_categories", [])
        })

        cwe_breakdown: dict[str, int] = {}
        for issue in issues:
            for cwe in issue.get("cwe_categories", []):
                cwe_breakdown[cwe] = cwe_breakdown.get(cwe, 0) + 1

        return {
            "file": file_path,
            "loc": loc,
            "count": count,
            "density": density,
            "weighted_vuln_score": weighted_score,
            "weighted_density": weighted_density,
            "rule_ids": rule_ids,
            "cwe_categories": cwe_categories,
            "cwe_breakdown": cwe_breakdown,
            "issues": issues,
        }

    def _run_semgrep(self, file_path: str) -> dict[str, Any]:
        try:
            proc = subprocess.run(
                [
                    "semgrep",
                    "--config",
                    self.rules_path,
                    "--json",
                    file_path,
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if proc.stdout.strip():
                return json.loads(proc.stdout)
            return {}

        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            return {}

    def _parse_semgrep(self, semgrep_output: dict[str, Any]) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []

        for result in semgrep_output.get("results", []):
            extra = result.get("extra", {}) or {}
            metadata = extra.get("metadata", {}) or {}
            severity = str(extra.get("severity", "INFO")).upper()

            raw_cwe = metadata.get("cwe", [])
            if isinstance(raw_cwe, str):
                raw_cwe = [raw_cwe]

            cwe_categories = []
            for item in raw_cwe:
                if isinstance(item, str):
                    # "CWE-20: Improper Input Validation" -> "CWE-20"
                    cwe_id = item.split(":")[0].strip()
                    cwe_categories.append(cwe_id)

            issues.append(
                {
                    "rule_id": result.get("check_id", "unknown"),
                    "severity": severity,
                    "message": extra.get("message", ""),
                    "line": result.get("start", {}).get("line", 0),
                    "path": result.get("path", ""),
                    "metadata": metadata,
                    "cwe_categories": sorted(set(cwe_categories)),
                }
            )

        return issues

    def _count_loc(self, file_path: str) -> int:
        try:
            lines = Path(file_path).read_text(encoding="utf-8").splitlines()
            loc = sum(
                1 for line in lines
                if line.strip() and not line.strip().startswith("#")
            )
            return max(loc, 1)
        except Exception:
            return 1