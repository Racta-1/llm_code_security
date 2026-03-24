import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


class CorrectnessChecker:
    """
    Functional correctness checker.

    For a given task, this class:
    1. Writes the candidate code into a temporary module (default: solution.py)
    2. Copies the task's pytest file into the temporary directory
    3. Runs pytest with JSON reporting enabled
    4. Returns structured correctness metrics

    Returned metrics include:
    - pass_rate
    - passed
    - failed
    - errors
    - total
    - functional_success
    - details
    """

    def __init__(self, task: dict[str, Any]):
        self.task = task
        self.test_file = task.get("test_file")
        self.module_name = task.get("module_name", "solution")

    def check(self, code: str) -> dict[str, Any]:
        test_path = Path(self.test_file) if self.test_file else None

        if not test_path or not test_path.exists():
            return self._no_tests()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            code_file = tmpdir_path / f"{self.module_name}.py"
            local_test_file = tmpdir_path / "test_solution.py"
            report_file = tmpdir_path / "report.json"

            code_file.write_text(code, encoding="utf-8")
            local_test_file.write_text(test_path.read_text(encoding="utf-8"), encoding="utf-8")

            try:
                proc = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pytest",
                        str(local_test_file),
                        "--json-report",
                        f"--json-report-file={report_file}",
                        "-q",
                        "--tb=no",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=tmpdir,
                )
            except subprocess.TimeoutExpired as exc:
                return {
                    "pass_rate": 0.0,
                    "passed": 0,
                    "failed": 0,
                    "errors": 1,
                    "total": 0,
                    "details": [],
                    "functional_success": 0,
                    "status": "timeout",
                    "note": "Pytest execution timed out.",
                    "raw_output": (exc.stdout or "") + "\n" + (exc.stderr or ""),
                }
            except Exception as exc:
                return {
                    "pass_rate": 0.0,
                    "passed": 0,
                    "failed": 0,
                    "errors": 1,
                    "total": 0,
                    "details": [],
                    "functional_success": 0,
                    "status": "runner_error",
                    "note": f"Failed to execute pytest: {exc}",
                    "raw_output": "",
                }

            return self._parse_report(report_file, proc)

    def _parse_report(self, report_file: Path, proc: subprocess.CompletedProcess) -> dict[str, Any]:
        if report_file.exists():
            try:
                report = json.loads(report_file.read_text(encoding="utf-8"))
                summary = report.get("summary", {})

                passed = int(summary.get("passed", 0))
                failed = int(summary.get("failed", 0))
                errors = int(summary.get("errors", 0))
                total = int(summary.get("total", passed + failed + errors))

                pass_rate = passed / total if total > 0 else 0.0
                functional_success = 1 if total > 0 and passed == total else 0

                return {
                    "pass_rate": pass_rate,
                    "passed": passed,
                    "failed": failed,
                    "errors": errors,
                    "total": total,
                    "details": report.get("tests", []),
                    "functional_success": functional_success,
                    "status": "ok" if functional_success else "failed_tests",
                    "raw_output": proc.stdout.strip(),
                    "raw_error": proc.stderr.strip(),
                }
            except Exception as exc:
                return self._fallback_parse(proc, note=f"Failed to parse pytest JSON report: {exc}")

        return self._fallback_parse(proc, note="Pytest JSON report was not created.")

    def _fallback_parse(self, proc: subprocess.CompletedProcess, note: str) -> dict[str, Any]:
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""

        passed = self._extract_count(stdout, "passed")
        failed = self._extract_count(stdout, "failed")
        errors = self._extract_count(stdout, "error") + self._extract_count(stdout, "errors")

        total = passed + failed + errors
        pass_rate = passed / total if total > 0 else 0.0
        functional_success = 1 if total > 0 and passed == total and failed == 0 and errors == 0 else 0

        return {
            "pass_rate": pass_rate,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "total": total,
            "details": [],
            "functional_success": functional_success,
            "status": "fallback_parsed",
            "note": note,
            "raw_output": stdout.strip(),
            "raw_error": stderr.strip(),
        }

    @staticmethod
    def _extract_count(text: str, keyword: str) -> int:
        """
        Tries to extract counts from pytest output lines like:
        '3 passed in 0.02s'
        '1 failed, 2 passed in 0.05s'
        """
        import re

        matches = re.findall(rf"(\d+)\s+{keyword}\b", text)
        return sum(int(m) for m in matches) if matches else 0

    def _no_tests(self) -> dict[str, Any]:
        return {
            "pass_rate": None,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "total": 0,
            "details": [],
            "functional_success": 0,
            "status": "no_tests",
            "note": "No test file configured for this task.",
        }