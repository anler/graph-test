from collections import defaultdict, deque
import heapq
from dataclasses import dataclass
from typing import Iterable, Optional

_label = 0


def label():
    "A helper function to automatically labe nodes"
    global _label
    _label += 1
    return str(_label)


@dataclass
class Node:
    label: str
    left: Optional["Node"] = None
    right: Optional["Node"] = None


class Graph:
    def __init__(self):
        self._adj = defaultdict(lambda: set())

    def add(self, node: str):
        self._adj[node] = set()

    def connect(self, from_: str, to: str):
        self._adj[from_].add(to)
        self._adj[to].add(from_)

    def degree(self, node: str) -> int:
        return len(self._adj[node])

    def adj(self, node: str) -> Iterable[str]:
        return self._adj[node]

    def __iter__(self) -> Iterable[str]:
        return self._adj.keys()

    def __str__(self):
        lines = []
        for node in self._adj:
            lines.append(f"{node} -> {self._adj[node]}")
        return "\n".join(lines)


class CC:
    def __init__(self, g: Graph):
        self.g = g
        self.cc = 0
        self.visited = defaultdict(lambda: False)

    def visit(self, node: str):
        if self.visited[node]:
            return

        adj = list(self.g.adj(node))
        if len(adj) == 2 and (
            (self.visited[adj[0]] and not self.visited[adj[1]])
            or (self.visited[adj[1]] and not self.visited[adj[0]])
        ):
            return
        # Maybe I should also consider the case of three connections
        # with one or two already visited? 🤔

        self.visited[node] = True
        for adj in self.g.adj(node):
            self.visited[adj] = True

        self.cc += 1


class MinInstallations:
    def __init__(self, root: Node):
        g = self._build_graph(root)
        pq = self._build_queue(root, g)
        cc = CC(g)

        while len(pq) > 0:
            [_, _, node] = heapq.heappop(pq)
            cc.visit(node)

        self.count = cc.cc

    def _build_queue(self, root: Node, g: Graph):
        pq = []
        q = deque([])
        q.append((root, 1))
        while len(q) > 0:
            node, level = q.popleft()
            item = (-1 * g.degree(node.label), -1 * level, node.label)
            heapq.heappush(pq, item)
            if node.left:
                q.append((node.left, level + 1))
            if node.right:
                q.append((node.right, level + 1))

        return pq

    def _build_graph(self, root: Node):
        g = Graph()

        def traverse(node: Node, parent: Optional[Node] = None):
            g.add(node.label)
            if parent is not None:
                g.connect(node.label, parent.label)

            if node.left:
                g.connect(node.label, node.left.label)
                traverse(node.left, node)

            if node.right:
                g.connect(node.label, node.right.label)
                traverse(node.right, node)

        traverse(root)

        return g


print(MinInstallations(Node("1")).count)
print(MinInstallations(Node("1", right=Node("2"))).count)
print(MinInstallations(Node("1", left=Node("3"), right=Node("2"))).count)
print(
    MinInstallations(
        Node(
            label(),
            left=Node(label(), right=Node(label(), left=Node(label()))),
            right=Node(label(), right=Node(label())),
        )
    ).count
)

print(
    MinInstallations(
        Node(
            label(),
            left=Node(
                label(),
                left=Node(label(), left=Node(label())),
                right=Node(label(), right=Node(label())),
            ),
            right=Node(
                label(),
                right=Node(
                    label(),
                    right=Node(
                        label(),
                        right=Node(label(), left=Node(label(), left=Node(label()))),
                    ),
                ),
            ),
        )
    ).count
)
