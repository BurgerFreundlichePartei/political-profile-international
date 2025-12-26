from pathlib import Path
import subprocess
import textwrap


def test_build_toc_from_chapters_md(tmp_path):
    chapters = tmp_path / "manuscript" / "chapters"
    out_dir = tmp_path / "manuscript" / "front-matter"
    chapters.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "01-chapter.md": "# Kapitel 1 – Architektur statt Ideologie\n\nText",
        "02-chapter.md": "# Kapitel 2 – Warum Demokratien scheitern können, obwohl sie legitim sind\n\nText",
        "03-chapter.md": "# Kapitel 3 – Macht ohne Architektur\n\nText",
        "04-chapter.md": "# Kapitel 4 – Struktur ist keine Bürokratie\n\nText",
        "05-chapter.md": "# Kapitel 5 – Kontrolle ohne Misstrauen\n\nText",
        "06-chapter.md": "# Kapitel 6 – Sichtbarkeit ohne Kontrolle ist Illusion\n\nText",
        "07-chapter.md": "# Kapitel 7 – Eigentümerschaft ohne Mandat bleibt Fiktion\n\nText",
        "08-chapter.md": "# Kapitel 8 – Der Bürger als Eigentümer des Staates\n\nText",
        "09-chapter.md": "# Kapitel 9 – Prozesse als Nervensystem des Staates\n\nText",
        "10-chapter.md": "# Kapitel 11 – Daten als Realitätssensor des Staates\n\nText",
        "11-chapter.md": "# Kapitel 11 – Identität ohne Architektur wird zum Konflikt\n\nText",
        "12-chapter.md": "# Kapitel 12 – Pflege, Kontrolle und Weiterentwicklung des Systems\n\nText",
        "13-chapter.md": "# Kapitel 13 – Der Staat als lernende Architektur\n\nText",
    }

    for name, content in files.items():
        (chapters / name).write_text(content, encoding="utf-8")

    toc_out = out_dir / "toc.md"

    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "build_toc_from_chapters.py"
    assert script_path.exists(), f"Script not found: {script_path}"

    result = subprocess.run(
        [
            "python",
            str(script_path),
            "--chapters-dir",
            str(chapters),
            "--out",
            str(toc_out),
            "--format",
            "md",
            "--heading",
            "Inhaltsverzeichnis",
            "--lang",
            "de",
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        "TOC generator failed.\n"
        f"cmd: python {script_path} ...\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}\n"
    )

    assert toc_out.exists(), f"TOC output not created: {toc_out}"

    toc = toc_out.read_text(encoding="utf-8").strip()

    expected = textwrap.dedent(
        """\
        # Inhaltsverzeichnis

        - Kapitel 1: Architektur statt Ideologie
        - Kapitel 2: Warum Demokratien scheitern können, obwohl sie legitim sind
        - Kapitel 3: Macht ohne Architektur
        - Kapitel 4: Struktur ist keine Bürokratie
        - Kapitel 5: Kontrolle ohne Misstrauen
        - Kapitel 6: Sichtbarkeit ohne Kontrolle ist Illusion
        - Kapitel 7: Eigentümerschaft ohne Mandat bleibt Fiktion
        - Kapitel 8: Der Bürger als Eigentümer des Staates
        - Kapitel 9: Prozesse als Nervensystem des Staates
        - Kapitel 10: Daten als Realitätssensor des Staates
        - Kapitel 11: Identität ohne Architektur wird zum Konflikt
        - Kapitel 12: Pflege, Kontrolle und Weiterentwicklung des Systems
        - Kapitel 13: Der Staat als lernende Architektur
        """
    ).strip()

    assert toc == expected
