# arXiv Source Workflow

## Why Use Source Instead Of PDF Alone

Source bundles expose:

1. section splits
2. table files
3. figure code or assets
4. appendix organization
5. macros and naming conventions

This is especially useful for:

1. related work organization
2. method subsection design
3. experiment/table layout reuse

## Default Workflow

1. pick exemplar papers by section quality, not just citation count
2. download source with `scripts/fetch_arxiv_source.py`
3. inspect candidate main `.tex` and included subfiles
4. read only the relevant source fragments
5. extract organization patterns, not sentences

## Example

`ReAct` (`2210.03629`) was verified during skill creation:

1. arXiv e-print works
2. the source bundle contains split files such as:
   - `text/method.tex`
   - `table/*.tex`
   - figure assets

That makes it a good reference for section decomposition and table/figure separation.

## Command

```bash
python3 .agents/skills/paper-writing/scripts/fetch_arxiv_source.py 2210.03629
```

## What To Look For

1. does the paper isolate related work or blend it into introduction
2. how many method subsections it uses
3. where tables live
4. whether architecture figures are code-generated or image-based
5. how appendix references are wired
