import os
import re
from openai import OpenAI
from dotenv import load_dotenv

def generate_response(query: str, retrieved_feedback: list):
    """
    Generates a response using an LLM based on the user's query and retrieved feedback.
    Streams the response and extracts cited feedback IDs.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    # Format the retrieved feedback for the prompt
    context = "\n---\n".join(
        [
            f"Feedback ID: {item['feedback_id']}\n"
            f"Customer Segment: {item['customer_segment']}\n"
            f"Rating: {item['rating']}\n"
            f"Feedback Text: {item['feedback_text']}"
            for item in retrieved_feedback
        ]
    )

    system_prompt = """
    You are an AI assistant for a customer feedback analysis system. Your role is to provide clear, concise, and data-driven insights based on customer feedback.

    - **Ground your answers in the provided context.** The context contains customer feedback entries with their IDs, customer segments, ratings, and text.
    - **Do not make up information.** If the provided feedback does not contain the answer, state that clearly.
    - **Cite your sources.** When you use information from a feedback entry, you MUST cite it by including its ID in the format `[feedback_id: <ID>]` at the end of the sentence or claim. For example: 'Some users are requesting a mobile app [feedback_id: 42].'
    - **Synthesize information.** Do not just list feedback. Summarize the key themes, trends, and sentiment.
    - **Be direct.** Answer the user's query directly.
    """

    user_prompt = f"""
    User Query: "{query}"

    Relevant Customer Feedback:
    ---
    {context}
    ---

    Based on the provided feedback, please answer the user's query.
    """

    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
        )

        full_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            full_response += content
            yield content

        # Extract cited feedback IDs after streaming is complete
        cited_ids = re.findall(r'\[feedback_id:\s*(\d+)\]', full_response)
        # Return a list of unique integer IDs
        unique_ids = list(set(int(id) for id in cited_ids))

        # Yield a special token to signal the end of the text stream and to send the citations
        yield f"\n<<CITATIONS:{unique_ids}>>"

    except Exception as e:
        print(f"An error occurred during response generation: {e}")
        yield "Sorry, I encountered an error while generating the response."
        yield f"\n<<CITATIONS:[]>>"