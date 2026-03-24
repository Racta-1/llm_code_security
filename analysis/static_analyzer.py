import json
import subprocess
from pathlib import Path
from typing import Any


# Map Bandit test IDs to CWE categories
BANDIT_TO_CWE = {
    "B608": "CWE-89",   # SQL injection
    "B601": "CWE-78",   # Shell injection (paramiko)
    "B602": "CWE-78",   # subprocess shell=True
    "B603": "CWE-78",   # subprocess without shell
    "B604": "CWE-78",   # Function call with shell=True
    "B605": "CWE-78",   # Start process with shell
    "B606": "CWE-78",   # Start process with no shell
    "B607": "CWE-78",   # Start process with partial path
    "B101": "CWE-703",  # Use of assert
    "B324": "CWE-327",  # weak hash
    "B303": "CWE-327",  # md5/sha1 in hashlib
    "B311": "CWE-338",  # insecure randomness
    "B105": "CWE-798",  # hardcoded password string
    "B106": "CWE-798",  # hardcoded password func arg
    "B107": "CWE-798",  # hardcoded password default
    "B301": "CWE-502",  # pickle usage
    "B302": "CWE-502",  # marshal
    "B506": "CWE-502",  # yaml.load
}

SEVERITY_WEIGHTS = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
}


class StaticAnalyzer:
    """
    Static security analysis using Bandit.

    Returns:
    - vuln_count
    - vuln_density
    - weighted_vuln_score
    - weighted_density
    - severity breakdown
    - CWE categories / breakdown
    - raw issue list
    """

    def analyze(self, file_path: str) -> dict[str, Any]:
        bandit_output = self._run_bandit(file_path)
        loc = self._count_loc(file_path)
        issues = self._parse_bandit(bandit_output)

        count = len(issues)
        density = (count / loc * 100) if loc > 0 else 0.0

        weighted_vuln_score = sum(
            SEVERITY_WEIGHTS.get(issue["severity"].upper(), 1)
            for issue in issues
        )
        weighted_density = (weighted_vuln_score / loc * 100) if loc > 0 else 0.0

        severity_breakdown = {
            "HIGH": sum(1 for i in issues if i["severity"].upper() == "HIGH"),
            "MEDIUM": sum(1 for i in issues if i["severity"].upper() == "MEDIUM"),
            "LOW": sum(1 for i in issues if i["severity"].upper() == "LOW"),
        }

        cwe_breakdown: dict[str, int] = {}
        for issue in issues:
            cwe = issue.get("cwe", "OTHER")
            cwe_breakdown[cwe] = cwe_breakdown.get(cwe, 0) + 1

        cwe_categories = sorted(
            [cwe for cwe in cwe_breakdown.keys() if cwe not in ("OTHER", "UNKNOWN")]
        )

        return {
            "file": file_path,
            "loc": loc,
            "count": count,
            "density": density,
            "weighted_vuln_score": weighted_vuln_score,
            "weighted_density": weighted_density,
            "severity_breakdown": severity_breakdown,
            "cwe_categories": cwe_categories,
            "cwe_breakdown": cwe_breakdown,
            "issues": issues,
        }

    def _run_bandit(self, file_path: str) -> dict[str, Any]:
        try:
            proc = subprocess.run(
                ["bandit", "-f", "json", "-q", file_path],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if proc.stdout.strip():
                return json.loads(proc.stdout)

            return {}
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            return {}

    def _parse_bandit(self, bandit_output: dict[str, Any]) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []

        for result in bandit_output.get("results", []):
            test_id = result.get("test_id", "")
            severity = str(result.get("issue_severity", "LOW")).upper()
            confidence = str(result.get("issue_confidence", "LOW")).upper()

            issues.append(
                {
                    "test_id": test_id,
                    "test_name": result.get("test_name", ""),
                    "severity": severity,
                    "confidence": confidence,
                    "line": result.get("line_number", 0),
                    "text": result.get("issue_text", ""),
                    "cwe": BANDIT_TO_CWE.get(test_id, "OTHER"),
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