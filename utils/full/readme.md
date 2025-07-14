Once you've pasted the above into build_zip.py or individual files, you can run the script to build adi-toolkit.zip.

Would you like help with:

    Uploading the ZIP to a repo or file server?

    Adding unit tests or schema validation next?

    File delivery integration (e.g. packaging XML with media references)?

Let me know — I'm here to help!

CLI Support: Add to cli.py

Add this to the CLI:

    d = subparsers.add_parser("package", help="Package ADI XML with media into a ZIP")
    d.add_argument("xml", help="Path to ADI XML")
    d.add_argument("media", nargs="+", help="List of media file paths")
    d.add_argument("output", help="Output ZIP archive")

In run_cli():

    elif args.command == "package":
        from .packager import package_delivery
        package_delivery(args.xml, args.media, args.output)

🧪 Example Usage

# Generate XML

adi-toolkit generate examples/sample_input.yaml output.xml

# Package XML with assets

adi-toolkit package output.xml media/poster.jpg media/movie.mp4 delivery_package.zip

📌 Summary of New Features
Feature Status
✅ Unit tests with pytest ✅ Done
✅ CLI for test automation ✅ Done
✅ Package XML + media ✅ Done
✅ CLI zip bundling ✅ Done

Would you like to:

    Auto-name ZIPs using metadata? (title, asset_id, date)

    Validate file presence inside package_delivery()?

    Add s3 upload / network delivery next?

Let me know!
4

Great idea — let’s enhance package_delivery() to strictly validate the presence of all media files before creating the ZIP. This prevents incomplete delivery packages.
✅ Updated package_delivery() With Validation

import zipfile
from pathlib import Path

def package_delivery(xml_path, media_files, output_zip, strict=True):
missing_files = [f for f in media_files if not Path(f).exists()]

    if missing_files and strict:
        print("[✗] Missing media files:")
        for mf in missing_files:
            print(f"   - {mf}")
        raise FileNotFoundError("One or more required media files are missing.")

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        xml_path = Path(xml_path)
        zipf.write(xml_path, arcname=xml_path.name)

        for f in media_files:
            f = Path(f)
            if f.exists():
                zipf.write(f, arcname=f.name)
            else:
                print(f"[WARN] Skipping missing file: {f} (strict={strict})")

    print(f"[✓] Delivery package created: {output_zip}")

🧪 Optional: strict=False

If you pass strict=False, it will:

    Warn for missing files

    Still proceed with packaging

Usage:

package_delivery("output.xml", ["poster.jpg", "movie.mp4"], "bundle.zip", strict=False)

🖥 CLI Integration (optional flag)

In cli.py, update:

    d = subparsers.add_parser("package", help="Package ADI XML and media")
    d.add_argument("xml", help="ADI XML path")
    d.add_argument("media", nargs="+", help="Media file paths")
    d.add_argument("output", help="Output ZIP archive")
    d.add_argument("--no-strict", action="store_true", help="Ignore missing media files")

And update this block:

    elif args.command == "package":
        from .packager import package_delivery
        package_delivery(args.xml, args.media, args.output, strict=not args.no_strict)

✅ Result

# Strict (default)

adi-toolkit package output.xml poster.jpg movie.mp4 out.zip

# Will raise error if files are missing

# Non-strict

adi-toolkit package output.xml poster.jpg movie.mp4 out.zip --no-strict

# Will skip missing files with warnings

Would you like:

    Auto-naming the output zip based on metadata (e.g., Inception_2025.zip)?

    Media file discovery based on a config file?
