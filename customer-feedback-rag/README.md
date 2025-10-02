# RAG-based Customer Feedback Analysis System (MVP)

This project is a Minimum Viable Product (MVP) for a customer feedback analysis system that uses Retrieval-Augmented Generation (RAG) to provide conversational insights from customer data. Users can ask questions in natural language and receive synthesized answers based on real feedback, complete with citations to the source data.

## Project Overview

The core of this system is a RAG pipeline that allows users to "talk" to their customer feedback. Instead of manually sifting through thousands of reviews and survey responses, users can ask questions like "What are our enterprise customers complaining about?" or "What new features are startups requesting?" and receive an AI-generated summary grounded in specific feedback entries.

This MVP demonstrates the end-to-end architecture, from data ingestion and embedding to retrieval and AI-powered generation.

## Architecture

The system follows a classic RAG architecture:

1.  **Data Ingestion**: Customer feedback data (from CSV) is loaded, and each entry is converted into a numerical representation (an embedding) using an OpenAI embedding model. These embeddings are stored in a `pgvector`-enabled Supabase PostgreSQL database.
2.  **Retrieval**: When a user asks a question, the query is also converted into an embedding. The system then performs a semantic search (cosine similarity) against the stored feedback embeddings to find the most relevant entries.
3.  **Augmentation**: The top 50 most relevant feedback entries are "augmented" (added) to the user's original query as context.
4.  **Generation**: The combined prompt (query + context) is sent to an OpenAI generation model (GPT-4o-mini). A carefully designed system prompt instructs the model to synthesize an answer based *only* on the provided feedback and to cite the source feedback IDs.
5.  **Streaming & Citation**: The generated answer is streamed back to the user for a real-time chat experience. The cited feedback IDs are extracted and used to display the original feedback entries, providing transparency and trust in the generated answer.

![Architecture Diagram](docs/architecture_diagram.png)
*(Note: The architecture diagram is a placeholder and would be added in a full project.)*

## Tech Stack

-   **Backend**: Python with Flask
-   **Database**: Supabase (PostgreSQL with `pgvector`)
-   **Vector Storage**: `pgvector` for efficient similarity search
-   **Embeddings**: OpenAI `text-embedding-3-small`
-   **LLM**: OpenAI `gpt-4o-mini`
-   **Frontend**: Simple HTML, CSS, and JavaScript

### Why this stack?

-   **Flask**: A lightweight and simple Python framework, perfect for building the API for this MVP.
-   **Supabase & pgvector**: Provides a powerful and scalable PostgreSQL database with the `pgvector` extension out-of-the-box. This allows us to store both our structured data and vector embeddings in the same place, simplifying the architecture.
-   **OpenAI Models**: `text-embedding-3-small` offers a great balance of performance and cost for embeddings, while `gpt-4o-mini` is a fast and capable model for the generation step.
-   **Vanilla JS/CSS/HTML**: Keeps the frontend simple and dependency-free, focusing on the core functionality.

## Setup and Installation

Follow these steps to get the application running locally.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd customer-feedback-rag
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root by copying the example file:

```bash
cp .env.example .env
```

Now, edit the `.env` file and add your credentials:

```
SUPABASE_URL="your-supabase-url"
SUPABASE_SERVICE_KEY="your-supabase-service-key"
OPENAI_API_KEY="your-openai-api-key"
```

-   `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`: Find these in your Supabase project dashboard under **Project Settings > API**. Use the `service_role` key for backend operations.
-   `OPENAI_API_KEY`: Your API key from the OpenAI platform.

### 5. Set Up the Database Schema

The database schema needs to be created in your Supabase project.

1.  Navigate to the **SQL Editor** in your Supabase dashboard.
2.  Run the following command to get the required SQL:

    ```bash
    python scripts/setup_database.py
    ```

3.  Copy the SQL output from the command and run it in the Supabase SQL Editor. This will create the `feedback` table and a database function for semantic search.

### 6. Ingest the Data

With the database set up, you can now ingest the sample data. This script will read the sample CSV, generate embeddings for each entry, and upload them to your Supabase table.

```bash
python scripts/ingest_data.py
```

## How to Run Locally

Once the setup is complete, you can run the Flask application:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`. Open this URL in your web browser.

## Example Queries to Try

-   "What are customers saying about integrations?"
-   "Show me churn risks in the enterprise segment"
-   "What features are SMB customers requesting most?"
-   "How has sentiment changed in the past 30 days?"
-   "What are the top 3 pain points mentioned in reviews?"

## Cost Considerations

-   **OpenAI API**: The primary cost will be from the OpenAI API for generating embeddings and chat completions.
    -   `text-embedding-3-small` is very cost-effective.
    -   `gpt-4o-mini` is used for generation to keep costs lower than larger models like GPT-4.
-   **Supabase**: The free tier of Supabase should be sufficient for this MVP, but costs may increase with larger datasets and higher traffic.

## Future Improvements

-   **Real-time Data Ingestion**: Instead of a manual script, use Supabase webhooks or a message queue to ingest new feedback in real-time.
-   **More Advanced Retrieval**: Implement a more sophisticated retrieval strategy, such as using a hybrid search that combines semantic search with keyword-based search.
-   **User Authentication**: Add user accounts to save conversation history.
-   **Frontend Enhancements**: Use a modern frontend framework like React or Vue.js to build a more dynamic and feature-rich interface.
-   **Metadata Filtering**: Allow users to filter feedback by customer segment, date range, or rating before asking a question.
-   **Automated Insights**: Create a dashboard that proactively surfaces key themes and trends without requiring a user to ask a question.