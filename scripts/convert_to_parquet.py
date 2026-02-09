import argparse
import logging
from pathlib import Path

import pandas as pd


def iter_csv_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.csv") if p.is_file()]


def convert_csv_to_parquet(src_root: Path, dst_root: Path) -> None:
    csv_files = iter_csv_files(src_root)
    if not csv_files:
        logging.warning("No CSV files found under %s", src_root)
        return

    for csv_path in csv_files:
        rel_path = csv_path.relative_to(src_root)
        parquet_path = dst_root / rel_path.with_suffix(".parquet")
        parquet_path.parent.mkdir(parents=True, exist_ok=True)

        logging.info("Reading %s", csv_path)
        df = pd.read_csv(csv_path)

        logging.info("Writing %s", parquet_path)
        df.to_parquet(parquet_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert all CSV files under a folder to Parquet, preserving structure."
    )
    parser.add_argument(
        "--src",
        default="dataset",
        help="Source folder containing CSV files (default: dataset)",
    )
    parser.add_argument(
        "--dst",
        default="data/raw",
        help="Destination root for Parquet files (default: data/raw)",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()

    src_root = Path(args.src).resolve()
    dst_root = Path(args.dst).resolve()

    if not src_root.exists():
        raise SystemExit(f"Source path does not exist: {src_root}")

    convert_csv_to_parquet(src_root, dst_root)


if __name__ == "__main__":
    main()
