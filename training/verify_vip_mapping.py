import zipfile
import collections
import xml.etree.ElementTree as ET
from pathlib import Path

ZIP_PATH = Path(
    r"D:\AI_Smart_Blind_Stick\datasets\VIP-Mobility360\VIP-Mobility360.zip"
)

print("=" * 60)
print("VERIFYING VIP YOLO ID -> XML CLASS NAME MAPPING")
print("=" * 60)

pairs = collections.defaultdict(collections.Counter)

with zipfile.ZipFile(ZIP_PATH, "r") as z:

    label_files = [
        x
        for x in z.infolist()
        if "/labels/" in x.filename
        and x.filename.endswith(".txt")
    ]

    print(f"YOLO label files: {len(label_files):,}")

    for index, label_file in enumerate(label_files, start=1):

        xml_name = (
            label_file.filename
            .replace("/labels/", "/XML/")
            .replace(".txt", ".xml")
        )

        label_text = z.read(label_file).decode(
            "utf-8",
            errors="ignore"
        )

        xml_root = ET.fromstring(z.read(xml_name))

        xml_objects = xml_root.findall("./object")

        for line in label_text.splitlines():

            parts = line.split()

            if not parts:
                continue

            yolo_class_id = parts[0]

            # We only need the first XML object for this
            # consistency check when the image has one object.
            for obj in xml_objects:
                name_element = obj.find("name")

                if name_element is not None:
                    class_name = name_element.text
                    pairs[yolo_class_id][class_name] += 1
                    break

        if index % 10000 == 0:
            print(f"Processed: {index:,}")

print()
print("=" * 60)
print("OBSERVED ID -> XML CLASS NAME")
print("=" * 60)

for class_id in sorted(pairs, key=lambda x: int(x)):

    print()
    print(f"YOLO ID {class_id}:")

    for name, count in pairs[class_id].most_common():
        print(f"    {name}: {count:,}")

print()
print("=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)