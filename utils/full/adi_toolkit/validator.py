from lxml import etree


def validate_adi(xml_path):
    print(f"[INFO] Validating ADI XML: {xml_path}")
    try:
        tree = etree.parse(xml_path)
        root = tree.getroot()
        if root.tag != "ADI":
            print("[ERROR] Root tag is not <ADI>")
        else:
            print("[✓] Root tag is valid")
        # Add more validation logic as needed
    except Exception as e:
        print(f"[ERROR] Failed to parse XML: {e}")
