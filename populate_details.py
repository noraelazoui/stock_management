from models.database import db
from bson.objectid import ObjectId
from models.fabrication import Fabrication

# Call get_details_fabrication to populate the details
result = Fabrication.get_details_fabrication("mama", "1")

# Print the result
print("Updated fabrication details:", result)

# Verify the update
fabrication = db.fabrications.find_one({"_id": ObjectId("68bc624a6086478eaa6ba373")})
print("\nVerifying fabrication document:", fabrication.get("detail-fabrication", {}))
