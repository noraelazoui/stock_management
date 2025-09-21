from models.database import db
from bson.objectid import ObjectId

# Update the fabrication record
doc_id = ObjectId("68bc624a6086478eaa6ba373")
result = db.fabrications.update_one(
    {"_id": doc_id},
    {"$set": {"detail-fabrication": {"article": []}}}
)

print(f"Modified {result.modified_count} document(s)")
