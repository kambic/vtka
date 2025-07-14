import zipfile
from pathlib import Path

# Create project structure
structure = {
    "adi-toolkit/adi_toolkit/__init__.py": "",
    "adi-toolkit/adi_toolkit/generator.py": """<PASTE generator.py CONTENT HERE>""",
    "adi-toolkit/adi_toolkit/validator.py": """<PASTE validator.py CONTENT HERE>""",
    "adi-toolkit/adi_toolkit/cli.py": """<PASTE cli.py CONTENT HERE>""",
    "adi-toolkit/examples/sample_input.yaml": """<PASTE sample_input.yaml CONTENT HERE>""",
    "adi-toolkit/pyproject.toml": """<PASTE pyproject.toml CONTENT HERE>""",
    "adi-toolkit/Dockerfile": """<PASTE Dockerfile CONTENT HERE>""",
    "adi-toolkit/README.md": """<PASTE README CONTENT HERE>""",
}

# Write files to disk
for path, content in structure.items():
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)

# Create zip
with zipfile.ZipFile("adi-toolkit.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    for path in Path("adi-toolkit").rglob("*"):
        zipf.write(path, path.relative_to(Path("adi-toolkit").parent))

print("[✓] ZIP file created: adi-toolkit.zip")
