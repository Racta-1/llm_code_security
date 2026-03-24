"""
Static security analysis using Bandit (and optionally Semgrep).

Outputs vuln density = issues per 100 LOC, with severity breakdown.
CWE categories tracked (per research design):
  - CWE-89  SQL Injection
  - CWE-78  OS Injection
  - CWE-22  Path Traversal
  - CWE-327 Weak Crypto
  - CWE-798 Hard-coded Credentials
  - CWE-502 Unsafe Deserialization
"""

import json
import subprocess
import tempfile
from pathlib import Path


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
    "B324": "CWE-327",  # Use of weak MD5/SHA1
    "B303": "CWE-327",  # Use of MD5 in hashlib
    "B311": "CWE-338",  # Standard pseudo-random generators
    "B105": "CWE-798",  # Hardcoded password string
    "B106": "CWE-798",  # Hardcoded password func arg
    "B107": "CWE-798",  # Hardcoded password default
    "B301": "CWE-502",  # Pickle usage
    "B302": "CWE-502",  # marshal.loads
    "B506": "CWE-502",  # yaml.load
    "B301": "CWE-502",  # Pickle
}

SEVERITY_WEIGHTS = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}


class StaticAnalyzer:
    def analyze(self, file_path: str) -> dict:
        """Run Bandit on a Python file, return structured vuln report."""
        result = self._run_bandit(file_path)
        loc = self._count_loc(file_path)
        issues = self._parse_bandit(result)

        count = len(issues)
        density = (count / loc * 100) if loc > 0 else 0.0
        weighted = sum(SEVERITY_WEIGHTS.get(i["severity"], 1) for i in issues)
        weighted_density = (weighted / loc * 100) if loc > 0 else 0.0

        # Group by CWE
        cwe_breakdown = {}
        for issue in issues:
            cwe = issue.get("cwe", "UNKNOWN")
            cwe_breakdown.setdefault(cwe, []).append(issue)

        return {
            "file": file_path,
            "loc": loc,
            "count": count,
            "density": density,
            "weighted_density": weighted_density,
            "severity_breakdown": {
                "HIGH": sum(1 for i in issues if i["severity"] == "HIGH"),
                "MEDIUM": sum(1 for i in issues if i["severity"] == "MEDIUM"),
                "LOW": sum(1 for i in issues if i["severity"] == "LOW"),
            },
            "cwe_breakdown": {k: len(v) for k, v in cwe_breakdown.items()},
            "issues": issues,
        }

    def _run_bandit(self, file_path: str) -> dict:
        try:
            proc = subprocess.run(
                ["bandit", "-f", "json", "-q", file_path],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return json.loads(proc.stdout) if proc.stdout.strip() else {}
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            return {}

    def _parse_bandit(self, bandit_output: dict) -> list[dict]:
        issues = []
        for r in bandit_output.get("results", []):
            test_id = r.get("test_id", "")
            issues.append(
                {
                    "test_id": test_id,
                    "test_name": r.get("test_name", ""),
                    "severity": r.get("issue_severity", "LOW"),
                    "confidence": r.get("issue_confidence", "LOW"),
                    "line": r.get("line_number", 0),
                    "text": r.get("issue_text", ""),
                    "cwe": BANDIT_TO_CWE.get(test_id, "OTHER"),
                }
            )
        return issues

    def _count_loc(self, file_path: str) -> int:
        try:
            lines = Path(file_path).read_text().splitlines()
            return sum(
                1 for l in lines
                if l.strip() and not l.strip().startswith("#")
            )
        except Exception:
            return 1