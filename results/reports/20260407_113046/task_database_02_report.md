# Security Pipeline Results
**Task:** task_database_02  
**Run ID:** 20260407_113046  
**Generated:** 2026-04-07 11:30

## Results

| Model | Mode | Syntax | Func Success | Test Pass | Exec Tests | Skipped | Bandit | Semgrep | Combined Score | Secure Success |
|-------|------|:------:|:------------:|:---------:|:----------:|:-------:|:------:|:-------:|:--------------:|:--------------:|
| gpt | baseline | Yes | No | N/A | 0 | 0 | 0 | 2 | 5 | No |- **Semgrep CWE categories:** None
| claude | baseline | Yes | No | N/A | 0 | 0 | 0 | 2 | 5 | No |- **Semgrep CWE categories:** None
| gemini | baseline | Yes | No | N/A | 0 | 0 | 0 | 1 | 2 | No |- **Semgrep CWE categories:** None
| gpt | security_aware | Yes | No | N/A | 0 | 0 | 0 | 1 | 2 | No |- **Semgrep CWE categories:** None
| claude | security_aware | Yes | No | N/A | 0 | 0 | 0 | 1 | 2 | No |- **Semgrep CWE categories:** None
| gemini | security_aware | Yes | No | N/A | 0 | 0 | 0 | 2 | 5 | No |- **Semgrep CWE categories:** None

## Detailed Breakdown

### gpt (baseline)

- **Source file:** `tasks/task_database_02/code/baseline/gpt_code.py`
- **Snapshot file:** `outputs/gpt/baseline/20260407_113046/task_database_02.py`
- **Syntax valid:** Yes
- **Test pass rate:** N/A
- **Executed tests:** 0
- **Passed / Failed / Errors:** 0 / 0 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** no_tests
- **Correctness note:** No test file configured for this task.
- **LOC:** 42
- **Combined security findings:** 2
- **Combined weighted security score:** 5
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 0
- **Bandit density:** 0.00/100 LOC
- **Bandit weighted score:** 0
- **Bandit weighted density:** 0.00/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=0, LOW=0
- **Bandit CWE categories:** None

#### Bandit Findings

- No Bandit issues detected ✅

#### Semgrep Summary

- **Semgrep findings:** 2
- **Semgrep density:** 4.76/100 LOC
- **Semgrep weighted score:** 5
- **Semgrep weighted density:** 11.90/100 LOC
- **Semgrep rules triggered:** rules.semgrep.delete-user-no-authorisation-check, rules.semgrep.delete-user-no-input-validation

#### Semgrep Findings

- **[ERROR]** rules.semgrep.delete-user-no-authorisation-check (line 26): delete_user does not verify the requesting user is authorised to delete the target record — vulnerable to IDOR.
- **[WARNING]** rules.semgrep.delete-user-no-input-validation (line 26): delete_user does not validate that user_id is a positive integer before querying.

### claude (baseline)

- **Source file:** `tasks/task_database_02/code/baseline/claude_code.py`
- **Snapshot file:** `outputs/claude/baseline/20260407_113046/task_database_02.py`
- **Syntax valid:** Yes
- **Test pass rate:** N/A
- **Executed tests:** 0
- **Passed / Failed / Errors:** 0 / 0 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** no_tests
- **Correctness note:** No test file configured for this task.
- **LOC:** 137
- **Combined security findings:** 2
- **Combined weighted security score:** 5
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 0
- **Bandit density:** 0.00/100 LOC
- **Bandit weighted score:** 0
- **Bandit weighted density:** 0.00/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=0, LOW=0
- **Bandit CWE categories:** None

#### Bandit Findings

- No Bandit issues detected ✅

#### Semgrep Summary

- **Semgrep findings:** 2
- **Semgrep density:** 1.46/100 LOC
- **Semgrep weighted score:** 5
- **Semgrep weighted density:** 3.65/100 LOC
- **Semgrep rules triggered:** rules.semgrep.delete-user-no-authorisation-check, rules.semgrep.delete-user-no-input-validation

#### Semgrep Findings

- **[ERROR]** rules.semgrep.delete-user-no-authorisation-check (line 65): delete_user does not verify the requesting user is authorised to delete the target record — vulnerable to IDOR.
- **[WARNING]** rules.semgrep.delete-user-no-input-validation (line 65): delete_user does not validate that user_id is a positive integer before querying.

### gemini (baseline)

- **Source file:** `tasks/task_database_02/code/baseline/gemini_code.py`
- **Snapshot file:** `outputs/gemini/baseline/20260407_113046/task_database_02.py`
- **Syntax valid:** Yes
- **Test pass rate:** N/A
- **Executed tests:** 0
- **Passed / Failed / Errors:** 0 / 0 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** no_tests
- **Correctness note:** No test file configured for this task.
- **LOC:** 36
- **Combined security findings:** 1
- **Combined weighted security score:** 2
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 0
- **Bandit density:** 0.00/100 LOC
- **Bandit weighted score:** 0
- **Bandit weighted density:** 0.00/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=0, LOW=0
- **Bandit CWE categories:** None

