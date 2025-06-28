import spacy

def process_query(query):
    # Load SpaCy model
    nlp = spacy.load("en_core_web_sm")
    
    # Process query
    doc = nlp(query)
    
    # Extract entities (e.g., mission names like "INSAT-3DR")
    entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "GPE"]]
    
    # Return the most relevant entity or the original query
    return entities[0] if entities else query

if __name__ == "__main__":
    # Test NLP
    test_query = "What is INSAT-3DR?"
    processed = process_query(test_query)
    print(f"Original: {test_query}, Processed: {processed}")