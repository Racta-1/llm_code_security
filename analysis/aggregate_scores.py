# python analysis/aggregate_scores.py --results-dir results/per_sample/20260408_174011 --output-dir results/aggregate/20260408_174011

import argparse
import json
from pathlib import Path
from typing import Dict, List

import pandas as pd


def load_results(results_dir: str) -> List[Dict]:
    root = Path(results_dir)
    if not root.exists():
        raise FileNotFoundError(f"Results directory not found: {results_dir}")

    rows = []
    for json_file in sorted(root.rglob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                data["_source_file"] = str(json_file)
                rows.append(data)
        except Exception as e:
            print(f"[WARN] Skipping {json_file}: {e}")

    return rows


def build_dataframe(rows: List[Dict]) -> pd.DataFrame:
    if not rows:
        raise ValueError("No result JSON files found.")

    df = pd.DataFrame(rows)

    expected_cols = [
        "run_id",
        "task",
        "model",
        "mode",
        "pass_rate",
        "security_findings",
        "vulnerability_density",
        "security_score",
        "overall_score",
        "functional_success",
        "secure_success",
        "combined_vuln_density",
    ]

    for col in expected_cols:
        if col not in df.columns:
            df[col] = None

    # Backward compatibility:
    # if vulnerability_density is missing but combined_vuln_density exists, use it
    if df["vulnerability_density"].isna().all() and "combined_vuln_density" in df.columns:
        df["vulnerability_density"] = df["combined_vuln_density"]

    # If secure_success is missing, derive it from security_findings
    if df["secure_success"].isna().all() and "security_findings" in df.columns:
        df["secure_success"] = df["security_findings"].apply(
            lambda x: 1 if pd.notna(x) and x == 0 else 0
        )

    numeric_cols = [
        "pass_rate",
        "security_findings",
        "vulnerability_density",
        "security_score",
        "overall_score",
        "functional_success",
        "secure_success",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def summarize_by_task(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "task",
        "mode",
        "model",
        "pass_rate",
        "security_findings",
        "vulnerability_density",
        "security_score",
        "overall_score",
        "functional_success",
        "secure_success",
    ]
    return df[cols].sort_values(["task", "mode", "model"]).reset_index(drop=True)


def summarize_across_tasks(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["mode", "model"], as_index=False)
        .agg(
            num_tasks=("task", "count"),
            avg_pass_rate=("pass_rate", "mean"),
            avg_security_findings=("security_findings", "mean"),
            avg_vulnerability_density=("vulnerability_density", "mean"),
            avg_security_score=("security_score", "mean"),
            avg_overall_score=("overall_score", "mean"),
            functional_success_rate=("functional_success", "mean"),
            secure_success_rate=("secure_success", "mean"),
        )
    )

    summary["functional_success_rate"] = summary["functional_success_rate"] * 100
    summary["secure_success_rate"] = summary["secure_success_rate"] * 100

    return summary.sort_values(
        ["mode", "avg_overall_score"], ascending=[True, False]
    ).reset_index(drop=True)


def summarize_mode_only(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["mode"], as_index=False)
        .agg(
            num_tasks=("task", "count"),
            avg_pass_rate=("pass_rate", "mean"),
            avg_security_findings=("security_findings", "mean"),
            avg_vulnerability_density=("vulnerability_density", "mean"),
            avg_security_score=("security_score", "mean"),
            avg_overall_score=("overall_score", "mean"),
            functional_success_rate=("functional_success", "mean"),
            secure_success_rate=("secure_success", "mean"),
        )
    )

    summary["functional_success_rate"] = summary["functional_success_rate"] * 100
    summary["secure_success_rate"] = summary["secure_success_rate"] * 100

    return summary.sort_values("avg_overall_score", ascending=False).reset_index(drop=True)


def save_outputs(
    df_task: pd.DataFrame,
    df_model_mode: pd.DataFrame,
    df_mode: pd.DataFrame,
    output_dir: str,
) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    df_task.to_csv(out / "combined_scores_by_task.csv", index=False)
    df_model_mode.to_csv(out / "combined_scores_by_mode_and_model.csv", index=False)
    df_mode.to_csv(out / "combined_scores_by_mode.csv", index=False)

    with pd.ExcelWriter(out / "combined_scores_summary.xlsx", engine="openpyxl") as writer:
        df_task.to_excel(writer, sheet_name="by_task", index=False)
        df_model_mode.to_excel(writer, sheet_name="by_mode_model", index=False)
        df_mode.to_excel(writer, sheet_name="by_mode", index=False)


def print_summary(df_model_mode: pd.DataFrame, df_mode: pd.DataFrame) -> None:
    print("\n=== Average scores by mode and model ===")
    print(df_model_mode.to_string(index=False))

    print("\n=== Average scores by mode only ===")
    print(df_mode.to_string(index=False))


def main():
    parser = argparse.ArgumentParser(description="Aggregate combined scores across all tasks.")
    parser.add_argument(
        "--results-dir",
        required=True,
        help="Path to results/per_sample/<run_id> or parent folder containing result JSON files",
    )
    parser.add_argument(
        "--output-dir",
        default="results/aggregate",
        help="Directory to save summary CSV/XLSX outputs",
    )
    args = parser.parse_args()

    rows = load_results(args.results_dir)
    df = build_dataframe(rows)

    df_task = summarize_by_task(df)
    df_model_mode = summarize_across_tasks(df)
    df_mode = summarize_mode_only(df)

    save_outputs(df_task, df_model_mode, df_mode, args.output_dir)
    print_summary(df_model_mode, df_mode)

    print(f"\nSaved summaries to: {args.output_dir}")


if __name__ == "__main__":
    main()