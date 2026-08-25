from itertools import combinations
import networkx as nx

## Map each signed gene x to a pair of vertices, with caps for ends of the genome.
## +x -> (2x-1, 2x)    -x -> (2x, 2x-1)
def map_vertices(genome):
    seq = [0]
    for g in genome:
        a = abs(g)
        seq += [2 * a - 1, 2 * a] if g > 0 else [2 * a, 2 * a - 1]
    seq.append(2 * len(genome) + 1)
    return seq

## Builds a breakpoint graph based on the source and target genomes
## gamma = source genome, pi = target genome (as in HP paper)
def build_breakpoint(gamma, pi=None):
    # Defaults to identity permutation (1, 2, ... , n).
    n=len(gamma)

    pi = pi if pi is not None else list(range(1, n+1))

    vx_gamma=map_vertices(gamma)
    vx_pi=map_vertices(pi)

    bp = nx.MultiGraph()
    bp.add_nodes_from(range(2*n+2))

    for i in range(0, len(vx_gamma)-1, 2):
        bp.add_edge(vx_gamma[i], vx_gamma[i+1], color="black") #source edges
        bp.add_edge(vx_pi[i], vx_pi[i+1], color="gray") #target edges

    pos = {v: i for i, v in enumerate(vx_gamma)}
    return bp, pos

## Gets the orientation/span of edges in breakpoint graph
def orientation(bp, pos):
    spans, oriented = [], []
    target_edges = [(u, v) for u, v, d in bp.edges(data=True) if d["color"] == "gray"]
    for u, v in target_edges:
        p, q = pos[u], pos[v]
        spans.append((min(p, q), max(p, q)))
        oriented.append(p % 2 == q % 2)
    return spans, oriented

## Builds an overlap graph of overlapping cycles
def overlap_graph(spans):
    og = nx.Graph()
    og.add_nodes_from(range(len(spans)))
    for i, j in combinations(range(len(spans)), 2):
        (a, b), (x, y) = sorted((spans[i], spans[j]))
        if a < x < b < y:
            og.add_edge(i, j)
    return og

## Finds the connected components in the overlap graph
def components(spans, oriented):
    comps = []
    for group in nx.connected_components(overlap_graph(spans)):
        points = {p for k in group for p in spans[k]}
        if len(group) == 1 and max(points) - min(points) == 1:
            continue
        comps.append((points, any(oriented[k] for k in group)))
    return comps

def find_hurdles(unoriented, n):
    hurdles = []
    for points in unoriented:
        circle = nx.cycle_graph(2 * n + 2)
        circle.remove_nodes_from(points)
        arc = {}
        for k, a in enumerate(nx.connected_components(circle)):
            for p in a:
                arc[p] = k
        others = [o for o in unoriented if o is not points]
        if len({arc[p] for pts in others for p in pts}) <= 1:
            hurdles.append(points)
    return hurdles

def is_fortress(hurdles, unoriented, n):
    if len(hurdles) < 3 or len(hurdles) % 2 == 0:
        return False
    for h in hurdles:
        rest = [u for u in unoriented if u is not h]
        if not any(x not in hurdles for x in find_hurdles(rest, n)):
            return False
    return True

def reversal_distance(gamma, pi=None):
    n = len(gamma)
    bp, pos = build_breakpoint(gamma, pi)
    spans, oriented = orientation(bp, pos)
 
    unoriented = [pts for pts, o in components(spans, oriented) if not o]
    hurdles = find_hurdles(unoriented, n)
    fortress = is_fortress(hurdles, unoriented, n)
 
    return n + 1 - nx.number_connected_components(bp) + len(hurdles) + fortress

## Reverse genes from i to j and flip signs
def reverse(genome, i, j):
    return genome[:i] + [-g for g in reversed(genome[i:j+1])] + genome[j+1:]
 
def sort_by_reversals(gamma, pi=None):
    cur = list(gamma)
    d = reversal_distance(cur, pi)
    steps = []
    while d > 0:
        for i in range(len(cur)):
            for j in range(i, len(cur)):
                nxt = reverse(cur, i, j)
                if reversal_distance(nxt, pi) == d - 1:
                    steps.append((i, j))
                    cur, d = nxt, d - 1
                    break
            else:
                continue
            break
    return steps
