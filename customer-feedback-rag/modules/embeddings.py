import os
from openai import OpenAI
from dotenv import load_dotenv

def get_embedding(text, model="text-embedding-3-small"):
    """
    Generates an embedding for the given text using the specified OpenAI model.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"An error occurred while generating embedding: {e}")
        return None