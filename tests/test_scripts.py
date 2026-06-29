from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class ScriptSmokeTests(unittest.TestCase):
    def test_latex_guard_passes_valid_fixture(self) -> None:
        result = run_script(
            "src/scripts/latex_guard.py",
            str(FIXTURES / "mini_paper.tex"),
            "--bib",
            str(FIXTURES / "references.bib"),
            "--markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("Errors: 0", result.stdout)

    def test_latex_guard_flags_author_year_citation(self) -> None:
        # Regression: SKILL.md and references/latex.md say latex_guard rejects
        # author-year citations; it must actually fire on (Name, Year) in the body.
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "ay.tex"
            tex.write_text(
                r"""\documentclass{article}
\title{Author Year Citation Test}
\begin{document}
\maketitle
\section{Introduction}
Prior work (Smith et al., 2019) and (Jones and Lee, 2021) studied this problem.
\end{document}
""",
                encoding="utf-8",
            )
            result = run_script("src/scripts/latex_guard.py", str(tex), "--markdown")
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertIn("Author-year citation", result.stdout)

    def test_citation_bank_reference_format_is_case_insensitive(self) -> None:
        # Regression: has_reference_format matched only capital-P "Proceedings"/
        # "Journal"/"arXiv", so a legitimate lowercase channel label like
        # "Conference proceedings" was wrongly treated as missing a reference.
        sys.path.insert(0, str(ROOT / "src" / "scripts"))
        from citation_bank_check import has_reference_format  # noqa: PLC0415

        self.assertTrue(has_reference_format(["C1", "Conference proceedings", "2023"]))
        self.assertTrue(has_reference_format(["C2", "arxiv:2305.14314"]))
        self.assertTrue(has_reference_format(["C3", "Journal of ML"]))
        self.assertFalse(has_reference_format(["C4", "just a claim sentence."]))

    def test_style_metrics_reports_sections(self) -> None:
        result = run_script("src/scripts/style_metrics.py", str(FIXTURES / "mini_paper.tex"), "--markdown")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("# Style Metrics", result.stdout)
        self.assertIn("Introduction", result.stdout)

    def test_revision_audit_reports_similarity(self) -> None:
        result = run_script(
            "src/scripts/revision_audit.py",
            str(FIXTURES / "mini_paper.tex"),
            str(FIXTURES / "mini_paper_revised.tex"),
            "--markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("# Revision Audit", result.stdout)
        self.assertIn("Near-identical revised paragraphs", result.stdout)

    def test_reference_inventory_indexes_local_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            refs = base / "refs"
            refs.mkdir()
            (refs / "paper.pdf").write_bytes(b"%PDF-1.4\n")
            (refs / "notes.txt").write_text("local reference notes", encoding="utf-8")
            out = base / "out"
            result = run_script(
                "src/scripts/reference_inventory.py",
                str(refs),
                "--output-dir",
                str(out),
                "--mode",
                "specified_paths",
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            index = out / "reference_materials" / "source_index.md"
            self.assertTrue(index.exists())
            text = index.read_text(encoding="utf-8")
            self.assertIn("specified_paths", text)
            self.assertIn(str(refs / "paper.pdf"), text)

    def test_citation_bank_check_enforces_candidate_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bank = Path(tmp) / "citation_support_bank.md"
            lines = [
                "# Citation Support Bank",
                "",
                "| Candidate ID | Reference/BibTeX | Year | Recency | Supports Section | Support Claim Sentence | Why This Paper Fits | Source |",
                "|---|---|---|---|---|---|---|---|",
            ]
            for index in range(1, 61):
                lines.append(
                    f"| C{index:03d} | @article{{ref{index}, year={{2024}}, doi={{10.0000/ref{index}}}}} | 2024 | recent | Introduction | "
                    f"This paper supports one specific manuscript sentence about the literature context and prevents unsupported claims. | "
                    f"It fits the same-field or adjacent-field context needed for background and discussion. | REF{index:03d} |"
                )
            bank.write_text("\n".join(lines), encoding="utf-8")
            result = run_script(
                "src/scripts/citation_bank_check.py",
                str(bank),
                "--target-count",
                "20",
                "--markdown",
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("Status: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
