from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, DCTERMS
import json
import uuid
import networkx as nx
import matplotlib.pyplot as plt

# Define custom namespace for ISRO mission types
ISRO = "http://example.org/isro/"
MISSION_TYPE = URIRef(ISRO + "missionType")

def create_knowledge_graph():
    """Create a knowledge graph from missions.json with mission types."""
    kg = Graph()
    
    try:
        with open('missions.json', 'r') as f:
            missions = json.load(f)
    except FileNotFoundError:
        print("missions.json not found. Creating empty graph.")
        return kg
    except json.JSONDecodeError:
        print("Invalid JSON format in missions.json.")
        return kg

    # Define mission types based on description keywords
    def get_mission_type(description):
        description = description.lower()
        if any(keyword in description for keyword in ["lunar", "moon", "south pole"]):
            return Literal("Lunar")
        elif any(keyword in description for keyword in ["mars", "martian"]):
            return Literal("Interplanetary")
        elif any(keyword in description for keyword in ["solar", "sun"]):
            return Literal("Solar")
        elif any(keyword in description for keyword in ["communication", "telecom", "broadcasting", "transponders"]):
            return Literal("Communication")
        elif any(keyword in description for keyword in ["weather", "meteorological", "cyclone", "monsoon"]):
            return Literal("Meteorological")
        elif any(keyword in description for keyword in ["radar", "surveillance"]):
            return Literal("Radar Imaging")
        elif any(keyword in description for keyword in ["earth observation", "mapping", "cartography"]):
            return Literal("Earth Observation")
        elif any(keyword in description for keyword in ["navigation", "gps", "navic"]):
            return Literal("Navigation")
        elif any(keyword in description for keyword in ["x-ray", "astronomy", "black holes"]):
            return Literal("Astronomy")
        else:
            return Literal("Other")

    # Populate graph
    for mission in missions:
        mission_uri = URIRef(ISRO + str(uuid.uuid4()))
        kg.add((mission_uri, RDF.type, FOAF.Project))
        kg.add((mission_uri, DCTERMS.title, Literal(mission["name"])))
        kg.add((mission_uri, DCTERMS.date, Literal(mission["date"])))
        kg.add((mission_uri, DCTERMS.description, Literal(mission["description"])))
        mission_type = get_mission_type(mission["description"])
        kg.add((mission_uri, MISSION_TYPE, mission_type))

    # Save graph for debugging
    try:
        kg.serialize("isro_knowledge_graph.ttl", format="turtle")
    except Exception as e:
        print(f"Error serializing graph: {e}")

    # Visualize the graph
    visualize_graph(kg)

    return kg

def query_knowledge_graph(kg, query):
    """Query the knowledge graph for missions matching the query in name, description, or type."""
    q = f"""
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX isro: <{ISRO}>
        SELECT ?name ?date ?description ?type
        WHERE {{
            ?mission a foaf:Project ;
                     dct:title ?name ;
                     dct:date ?date ;
                     dct:description ?description ;
                     isro:missionType ?type .
            FILTER (
                regex(str(?name), "{query}", "i") ||
                regex(str(?description), "{query}", "i") ||
                regex(str(?type), "{query}", "i")
            )
        }}
    """
    try:
        results = kg.query(q)
        return [{"name": str(row.name), "date": str(row.date), "description": str(row.description), "type": str(row.type)} for row in results]
    except Exception as e:
        print(f"SPARQL query error: {e}")
        return []

def visualize_graph(kg):
    """Generate a NetworkX/Matplotlib diagram of the knowledge graph."""
    try:
        # Create a NetworkX graph
        G = nx.DiGraph()
        
        # Add nodes and edges from RDF triples
        for s, p, o in kg:
            # Simplify labels for readability
            subject_label = str(s).split('/')[-1][:10]  # Shorten mission URI
            object_label = str(o)[:20] if isinstance(o, Literal) else str(o).split('/')[-1]  # Shorten literals
            predicate_label = str(p).split('/')[-1].split('#')[-1]  # e.g., "missionType"

            # Add nodes
            G.add_node(subject_label, shape='ellipse')
            G.add_node(object_label, shape='box' if isinstance(o, Literal) else 'ellipse')
            
            # Add edge
            G.add_edge(subject_label, object_label, label=predicate_label)

        # Set up plot
        plt.figure(figsize=(18, 14))  # Adjusted for 25 missions
        pos = nx.spring_layout(G, k=0.15, iterations=50)  # Adjusted layout

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_shape='o', node_color='lightblue', node_size=600)
        nx.draw_networkx_nodes(G, pos, nodelist=[n for n, attr in G.nodes(data=True) if attr.get('shape') == 'box'], 
                              node_shape='s', node_color='lightgreen', node_size=400)

        # Draw edges
        nx.draw_networkx_edges(G, pos)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=6)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5)

        # Save and close plot
        output_file = 'static/isro_knowledge_graph.png'
        plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Graph visualization saved as {output_file}")
    except Exception as e:
        print(f"Error visualizing graph: {e}")

if __name__ == "__main__":
    # Test the knowledge graph
    kg = create_knowledge_graph()
    test_queries = ["Chandrayaan", "lunar", "communication", "failed missions"]
    for query in test_queries:
        results = query_knowledge_graph(kg, query)
        print(f"Query: {query}\nResults: {results}\n")