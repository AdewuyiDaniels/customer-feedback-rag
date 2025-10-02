import os
from supabase import create_client, Client
from dotenv import load_dotenv
import sys

# Add the parent directory to the Python path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.embeddings import get_embedding

def retrieve_feedback(query: str, match_threshold: float = 0.78, match_count: int = 50):
    """
    Retrieves relevant feedback from the database based on a user query.
    """
    load_dotenv()

    # Supabase client setup
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    if not supabase_url or not supabase_key:
        print("Error: Supabase environment variables not set.")
        return None
    supabase: Client = create_client(supabase_url, supabase_key)

    # Get query embedding
    query_embedding = get_embedding(query)
    if not query_embedding:
        return None

    # Call the database function
    try:
        response = supabase.rpc(
            "match_feedback",
            {
                "query_embedding": query_embedding,
                "match_threshold": match_threshold,
                "match_count": match_count,
            },
        ).execute()
        return response.data
    except Exception as e:
        print(f"An error occurred during feedback retrieval: {e}")
        return None