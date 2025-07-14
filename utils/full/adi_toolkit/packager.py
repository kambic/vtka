import shutil
import zipfile
from pathlib import Path


def package_delivery(xml_path, media_files, output_zip):
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(xml_path, Path(xml_path).name)
        for f in media_files:
            f = Path(f)
            if f.exists():
                zipf.write(f, f.name)
            else:
                print(f"[WARN] Media file not found: {f}")
    print(f"[✓] Delivery package created: {output_zip}")