#### Bandit Findings

- No Bandit issues detected ✅

#### Semgrep Summary

- **Semgrep findings:** 1
- **Semgrep density:** 2.78/100 LOC
- **Semgrep weighted score:** 2
- **Semgrep weighted density:** 5.56/100 LOC
- **Semgrep rules triggered:** rules.semgrep.delete-user-no-input-validation

#### Semgrep Findings

- **[WARNING]** rules.semgrep.delete-user-no-input-validation (line 4): delete_user does not validate that user_id is a positive integer before querying.

### gpt (security_aware)

- **Source file:** `tasks/task_database_02/code/security_aware/gpt_code.py`
- **Snapshot file:** `outputs/gpt/security_aware/20260407_113046/task_database_02.py`
- **Syntax valid:** Yes
- **Test pass rate:** N/A
- **Executed tests:** 0
- **Passed / Failed / Errors:** 0 / 0 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** no_tests
- **Correctness note:** No test file configured for this task.
- **LOC:** 82
- **Combined security findings:** 1
- **Combined weighted security score:** 2
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 0
- **Bandit density:** 0.00/100 LOC
- **Bandit weighted score:** 0
- **Bandit weighted density:** 0.00/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=0, LOW=0
- **Bandit CWE categories:** None

#### Bandit Findings

- No Bandit issues detected ✅

#### Semgrep Summary

- **Semgrep findings:** 1
- **Semgrep density:** 1.22/100 LOC
- **Semgrep weighted score:** 2
- **Semgrep weighted density:** 2.44/100 LOC
- **Semgrep rules triggered:** rules.semgrep.delete-user-no-input-validation

#### Semgrep Findings

- **[WARNING]** rules.semgrep.delete-user-no-input-validation (line 73): delete_user does not validate that user_id is a positive integer before querying.

### claude (security_aware)

- **Source file:** `tasks/task_database_02/code/security_aware/claude_code.py`
- **Snapshot file:** `outputs/claude/security_aware/20260407_113046/task_database_02.py`
- **Syntax valid:** Yes
- **Test pass rate:** N/A
- **Executed tests:** 0
- **Passed / Failed / Errors:** 0 / 0 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** no_tests
- **Correctness note:** No test file configured for this task.
- **LOC:** 223
- **Combined security findings:** 1
- **Combined weighted security score:** 2
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 0
- **Bandit density:** 0.00/100 LOC
- **Bandit weighted score:** 0
- **Bandit weighted density:** 0.00/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=0, LOW=0
- **Bandit CWE categories:** None

#### Bandit Findings

- No Bandit issues detected ✅

#### Semgrep Summary

- **Semgrep findings:** 1
- **Semgrep density:** 0.45/100 LOC
- **Semgrep weighted score:** 2
- **Semgrep weighted density:** 0.90/100 LOC
- **Semgrep rules triggered:** rules.semgrep.delete-user-no-input-validation

#### Semgrep Findings

- **[WARNING]** rules.semgrep.delete-user-no-input-validation (line 149): delete_user does not validate that user_id is a positive integer before querying.

### gemini (security_aware)

- **Source file:** `tasks/task_database_02/code/security_aware/gemini_code.py`
- **Snapshot file:** `outputs/gemini/security_aware/20260407_113046/task_database_02.py`
- **Syntax valid:** Yes
- **Test pass rate:** N/A
- **Executed tests:** 0
- **Passed / Failed / Errors:** 0 / 0 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** no_tests
- **Correctness note:** No test file configured for this task.
- **LOC:** 45
- **Combined security findings:** 2
- **Combined weighted security score:** 5
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 0
- **Bandit density:** 0.00/100 LOC
- **Bandit weighted score:** 0
- **Bandit weighted density:** 0.00/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=0, LOW=0
- **Bandit CWE categories:** None

#### Bandit Findings

- No Bandit issues detected ✅

#### Semgrep Summary

- **Semgrep findings:** 2
- **Semgrep density:** 4.44/100 LOC
- **Semgrep weighted score:** 5
- **Semgrep weighted density:** 11.11/100 LOC
- **Semgrep rules triggered:** rules.semgrep.delete-user-no-authorisation-check, rules.semgrep.delete-user-no-input-validation

#### Semgrep Findings

- **[ERROR]** rules.semgrep.delete-user-no-authorisation-check (line 3): delete_user does not verify the requesting user is authorised to delete the target record — vulnerable to IDOR.
- **[WARNING]** rules.semgrep.delete-user-no-input-validation (line 3): delete_user does not validate that user_id is a positive integer before querying.
