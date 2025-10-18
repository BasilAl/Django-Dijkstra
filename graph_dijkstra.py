from __future__ import annotations

from typing import Optional, Dict, List

from pydantic import BaseModel, Field


class Node(BaseModel):
    name: str
    distance: float = Field(default=float("inf"))
    previous: Optional[Node] = None

    def __lt__(self, other: Node) -> bool:
        """Comparison method for priority queue."""
        return self.distance < other.distance

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        return False

    def __repr__(self):
        return f"Node(name={self.name}, distance={self.distance}, previous={self.previous.name if self.previous else None})"


class Vertex(BaseModel):
    source: Node
    destination: Node
    mode: str
    cost: float = Field(default=float("inf"))
    time: float = Field(default=float("inf"))

    def __repr__(self):
        return f"Vertex(source={self.source}, destination={self.destination}, cost={self.cost}, time={self.time})"


# noinspection PyDataclass
class Graph(BaseModel):
    nodes: Dict[str, Node] = Field(default_factory=dict)
    vertices: List[Vertex] = Field(default_factory=list)

    def add_node(self, name: str) -> Node:
        if name not in self.nodes:
            self.nodes[name] = Node(name=name)
        return self.nodes[name]

    def add_vertex(
        self, source: str, destination: str, cost: float, time: float, mode: str
    ) -> Vertex:
        source_node = self.add_node(source)
        destination_node = self.add_node(destination)
        self.vertices.append(
            Vertex(
                source=source_node,
                destination=destination_node,
                cost=cost,
                time=time,
                mode=mode,
            )
        )
        return Vertex(
            source=source_node,
            destination=destination_node,
            cost=cost,
            time=time,
            mode=mode,
        )

    def to_dict(self):
        return {
            "nodes": {name: node.dict() for name, node in self.nodes.items()},
            "vertices": [vertex.dict() for vertex in self.vertices],
        }

    @classmethod
    def from_dict(cls, data):
        graph = cls()
        graph.nodes = {name: Node(**node) for name, node in data["nodes"].items()}
        graph.vertices = [
            Vertex(
                source=graph.nodes[vertex["source"]["name"]],
                destination=graph.nodes[vertex["destination"]["name"]],
                **{
                    k: v
                    for k, v in vertex.items()
                    if k not in {"source", "destination"}
                },
            )
            for vertex in data["vertices"]
        ]
        return graph
