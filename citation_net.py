import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import ast

def create_citation_network(file_path):
    """
    Reads case law and IPC section citation data from a file and generates a citation network.
    
    Parameters:
    file_path (str): Path to the CSV file containing extracted citation data.
    
    Returns:
    networkx.DiGraph: The constructed citation network graph.
    """
    
    # Load data from the file (assuming CSV format with 'Case Law' and 'Referenced IPC Sections' columns)
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
    
    # Validate column names
    if "Case Law" not in df.columns or "Referenced IPC Sections" not in df.columns:
        print("Error: CSV file must contain 'Case Law' and 'Referenced IPC Sections' columns.")
        return None
    
    # Debugging: Check if the data is loaded correctly
    print("Sample Data:")
    print(df.head())
    
    # Create a Directed Graph
    G = nx.DiGraph()
    
    # Add nodes and edges
    for index, row in df.iterrows():
        case = row["Case Law"]
        try:
            sections = ast.literal_eval(row["Referenced IPC Sections"]) if isinstance(row["Referenced IPC Sections"], str) else row["Referenced IPC Sections"]
        except (ValueError, SyntaxError):
            print(f"Skipping row {index} due to incorrect format in 'Referenced IPC Sections'")
            continue
        
        G.add_node(case, type="case")
        for sec in sections:
            G.add_node(sec, type="section")
            G.add_edge(case, sec)  # Case law cites the IPC section
    
    # Debugging: Check if nodes and edges are added
    print(f"Nodes: {len(G.nodes())}, Edges: {len(G.edges())}")
    
    # Plot the Graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)  # Layout for better visualization
    node_colors = ["lightblue" if G.nodes[n]["type"] == "case" else "lightcoral" for n in G.nodes]
    
    nx.draw(G, pos, with_labels=True, node_size=2500, node_color=node_colors, font_size=8, edge_color="gray")
    
    # Display the graph
    plt.title("Citation Network from Extracted Data")
    plt.show(block=True)  # Ensure the plot doesn't disappear
    
    return G


if __name__ == "__main__":
    # Define the path to the citation data file
    file_path = "sample_citation_data.csv"  # Update with the actual file path
    
    # Generate the citation network
    citation_graph = create_citation_network(file_path)
    
    # Save the graph if needed
    if citation_graph:
        nx.write_gpickle(citation_graph, "citation_network.gpickle")
        print("Citation network saved as 'citation_network.gpickle'")
