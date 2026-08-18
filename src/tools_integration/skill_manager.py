import requests
from typing import List
import json

class SkillManager:
    def __init__(self, endpoint="http://localhost:7000"):
        self.endpoint = endpoint
        # The port 7000 is mapped to 6333 (Qdrant default) in our docker-compose
        self.api_url = f"{self.endpoint}"

    def get_skills(self, query: str) -> str:
        """
        Use this tool to fetch technical instructions and coding patterns from the 
        internal vector database. Input should be a short query like 'react' or 'python'.
        """
        try:
            # Qdrant/Pinecone-style logic: 
            # We perform a search on the 'skills' collection.
            # Since we are using a local proxy/port, we hit the search endpoint.
            
            # Note: In a production Qdrant setup, this would be a POST to /collection/points/search
            # For this implementation, we assume the backend handles the query logic.
            search_url = f"{self.api_url}/search" 
            
            # If the backend is a raw Qdrant instance, the payload would look like this:
            payload = {
                "vector": [0.1, 0.2, 0.3], # Placeholder: In a real app, we'd embed the 'query' string
                "limit": 3,
                "filter": None
            }
            
            # For the current architecture, we'll perform a GET/POST to the 
            # skill-specific endpoint provided by our local server.
            response = requests.post(
                f"{self.api_url}/query", 
                json={"query": query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # Extract the content from the results
                # Assuming the backend returns a list of results with 'content' fields
                results = data.get("results", [])
                if not results:
                    return f"No specific skills found for '{query}'."
                
                # Combine the content of the top results into a single context block
                context = ""
                for res in results:
                    context += f"Source: {res.get('name', 'Unknown')}\n"
                    context += f"{res.get('content', '')}\n\n"
                
                return context
            else:
                return f"Database returned an error: {response.status_code}"
        except Exception as e:
            return f"Failed to connect to skill database: {str(e)}"

