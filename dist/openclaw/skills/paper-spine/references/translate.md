# Translate Stage

This file is the canonical stage playbook for the paper-spine orchestrator.

## Purpose

Produce the complete `translation_zh/` package when `output_language=en` and
`translation_package=zh`. Every required file must be translated; partial
translation is a failed output.

Important: `translation_zh/` is the Chinese translation audit/intermediate
package. It is not the final user-facing Chinese document. When Word output is
enabled, the final Chinese deliverable must also be generated as one Word file:

- `paper_rewriting_output/final_paper/paper.zh.docx`
- `paper_rewriting_output/word_report.zh.md`

Do not report "Chinese translation: translation_zh/ - 10 files" as the final
Chinese doc deliverable. The user-facing result is `paper.zh.docx`.

## Three-Phase Flow

### Phase 1 - Inventory

List every file to translate. Write `translation_zh/manifest.md`.

Common files for both workflows include `writing_rationale_matrix.md`,
`citation_support_bank.md`, all research outputs, and the final paper text.

### Phase 2 - Translate

- Plain prose: translate full text; preserve LaTeX keys, labels, equations, URLs.
- Large tabular files: translate every row and cell; no summary.
- `full_paper_translation.zh.md`: title, abstract, every section, captions,
  tables, conclusion, appendix.

### Phase 3 - Final Chinese Word Document

After `translation_zh/full_paper_translation.zh.md` is complete, convert it into
the final user-facing Chinese Word document:

```bash
pandoc paper_rewriting_output/translation_zh/full_paper_translation.zh.md \
  -o paper_rewriting_output/final_paper/paper.zh.docx
python scripts/word_guard.py paper_rewriting_output/final_paper/paper.zh.docx \
  --markdown --output paper_rewriting_output/word_report.zh.md
```

If pandoc is unavailable while Word output is required, write BLOCKED/FAIL in
the relevant report and do not claim the Chinese deliverable is complete.

### Phase 4 - Verify

```bash
python scripts/translate_guard.py paper_rewriting_output --markdown --write
python scripts/progress_check.py paper_rewriting_output --gate word --require
```

Require PASS. Write `translation_coverage.md`.

## Integration

Called after LaTeX and before audit. The orchestrator requires translate guard
to PASS before audit begins. When Word output is enabled, the workflow is not
complete until `final_paper/paper.zh.docx` and `word_report.zh.md` exist.
