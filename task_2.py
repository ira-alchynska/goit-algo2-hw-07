import timeit
from functools import lru_cache
from timeit import Timer
import matplotlib.pyplot as plt

import sys
sys.setrecursionlimit(2000)


# --- Splay Tree implementation ---
class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None
        # Pre-seed base Fibonacci values
        self.insert(0, 0)
        self.insert(1, 1)

    def _rotate(self, x):
        p = x.parent
        if not p:
            return
        g = p.parent
        # Zig
        if x is p.left:
            p.left = b = x.right
            x.right = p
        else:
            # Zag
            p.right = b = x.left
            x.left = p
        if b:
            b.parent = p
        x.parent = g
        p.parent = x
        if g:
            if p is g.left:
                g.left = x
            else:
                g.right = x
        else:
            self.root = x

    def _splay(self, x):
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:
                # single rotation
                self._rotate(x)
            elif (x is p.left) == (p is g.left):
                # zig-zig
                self._rotate(p)
                self._rotate(x)
            else:
                # zig-zag
                self._rotate(x)
                self._rotate(x)

    def insert(self, key, val):
        if self.root is None:
            self.root = Node(key, val)
            return
        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # update existing
                node.val = val
                self._splay(node)
                return
        new_node = Node(key, val)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def search(self, key):
        node = self.root
        last = None
        while node:
            last = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return node
        # splay the last accessed node to root
        if last:
            self._splay(last)
        return None

# --- Fibonacci with LRU cache ---
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    # build bottom up
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

# --- Fibonacci with Splay Tree ---
def fibonacci_splay(n, tree):
    if n < 2:
        return n
    node = tree.search(n)
    if node is not None:
        return node.val
    # compute recursively
    val = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, val)
    return val

# --- Main measurement and plotting ---
if __name__ == "__main__":
    # Prepare test points
    ns = list(range(0, 951, 50))

    lru_times = []
    splay_times = []

    for n in ns:
        # Measure LRU Cache approach
        t_lru = Timer(lambda: fibonacci_lru(n))
        reps = t_lru.repeat(repeat=3, number=1)
        avg_lru = sum(reps) / len(reps)
        lru_times.append(avg_lru)
        fibonacci_lru.cache_clear()

        # Measure Splay Tree approach
        def run_splay():
            tree = SplayTree()
            return fibonacci_splay(n, tree)
        t_splay = Timer(run_splay)
        reps2 = t_splay.repeat(repeat=3, number=1)
        avg_splay = sum(reps2) / len(reps2)
        splay_times.append(avg_splay)

    # Print results table
    print(f"{'n':<8}{'LRU Cache Time (s)':<22}{'Splay Tree Time (s)':<22}")
    print("-" * 52)
    for n, t1, t2 in zip(ns, lru_times, splay_times):
        print(f"{n:<8}{t1:<22.6f}{t2:<22.6f}")

    # Plot the comparison graph
    plt.figure(figsize=(8, 5))
    plt.plot(ns, lru_times, marker='o', label='LRU Cache')
    plt.plot(ns, splay_times, marker='s', label='Splay Tree')
    plt.xlabel('n (Fibonacci Number)')
    plt.ylabel('Average Execution Time (seconds)')
    plt.title('Fibonacci: LRU Cache vs. Splay Tree Performance')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
