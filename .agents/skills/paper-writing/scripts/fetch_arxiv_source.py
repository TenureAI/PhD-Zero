#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import os
import pathlib
import shutil
import tarfile
import tempfile
import urllib.request


def download_source(arxiv_id: str, destination: pathlib.Path) -> pathlib.Path:
    url = f"https://arxiv.org/e-print/{arxiv_id}"
    target = destination / f"{arxiv_id}.tar"
    with urllib.request.urlopen(url) as response, target.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    return target


def extract_tar(tar_path: pathlib.Path, destination: pathlib.Path) -> pathlib.Path:
    extract_dir = destination / tar_path.stem
    extract_dir.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path) as archive:
        archive.extractall(extract_dir, filter="data")
    return extract_dir


def list_tex_files(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(path for path in root.rglob("*.tex") if path.is_file())


def score_tex_file(path: pathlib.Path) -> tuple[int, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    score = 0
    for token in ("\\documentclass", "\\begin{document}", "\\input{", "\\include{", "\\section{"):
        if token in text:
            score += 1
    return score, str(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and inspect an arXiv source bundle.")
    parser.add_argument("arxiv_id", help="arXiv identifier, e.g. 2210.03629")
    parser.add_argument("--out", default=".cache/arxiv-sources", help="Output directory")
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    tar_path = download_source(args.arxiv_id, out_dir)
    extract_dir = extract_tar(tar_path, out_dir)
    tex_files = list_tex_files(extract_dir)
    ranked = sorted((score_tex_file(path) for path in tex_files), reverse=True)

    print(f"arxiv_id: {args.arxiv_id}")
    print(f"tarball: {tar_path}")
    print(f"extracted_to: {extract_dir}")
    print("candidate_main_tex:")
    for score, path in ranked[:10]:
        print(f"  score={score} path={path}")
    print("all_tex_files:")
    for path in tex_files:
        print(f"  {path}")


if __name__ == "__main__":
    main()
