import json
from pathlib import Path

PROJECT = Path(r"D:\AI_Smart_Blind_Stick")

ANNOTATION_FILE = (
    PROJECT
    / "datasets"
    / "COCO"
    / "annotations"
    / "instances_train2017.json"
)

IMAGE_DIR = (
    PROJECT
    / "datasets"
    / "COCO"
    / "train2017"
)


print("=" * 60)
print("COCO DATASET INSPECTION")
print("=" * 60)

print("\nLoading annotation file...")
with open(ANNOTATION_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

images = data["images"]
annotations = data["annotations"]
categories = data["categories"]

print(f"Images listed in annotations : {len(images):,}")
print(f"Bounding-box annotations     : {len(annotations):,}")
print(f"Categories                   : {len(categories)}")

# ---------------------------------------------------------
# 1. Check category IDs
# ---------------------------------------------------------

category_ids = {c["id"] for c in categories}

print("\nCategory ID check:")
print(f"Unique category IDs: {len(category_ids)}")

# ---------------------------------------------------------
# 2. Check actual image files
# ---------------------------------------------------------

print("\nChecking image files...")

missing_images = []

for image_info in images:
    filename = image_info["file_name"]
    image_path = IMAGE_DIR / filename

    if not image_path.exists():
        missing_images.append(filename)

print(f"Missing image files: {len(missing_images):,}")

if missing_images:
    print("\nFirst missing files:")
    for filename in missing_images[:10]:
        print(filename)

# ---------------------------------------------------------
# 3. Check annotation category IDs
# ---------------------------------------------------------

unknown_category_ids = set()

for ann in annotations:
    category_id = ann["category_id"]

    if category_id not in category_ids:
        unknown_category_ids.add(category_id)

print("\nAnnotation category check:")
print(f"Unknown category IDs: {len(unknown_category_ids)}")

if unknown_category_ids:
    print("Unknown IDs:", sorted(unknown_category_ids))

# ---------------------------------------------------------
# 4. Check annotation image IDs
# ---------------------------------------------------------

image_ids = {img["id"] for img in images}

unknown_image_ids = set()

for ann in annotations:
    image_id = ann["image_id"]

    if image_id not in image_ids:
        unknown_image_ids.add(image_id)

print("\nAnnotation image-ID check:")
print(f"Unknown image IDs: {len(unknown_image_ids)}")

# ---------------------------------------------------------
# 5. Print categories
# ---------------------------------------------------------

print("\nCOCO categories:")

for category in categories:
    print(f"{category['id']:>2} : {category['name']}")

# ---------------------------------------------------------
# Final result
# ---------------------------------------------------------

print("\n" + "=" * 60)

if (
    len(categories) == 80
    and len(missing_images) == 0
    and len(unknown_category_ids) == 0
    and len(unknown_image_ids) == 0
):
    print("COCO INSPECTION PASSED")
else:
    print("COCO INSPECTION FOUND ISSUES")

print("=" * 60)