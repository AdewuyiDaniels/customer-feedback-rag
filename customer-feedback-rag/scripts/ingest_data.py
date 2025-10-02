import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
from tqdm import tqdm
import sys

# Add the parent directory to the Python path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.embeddings import get_embedding

def ingest_data():
    """
    Reads feedback data from a CSV file, generates embeddings,
    and ingests the data into the Supabase 'feedback' table.
    """
    load_dotenv()

    # Supabase client setup
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    if not supabase_url or not supabase_key:
        print("Error: Supabase environment variables not set.")
        return
    supabase: Client = create_client(supabase_url, supabase_key)

    # Load data
    try:
        df = pd.read_csv("data/sample_feedback.csv")
    except FileNotFoundError:
        print("Error: 'data/sample_feedback.csv' not found. Please generate it first.")
        return

    print(f"Starting ingestion of {len(df)} feedback entries...")

    # Ingest data in batches
    batch_size = 50
    for i in tqdm(range(0, len(df), batch_size), desc="Ingesting data"):
        batch = df.iloc[i:i+batch_size]
        records_to_insert = []

        for index, row in batch.iterrows():
            # Generate embedding
            text_to_embed = f"Segment: {row['customer_segment']}, Rating: {row['rating']}, Feedback: {row['feedback_text']}"
            embedding = get_embedding(text_to_embed)

            if embedding:
                records_to_insert.append({
                    "feedback_id": int(row["feedback_id"]),
                    "customer_segment": row["customer_segment"],
                    "feedback_text": row["feedback_text"],
                    "rating": int(row["rating"]),
                    "feedback_date": row["date"],
                    "source_type": row["source_type"],
                    "embedding": embedding,
                })

        if records_to_insert:
            try:
                supabase.table("customer_feedback").upsert(records_to_insert).execute()
            except Exception as e:
                print(f"\nAn error occurred during batch insertion: {e}")

    print("Data ingestion complete.")

if __name__ == "__main__":
    ingest_data()