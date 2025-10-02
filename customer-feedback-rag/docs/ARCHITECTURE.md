# System Architecture

This document provides a detailed explanation of the architectural decisions made in this RAG-based customer feedback analysis system.

## System Design Decisions

The architecture was designed to be simple, modular, and scalable, making it suitable for an MVP while laying the groundwork for future expansion.

-   **Monolithic Backend (for now)**: A single Flask application serves both the API and the frontend. For an MVP, this is simpler to develop, deploy, and manage than a microservices architecture. As the system grows, the API could be separated into its own service.
-   **Centralized Database**: Using Supabase (PostgreSQL) as a single database for both structured feedback data and vector embeddings simplifies the data management process. It avoids the need for a separate, dedicated vector database, which reduces complexity and operational overhead.
-   **Stateless API**: The API is stateless. Each query is self-contained, which makes the backend easy to scale horizontally by simply adding more instances of the Flask application.
-   **Client-Side State**: The frontend is responsible for managing the conversation state (the history of messages). This is a common pattern in modern web applications and simplifies the backend.

## Why RAG over Fine-Tuning?

Retrieval-Augmented Generation (RAG) was chosen over fine-tuning a large language model (LLM) for several key reasons:

1.  **Reduces Hallucinations**: Fine-tuning can teach a model a certain style or domain knowledge, but it doesn't prevent it from "hallucinating" or making up facts. RAG grounds the model's response in real, retrieved data, making the answers more factual and trustworthy.
2.  **Data Freshness**: RAG allows the system to use the most up-to-date information without needing to retrain the model. As soon as new feedback is ingested and embedded, it becomes available for retrieval. Fine-tuning, on the other hand, is a static process; the model only knows what it was trained on.
3.  **Transparency and Citations**: With RAG, we can easily cite the specific feedback entries used to generate an answer. This is crucial for building user trust, as it allows them to verify the AI's claims by looking at the source data. This is very difficult to achieve with a fine-tuned model.
4.  **Cost-Effectiveness**: Fine-tuning LLMs can be expensive and time-consuming. A RAG system is generally cheaper to build and maintain, as the primary cost is the API calls for embeddings and generation, which are pay-as-you-go.

## Embedding Strategy

-   **Model**: We use OpenAI's `text-embedding-3-small` model. It was chosen because it provides a strong balance between performance (quality of embeddings) and cost. It's one of the best-performing models on the [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard) and is significantly cheaper than larger models.
-   **Content to Embed**: We embed a combination of the feedback text and key metadata (`Customer Segment` and `Rating`). This enriches the embedding with important context, allowing for more nuanced retrieval. For example, a search for "unhappy enterprise users" can leverage both the sentiment in the text and the customer segment metadata.

## Retrieval Optimization Approach

-   **Database**: `pgvector` on Supabase provides an indexed and efficient way to perform cosine similarity searches. For the scale of this MVP, it is more than sufficient.
-   **Database Function**: We created a PostgreSQL function (`match_feedback`) to handle the similarity search on the database side. This is more efficient than pulling all embeddings into the application and performing the calculation in Python.
-   **Top-K Retrieval**: We retrieve the top 50 most relevant documents (`match_count = 50`). This is a common starting point and provides enough context for the LLM to generate a comprehensive answer without being overwhelmed. The `match_threshold` is also used to filter out irrelevant results.

## Cost vs. Accuracy Tradeoffs

-   **Models**: We are using `gpt-4o-mini` for the generation step. It's significantly faster and cheaper than `gpt-4` or `gpt-4o`, which is ideal for an MVP. While a more powerful model might provide slightly more nuanced summaries, `gpt-4o-mini` is more than capable for this task, especially with a well-designed prompt.
-   **Context Window**: We are limiting the context to the top 50 retrieved documents. This helps keep the cost of each API call down and fits comfortably within the context window of `gpt-4o-mini`. For more complex queries, a larger context window (and a model that supports it) might be necessary, but this would increase costs.

## Scalability Considerations

-   **Stateless Backend**: The Flask API can be scaled horizontally behind a load balancer to handle increased traffic.
-   **Database**: Supabase is built on AWS and can scale to handle very large datasets. As the `feedback` table grows, we may need to upgrade our Supabase plan and fine-tune the `pgvector` index for optimal performance.
-   **Data Ingestion**: The current data ingestion is a manual script. For a production system, this would be replaced with a more robust, scalable solution, such as a message queue (e.g., RabbitMQ, SQS) and a fleet of worker processes to handle embedding and ingestion in real-time.
-   **LLM Provider**: The system is modular, so the LLM provider can be swapped out if needed. If OpenAI API costs become a concern, we could switch to a different provider or even a self-hosted open-source model.