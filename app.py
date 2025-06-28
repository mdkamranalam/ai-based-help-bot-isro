from flask import Flask, request, render_template
from knowledge_graph import create_knowledge_graph, query_knowledge_graph
from nlp_processor import process_query
from llm_processor import load_missions_context, llm_answer_query

app = Flask(__name__)

# Initialize knowledge graph, LLM context, and cache
kg = None
llm_context = None
llm_cache = {}  # Cache for LLM responses

def initialize_knowledge_graph_and_context():
    global kg, llm_context
    kg = create_knowledge_graph()
    llm_context = load_missions_context()
    return kg, llm_context

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global kg, llm_context, llm_cache
    user_query = request.form.get('query', '').strip()
    if not user_query:
        return "Please enter a valid query."
    
    # Process query with NLP
    processed_query = process_query(user_query)
    
    # Query knowledge graph first
    results = query_knowledge_graph(kg, processed_query)
    
    # Format response from knowledge graph if results exist
    if results:
        response = "<br>".join([f"<b>{r['name']}</b>: Launched on {r['date']}. {r['description']}" for r in results])
    else:
        # Check cache for LLM response
        if user_query in llm_cache:
            response = f"LLM Answer: {llm_cache[user_query]}"
        else:
            # Fallback to LLM
            llm_response = llm_answer_query(user_query, llm_context)
            llm_cache[user_query] = llm_response
            response = f"LLM Answer: {llm_response}"
    
    return response

if __name__ == "__main__":
    initialize_knowledge_graph_and_context()
    app.run(debug=True)