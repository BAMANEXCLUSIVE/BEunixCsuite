import matplotlib.pyplot as plt
import networkx as nx

# Define the main organization structure
class Organization:
    def __init__(self):
        self.structure = {
            "CEO": {
                "Finance Group Functionality": {},
                "Operation Group Functionality": {},
                "Sales and Marketing Group Functionality": {},
                "Risk Management Group Functionality": {},
                "Research and Development Group Functionality": {},
                "Auditing Group Functionality": {},
                "Social Responsibility Group Functionality": {}
            }
        }

    def add_suborganization(self, parent, child):
        """Add a sub-organization under a parent."""
        if parent in self.structure:
            self.structure[parent][child] = {}
        else:
            print(f"Parent {parent} not found.")

    def visualize(self):
        """Visualize the organization structure."""
        G = nx.DiGraph()  # Directed graph

        # Recursive function to add nodes and edges to the graph
        def add_edges(parent, children):
            for child in children:
                G.add_edge(parent, child)
                add_edges(child, self.structure[parent][child])

        # Start adding edges from the CEO
        for sub_org in self.structure["CEO"]:
            G.add_edge("CEO", sub_org)
            add_edges(sub_org, self.structure["CEO"][sub_org])

        # Draw the graph
        pos = nx.spring_layout(G)  # positions for all nodes
        nx.draw(G, pos, with_labels=True, arrows=True)
        plt.title("Organization Structure")
        plt.show()

# Create an instance of the organization
org = Organization()

# Example of detecting new functionalities (simulated)
detected_functionalities = [
    "Finance Group Functionality",
    "Operation Group Functionality",
    "Sales and Marketing Group Functionality",
    "Risk Management Group Functionality",
    "Research and Development Group Functionality",
    "Auditing Group Functionality",
    "Social Responsibility Group Functionality"
]

# Logic to check for new functionalities (for demonstration)
existing_functionalities = org.structure["CEO"].keys()
for functionality in detected_functionalities:
    if functionality not in existing_functionalities:
        org.add_suborganization("CEO", functionality)

# Visualize the organization structure
org.visualize()