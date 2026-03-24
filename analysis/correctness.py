"""
Functional correctness checker.

Writes generated code to a temp file, runs the task's pytest suite against it,
and returns pass rate (DV2 in the research design).
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


class CorrectnessChecker:
    def __init__(self, task: dict):
        self.task = task
        self.test_file = task.get("test_file")  # path to pytest file

    def check(self, code: str) -> dict:
        if not self.test_file or not Path(self.test_file).exists():
            return self._no_tests()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Write generated code as the module under test
            module_name = self.task.get("module_name", "solution")
            code_path = os.path.join(tmpdir, f"{module_name}.py")
            with open(code_path, "w") as f:
                f.write(code)

            # Copy test file in
            test_src = Path(self.test_file).read_text()
            test_path = os.path.join(tmpdir, "test_solution.py")
            with open(test_path, "w") as f:
                f.write(test_src)

            # Run pytest, capture JSON report
            report_path = os.path.join(tmpdir, "report.json")
            proc = subprocess.run(
                [
                    sys.executable, "-m", "pytest",
                    test_path,
                    "--json-report", f"--json-report-file={report_path}",
                    "-q", "--tb=no",
                ],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=tmpdir,
            )

            return self._parse_report(report_path, proc)

    def _parse_report(self, report_path: str, proc) -> dict:
        try:
            import json
            with open(report_path) as f:
                report = json.load(f)

            summary = report.get("summary", {})
            total = summary.get("total", 1)
            passed = summary.get("passed", 0)
            failed = summary.get("failed", 0)
            errors = summary.get("errors", 0)

            return {
                "pass_rate": passed / total if total > 0 else 0.0,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "total": total,
                "details": report.get("tests", []),
            }
        except Exception:
            # Fallback: parse stdout
            passed = proc.stdout.count(" passed")
            return {
                "pass_rate": 1.0 if "passed" in proc.stdout and "failed" not in proc.stdout else 0.0,
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "total": 0,
                "details": [],
                "raw_output": proc.stdout,
            }

    def _no_tests(self) -> dict:
        return {
            "pass_rate": None,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "total": 0,
            "details": [],
            "note": "No test file configured for this task.",
        }