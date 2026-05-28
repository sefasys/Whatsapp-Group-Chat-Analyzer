import networkx as nx
from collections import Counter
from typing import Dict

class NetworkAnalyzer:
    def __init__(self, reply_network: Dict[str, Counter], all_user_ids: list[str] = None):
        self.reply_network = reply_network
        self.all_user_ids = all_user_ids
        self.graph = self.build_interaction_graph()

    def build_interaction_graph(self) -> nx.DiGraph:
        """
        Builds a directed graph from the reply network.
        Nodes are users, edges indicate a reply from sender to receiver.
        Edge weight is the frequency of replies.
        """
        G = nx.DiGraph()
        
        if self.all_user_ids:
            G.add_nodes_from(self.all_user_ids)
            
        for sender, receivers in self.reply_network.items():
            for receiver, count in receivers.items():
                if count > 0:
                    G.add_edge(sender, receiver, weight=count)
                    
        return G

    def compute_centrality_scores(self) -> Dict[str, Dict[str, float]]:
        """
        Computes network centrality metrics:
        - Degree Centrality: Overall involvement
        - Betweenness Centrality: Bridge or broker roles
        - PageRank: Influence or importance
        """
        if len(self.graph) == 0:
            return {}

        degree = nx.degree_centrality(self.graph)
        betweenness = nx.betweenness_centrality(self.graph, weight='weight')
        pagerank = nx.pagerank(self.graph, weight='weight')

        scores = {}
        for node in self.graph.nodes():
            scores[node] = {
                "degree_centrality": degree.get(node, 0.0),
                "betweenness_centrality": betweenness.get(node, 0.0),
                "pagerank": pagerank.get(node, 0.0)
            }
            
        return scores

    def export_graph_json(self) -> dict:
        return {
            "nodes": [
                {"id": str(n), "label": str(n), "weight": self.graph.degree(n)}
                for n in self.graph.nodes()
            ],
            "edges": [
                {"source": str(u), "target": str(v), "weight": d.get("weight", 1)}
                for u, v, d in self.graph.edges(data=True)
            ]
        }

    def detect_subgroups(self) -> list[list[str]]:
        """Detects closely communicating subgroups using weakly connected components."""
        if len(self.graph) == 0:
            return []
        return [list(c) for c in nx.weakly_connected_components(self.graph)]

    def compute_influence_score(self) -> Dict[str, float]:
        """Calculates a composite influence score for users."""
        scores = self.compute_centrality_scores()
        influence = {}
        for node, s in scores.items():
            influence[node] = (s["degree_centrality"] + s["pagerank"]) / 2
        return influence

def run_dummy_test():
    """Testing with 5 user dummy data"""
    dummy_data = {
        "User_A": Counter({"User_B": 5, "User_C": 2}),
        "User_B": Counter({"User_A": 3, "User_D": 10}),
        "User_C": Counter({"User_A": 1, "User_E": 4}),
        "User_D": Counter({"User_B": 8, "User_E": 1}),
        "User_E": Counter({"User_C": 5})
    }
    
    analyzer = NetworkAnalyzer(dummy_data)
    scores = analyzer.compute_centrality_scores()
    
    print("Dummy Network Test Results:")
    for user, metrics in scores.items():
        print(f"{user}:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")

if __name__ == "__main__":
    run_dummy_test()
