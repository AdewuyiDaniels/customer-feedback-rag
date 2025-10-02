document.addEventListener("DOMContentLoaded", () => {
    const queryInput = document.getElementById("query-input");
    const sendButton = document.getElementById("send-button");
    const chatContainer = document.getElementById("chat-container");
    const citationsContainer = document.getElementById("citations-container");
    const citationsContent = document.getElementById("citations-content");

    const handleQuery = async () => {
        const query = queryInput.value.trim();
        if (!query) return;

        // Clear input and display user message
        queryInput.value = "";
        addMessage(query, "user");

        // Add loading indicator
        const loadingIndicator = addMessage("", "ai", true);

        // Clear previous citations
        citationsContent.innerHTML = "";
        citationsContainer.style.display = "none";

        try {
            const response = await fetch("/api/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Process the streamed response
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let fullResponse = "";

            // Remove loading indicator and create a new message element for the AI
            loadingIndicator.remove();
            const aiMessageElement = addMessage("", "ai");

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                fullResponse += decoder.decode(value, { stream: true });

                // Check for the special citation token
                if (fullResponse.includes("<<CITATIONS:")) {
                    const parts = fullResponse.split("<<CITATIONS:");
                    aiMessageElement.innerHTML = parts[0]; // Display the main text

                    const citationData = parts[1].replace(">>", "");
                    const citedIds = JSON.parse(citationData);

                    await displayCitations(citedIds);
                    break; // Stop processing the stream
                } else {
                    aiMessageElement.innerHTML = fullResponse; // Update AI message as it streams
                }
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

        } catch (error) {
            console.error("Error fetching AI response:", error);
            const errorElement = document.querySelector('.loading-indicator')?.parentElement || addMessage("", "ai");
            errorElement.innerHTML = "Sorry, something went wrong. Please try again.";
        }
    };

    const displayCitations = async (ids) => {
        if (ids.length === 0) return;

        citationsContainer.style.display = "block";
        citationsContent.innerHTML = ""; // Clear previous citations

        for (const id of ids) {
            try {
                const response = await fetch(`/api/feedback/${id}`);
                if (response.ok) {
                    const feedback = await response.json();
                    const citationElement = document.createElement("div");
                    citationElement.classList.add("citation-item");
                    citationElement.innerHTML = `
                        <p class="header">Feedback ID: ${feedback.feedback_id} (Rating: ${feedback.rating})</p>
                        <p>${feedback.feedback_text}</p>
                    `;
                    citationsContent.appendChild(citationElement);
                }
            } catch (error) {
                console.error(`Error fetching citation for ID ${id}:`, error);
            }
        }
    };

    const addMessage = (text, sender, isLoading = false) => {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message", `${sender}-message`);

        if (isLoading) {
            messageElement.classList.add("loading-indicator");
            messageElement.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        } else {
            messageElement.textContent = text;
        }

        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return messageElement;
    };

    sendButton.addEventListener("click", handleQuery);
    queryInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleQuery();
        }
    });

    // Add a welcome message
    addMessage("Hello! How can I help you analyze the customer feedback today?", "ai");
});