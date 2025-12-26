from pathlib import Path
import subprocess
import textwrap


def test_build_toc_from_chapters_md(tmp_path):
    """
    Verifiziert:
    - TOC wird aus chapter-*.md korrekt erzeugt
    - Reihenfolge nach Kapitelnummer
    - Titel werden aus H1 gelesen, Fallback wenn kein Titel vorhanden
    """

    chapters = tmp_path / "manuscript" / "chapters"
    out_dir = tmp_path / "manuscript" / "front-matter"
    chapters.mkdir(parents=True)
    out_dir.mkdir(parents=True)

    # Kapiteldateien anlegen (bewusst gemischt: mit/ohne Titel)
    files = {
        "01-chapter.md": "# Kapitel 1 – Architektur statt Ideologie\n\nText",
        "02-chapter.md": "# Kapitel 2\n\nText",
        "03-chapter.md": "# Kapitel 3 – Macht ohne Architektur\n\nText",
        "04-chapter.md": "# Kapitel 4\n\nText",
        "05-chapter.md": "# Kapitel 5\n\nText",
        "06-chapter.md": "# Kapitel 6\n\nText",
        "07-chapter.md": "# Kapitel 7\n\nText",
        "08-chapter.md": "# Kapitel 8 – Der Bürger als Eigentümer des Staates\n\nText",
        "09-chapter.md": "# Kapitel 9 – Prozesse als Nervensystem des Staates\n\nText",
        # absichtlich falsche Nummer im Titel → Filename zählt
        "10-chapter.md": "# Kapitel 11 – Daten als Realitätssensor des Staates\n\nText",
        "11-chapter.md": "# Kapitel 11\n\nText",
        "12-chapter.md": "# Kapitel 12 – Pflege, Kontrolle und Weiterentwicklung des Systems\n\nText",
        "13-chapter.md": "# Kapitel 13 – Der Staat als lernende Architektur\n\nText",
    }

    for name, content in files.items():
        (chapters / name).write_text(content, encoding="utf-8")

    toc_out = out_dir / "toc.md"

    # Script ausführen
    result = subprocess.run(
        [
            "python",
            "scripts/build_toc_from_chapters.py",
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
        capture_output=True,
        text=True,
        check=True,
    )

    toc = toc_out.read_text(encoding="utf-8").strip()

    expected = textwrap.dedent(
        """\
        # Inhaltsverzeichnis

        - Kapitel 1: Kapitel 1 – Architektur statt Ideologie
        - Kapitel 2: Kapitel 2
        - Kapitel 3: Kapitel 3 – Macht ohne Architektur
        - Kapitel 4: Kapitel 4
        - Kapitel 5: Kapitel 5
        - Kapitel 6: Kapitel 6
        - Kapitel 7: Kapitel 7
        - Kapitel 8: Kapitel 8 – Der Bürger als Eigentümer des Staates
        - Kapitel 9: Kapitel 9 – Prozesse als Nervensystem des Staates
        - Kapitel 10: Kapitel 11 – Daten als Realitätssensor des Staates
        - Kapitel 11: Kapitel 11
        - Kapitel 12: Kapitel 12 – Pflege, Kontrolle und Weiterentwicklung des Systems
        - Kapitel 13: Kapitel 13 – Der Staat als lernende Architektur
        """
    ).strip()

    assert toc == expected
