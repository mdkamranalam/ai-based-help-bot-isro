from transformers import pipeline
import json

def load_missions_context():
    """Load mission descriptions from missions.json for LLM context."""
    try:
        with open('missions.json', 'r') as f:
            missions = json.load(f)
        # Concatenate all descriptions for context
        context = "\n".join([f"{m['name']}: {m['description']}" for m in missions])
        return context
    except Exception as e:
        print(f"Error loading missions context: {e}")
        return ""

def llm_answer_query(query):
    """Process a query using DistilBERT question-answering model."""
    try:
        llm_context = load_missions_context()
        if not llm_context:
            return "Error: Could not load mission data."
        
        # Initialize DistilBERT pipeline
        qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        
        # Combine query and context
        input_text = f"Question: {query}\nContext: {llm_context}"
        result = qa_pipeline(question=query, context=llm_context)
        
        return result['answer']
    except Exception as e:
        print(f"LLM processing error: {e}")
        return f"Error processing query: {str(e)}"

if __name__ == "__main__":
    # Test LLM queries
    test_queries = ["What does Chandrayaan-2 do?", "What is lunar?", "What are communication satellites?"]
    for query in test_queries:
        response = llm_answer_query(query)
        print(f"Query: {query}\nResponse: {response}\n")