import unittest
from models.database import db
from bson import ObjectId

class TestStockManagerControllers(unittest.TestCase):
    def setUp(self):
        # Ensure a clean state before each test
        db.articles.delete_many({"name": "UnitTest Article"})
        self.article_id = db.articles.insert_one({
            "name": "UnitTest Article",
            "description": "UnitTest Description",
            "quantity": 10,
            "price": 5.99
        }).inserted_id

    def tearDown(self):
        # Clean up after each test except delete
        pass

    def test_add_article(self):
        article = db.articles.find_one({"_id": self.article_id})
        self.assertIsNotNone(article)
        self.assertEqual(article["name"], "UnitTest Article")

    def test_update_article(self):
        db.articles.update_one({"_id": self.article_id}, {"$set": {"quantity": 20}})
        updated = db.articles.find_one({"_id": self.article_id})
        self.assertEqual(updated["quantity"], 20)

    # Delete test removed as requested

if __name__ == "__main__":
    unittest.main()
