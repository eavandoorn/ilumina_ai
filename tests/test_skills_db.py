import unittest
import requests

class TestSkillDatabase(unittest.TestCase):
    def test_database_reachable(self):
        """Test if the pinecone skill server is reachable on port 7000"""
        try:
            response = requests.get("http://localhost:7000")
            # If it's a query engine, it might return a 404 or a specific JSON
            # but a 200 or 404 means the port is open.
            self.assertIn(response.status_code, [200, 404, 405])
        except Exception as e:
            self.fail(f"Database not reachable: {e}")

if __name__ == '__main__':
    unittest.main()
