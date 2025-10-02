import os
from flask import Flask, request, jsonify, render_template, Response
from dotenv import load_dotenv
from supabase import create_client, Client
import sys

# Add the modules directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from modules.retrieval import retrieve_feedback
from modules.generation import generate_response

load_dotenv()

app = Flask(__name__)

# Supabase client setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
if not supabase_url or not supabase_key:
    raise ValueError("Supabase environment variables not set.")
supabase: Client = create_client(supabase_url, supabase_key)

@app.route("/")
def index():
    """Serves the main HTML page."""
    return render_template("index.html")

@app.route("/api/query", methods=["POST"])
def handle_query():
    """
    Handles user queries by retrieving relevant feedback and generating a response.
    Streams the response back to the client.
    """
    data = request.json
    query = data.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400

    # 1. Retrieval
    retrieved_context = retrieve_feedback(query)
    if not retrieved_context:
        return jsonify({"error": "Could not retrieve relevant feedback."}), 500

    # 2. Generation (with streaming)
    def stream_response():
        # The generator function yields chunks of the response
        for chunk in generate_response(query, retrieved_context):
            yield chunk

    return Response(stream_response(), mimetype="text/plain")

@app.route("/api/feedback/<int:feedback_id>", methods=["GET"])
def get_feedback_by_id(feedback_id):
    """
    Retrieves a specific feedback entry by its ID.
    """
    try:
        response = supabase.table("customer_feedback").select("*").eq("feedback_id", feedback_id).single().execute()
        if response.data:
            return jsonify(response.data)
        else:
            return jsonify({"error": "Feedback not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)