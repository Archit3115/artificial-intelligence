"""Generate a simple architecture diagram for VoiceX.

This script builds a directed graph representing components
and renders it using networkx + matplotlib.

Usage:
    python -m src.voicex_architecture
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx


def build_voicex_graph() -> nx.DiGraph:
    G = nx.DiGraph()
    # Components
    components = [
        "User",
        "Client App",
        "API Gateway",
        "Auth Service",
        "Voice Processing",
        "NLP Service",
        "Dialogue Manager",
        "TTS Service",
        "Storage",
        "Monitoring",
    ]
    G.add_nodes_from(components)

    # Edges (simplified)
    edges = [
        ("User", "Client App"),
        ("Client App", "API Gateway"),
        ("API Gateway", "Auth Service"),
        ("API Gateway", "Voice Processing"),
        ("Voice Processing", "NLP Service"),
        ("NLP Service", "Dialogue Manager"),
        ("Dialogue Manager", "TTS Service"),
        ("TTS Service", "Client App"),
        ("Dialogue Manager", "Storage"),
        ("Voice Processing", "Monitoring"),
    ]
    G.add_edges_from(edges)
    return G


def draw_graph(G: nx.DiGraph, filename: str | None = None) -> None:
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, node_size=1200, node_color="#A3C1DA")
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=16)
    nx.draw_networkx_labels(G, pos, font_size=10)
    plt.title("VoiceX Architecture (simplified)")
    plt.axis("off")
    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=150)
        print(f"Saved diagram to {filename}")
    else:
        plt.show()


def main() -> None:
    G = build_voicex_graph()
    draw_graph(G, filename="voicex_architecture.png")


if __name__ == "__main__":
    main()
