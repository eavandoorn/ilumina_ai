import requests
from typing import List

class SkillManager:
    def __init__(self, endpoint="http://localhost:8080"):
        self.endpoint = endpoint

    def get_skills(self, query: str) -> str:
        """This function retrieves skills from the skill server that provide the closest match to a query string 'string'."""
        try:
            # This now hits the Gateway script which handles the /query route
            response = requests.post(
                f"{self.endpoint}/query", 
                json={"query": query},
                timeout=10,
                headers={"Content-Type":"application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if not results:
                    return f"No specific skills found for '{query}'."
                
                context_blocks = []
                for res in results:
                    name = res.get("name", "Unknown Skill")
                    content = res.get("raw_content", "")
                    context_blocks.append(f"--- SKILL: {name} ---\n{content}")

                print("\n\n".join(context_blocks))
                return "\n\n".join(context_blocks)
            else:
                return f"Database error: Received status {response.status_code} from skill server."
        except Exception as e:
            return f"Connection error: Could not reach the skill database at {self.endpoint}. Error: {str(e)}"