formatted for clarity:

# Customer Feedback RAG System

A Retrieval-Augmented Generation (RAG) system that transforms how teams analyze customer feedback. Query thousands of reviews and survey responses conversationally, and get insights in seconds.

---

## 🚨 The Problem

Traditional feedback analysis is too slow. By the time you export data to Excel and run sentiment analysis, customer needs have already shifted.  

Product teams need to quickly answer questions like:
- What's driving churn in our enterprise segment?
- Which feature requests keep appearing?
- How has sentiment changed in the last 30 days?

This system makes that possible.

---

## ⚙️ How It Works

### **Storage Layer**
- Customer reviews and survey responses stored in **Supabase**
- Vector embeddings generated using **OpenAI `text-embedding-3-small`**
- **PostgreSQL + pgvector** for fast similarity search

### **Retrieval Strategy**
1. User query converted to an embedding  
2. Semantic search retrieves top **50 relevant feedback entries**  
3. Results include metadata (customer segment, rating, date)  

### **Generation Layer**
- **GPT-4o-mini** processes retrieved context  
- Generates **grounded insights with citations**  
- Streams responses in real-time  
- Full conversation history saved for audit  

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask  
- **Database**: Supabase (PostgreSQL + pgvector)  
- **Embeddings**: OpenAI `text-embedding-3-small`  
- **LLM**: OpenAI `gpt-4o-mini`  
- **Frontend**: HTML, CSS, JavaScript  

---

## 🚀 Setup Instructions

### **Prerequisites**
- Python 3.9+  
- Supabase account  
- OpenAI API key  

### **Installation**
```bash
# Clone the repository
git clone https://github.com/yourusername/customer-feedback-rag.git
cd customer-feedback-rag

# Install dependencies
pip install -r requirements.txt

````

Environment Variables

Create a .env file in the root directory:
```bash
OPENAI_API_KEY=your_openai_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
```

Database Setup
```bash
python scripts/setup_database.py

```

Generate & Ingest Data
```bash
python scripts/generate_sample_data.py
python scripts/ingest_data.py

```
Run the Application
```bash
python app.py

```

Open your browser at: http://localhost:5000

💡 Example Queries

Try asking:

"What are customers saying about integrations?"

"Show me churn risks in the enterprise segment"

"What features are SMB customers requesting most?"

"How has sentiment changed in the past 30 days?"

"What are the top 3 pain points in reviews?"

### **📂 Project Structure**
```bash
customer-feedback-rag/
├── app.py                   # Flask application
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── scripts/
│   ├── setup_database.py    # Database schema setup
│   ├── generate_sample_data.py
│   └── ingest_data.py
├── modules/
│   ├── embeddings.py        # Embedding logic
│   ├── retrieval.py         # Semantic search
│   └── generation.py        # LLM response generation
├── static/
│   ├── style.css
│   └── app.js
├── templates/
│   └── index.html           # Chat interface
├── data/
│   └── sample_feedback.csv
└── docs/
    ├── ARCHITECTURE.md
    └── architecture_diagram.png

```

## 🧠 Architecture Decisions

Why RAG Over Fine-Tuning?

        Cost: No expensive retraining, only embeddings + inference
        
        Flexibility: Add new feedback without retraining
        
        Transparency: Every answer cites sources
        
        Speed: Insights in <10s vs weeks of fine-tuning

Embedding Strategy

    Using OpenAI text-embedding-3-small because:
    
        1536 dimensions → balance accuracy & storage
        
        $0.02 / 1M tokens (very cost-effective)
        
        Strong semantic similarity performance

Cost Optimization

    Embeddings:
    
            1,000 feedback entries ≈ 500K tokens
            
            Cost: ~$0.01 per 1,000 entries
    
    Queries:
    
            ~50 feedback items / query (~10K tokens)
            
            GPT-4o-mini: $0.15 per 1M tokens
            
            Cost per query: ~$0.0015

👉 MVP cost: <$5 for 1,000 entries & 100 queries

## 📈 Scalability & Performance

###Current MVP

        Handles up to 10K feedback entries
        
        Query response: <10 seconds
        
        Single server deployment

### Scaling to Production

        Query result caching (Redis)
        
        Pagination for large results
        
        Supabase connection pooling
        
        Consider Pinecone/Weaviate for 100K+ entries

### Benchmarks (1K entries)

        Embedding generation: 2.5s per 100 entries
        
        Query response: 6–8s average
        
        Retrieval accuracy: 87% relevant results in top 50
        
        Query cost: $0.0015

### 🔮 Future Improvements

         1. Query result caching
        
         2. User authentication
        
         3.  Analytics dashboard
        
         4. Export to PDF/CSV
        
         5. Multi-language support
        
         6. Sentiment trend visualization
        
         7. Automated categorization
        
         8.Slack/Teams integration

### 🤝 Contributing

This is a proof of concept project. Fork and adapt it for your use case.
Found a bug or have suggestions? Open an issue.

### 📜 License

MIT License – free to use and adapt.

👤 Author

Abayomi Adewuyi Daniel
Product Manager | 5+ years building AI & IoT systems
Connect on LinkedIn
