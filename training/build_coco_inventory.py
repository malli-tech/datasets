import json
from pathlib import Path

PROJECT = Path(r"D:\AI_Smart_Blind_Stick")

COCO_ANNOTATIONS = (
    PROJECT
    / "datasets"
    / "COCO"
    / "annotations"
    / "instances_train2017.json"
)

OUTPUT = (
    PROJECT
    / "research"
    / "coco_class_inventory.json"
)

with open(COCO_ANNOTATIONS, "r", encoding="utf-8") as f:
    data = json.load(f)

categories = data["categories"]

inventory = {
    "dataset": "COCO",
    "class_count": len(categories),
    "classes": []
}

for category in sorted(categories, key=lambda x: x["id"]):
    inventory["classes"].append({
        "original_id": category["id"],
        "original_name": category["name"],
        "unified_name": category["name"]
    })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(
        inventory,
        f,
        indent=2,
        ensure_ascii=False
    )

print("=" * 50)
print("COCO CLASS INVENTORY CREATED")
print("=" * 50)
print(f"Classes : {len(categories)}")
print(f"Output  : {OUTPUT}")
print("=" * 50)