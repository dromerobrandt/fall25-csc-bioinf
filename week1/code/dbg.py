import copy
from typing import Dict, Set, Optional, List


def reverse_complement(key: str) -> str:
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    key = list(key[::-1])
    for i in range(len(key)):
        key[i] = complement[key[i]]
    return ''.join(key)


class Node:
    _children: Set[int]
    _count: int
    kmer: str
    visited: bool
    depth: int
    max_depth_child: Optional[int]

    def __init__(self, kmer: str):
        self._children: Set[int] = set()
        self._count: int = 0
        self.kmer: str = kmer
        self.visited: bool = False
        self.depth: int = 0
        self.max_depth_child: Optional[int] = None

    def add_child(self, kmer):
        self._children.add(kmer)

    def increase(self):
        self._count += 1

    def reset(self):
        self.visited = False
        self.depth = 0
        self.max_depth_child = None

    def get_count(self):
        return self._count

    def get_children(self):
        return list(self._children)

    def remove_children(self, target: Set[int]):
        self._children = self._children - target


class DBG:
    def __init__(self, k: int, data_list):
        self.k = k
        self.nodes: Dict[int, Node] = {}
        self.kmer2idx: Dict[str, int] = {}
        self.kmer_count = 0
        self._check(data_list)
        self._build(data_list)

    def _check(self, data_list):
        assert len(data_list) > 0
        assert self.k <= len(data_list[0][0])

    def _build(self, data_list):
        for data in data_list:
            for original in data:
                rc = reverse_complement(original)
                for i in range(len(original) - self.k - 1):
                    self._add_arc(original[i: i + self.k],
                                  original[i + 1: i + 1 + self.k])
                    self._add_arc(rc[i: i + self.k], rc[i + 1: i + 1 + self.k])

    def show_count_distribution(self):
        count = [0] * 30
        for idx in self.nodes:
            count[self.nodes[idx].get_count()] += 1
        print(count[0:10])

    def _add_node(self, kmer):
        if kmer not in self.kmer2idx:
            self.kmer2idx[kmer] = self.kmer_count
            self.nodes[self.kmer_count] = Node(kmer)
            self.kmer_count += 1
        idx = self.kmer2idx[kmer]
        self.nodes[idx].increase()
        return idx

    def _add_arc(self, kmer1, kmer2):
        idx1 = self._add_node(kmer1)
        idx2 = self._add_node(kmer2)
        self.nodes[idx1].add_child(idx2)

    def _get_count(self, child):
        return self.nodes[child].get_count()

    def _get_sorted_children(self, idx):
        children = self.nodes[idx].get_children()
        children.sort(key=self._get_count, reverse=True)
        return children

    def _get_depth(self, idx):
        if self.nodes[idx].visited:
            return self.nodes[idx].depth

        stack = [idx]
        next_child_index = {idx: 0}
        self.nodes[idx].visited = True

        while stack:
            current = stack[-1]
            children = self._get_sorted_children(current)
            if next_child_index.get(current, 0) < len(children):
                child = children[next_child_index[current]]
                next_child_index[current] += 1
                if not self.nodes[child].visited:
                    self.nodes[child].visited = True
                    stack.append(child)
                    next_child_index[child] = 0
            else:
                max_depth = 0
                max_child = None
                for child in children:
                    if self.nodes[child].depth > max_depth:
                        max_depth = self.nodes[child].depth
                        max_child = child
                self.nodes[current].depth = max_depth + 1
                self.nodes[current].max_depth_child = max_child
                stack.pop()

        return self.nodes[idx].depth

    def _reset(self):
        for idx in self.nodes.keys():
            self.nodes[idx].reset()

    def _get_longest_path(self):
        max_depth, max_idx = 0, None
        for idx in self.nodes.keys():
            depth = self._get_depth(idx)
            if depth > max_depth:
                max_depth, max_idx = depth, idx

        path: List[int] = []
        while max_idx is not None:
            path.append(max_idx)
            max_idx = self.nodes[max_idx].max_depth_child
        return path

    def _delete_path(self, path: List[int]):
        path_set = set(path)
        for idx in path:
            del self.nodes[idx]
        for idx in self.nodes.keys():
            self.nodes[idx].remove_children(path_set)

    def _concat_path(self, path):
        if len(path) < 1:
            return None
        concat = copy.copy(self.nodes[path[0]].kmer)
        for i in range(1, len(path)):
            concat += self.nodes[path[i]].kmer[-1]
        return concat

    def get_longest_contig(self):
        self._reset()
        path: List[int] = self._get_longest_path()
        contig = self._concat_path(path)
        self._delete_path(path)
        return contig
