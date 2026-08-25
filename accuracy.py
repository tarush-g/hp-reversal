from collections import deque
from itertools import permutations, product

import hp

#Largest size permutation checked by brute-force
MAX_SIZE = 6


def bfs(n):
    moves = [(i, j) for i in range(n) for j in range(i, n)]
    dist = {tuple(range(1, n + 1)): 0}
    queue = deque(dist)
    while queue:
        cur = queue.popleft()
        for i, j in moves:
            nxt = tuple(hp.reverse(list(cur), i, j))
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                queue.append(nxt)
    return dist


passed = 0
failed = 0

for n in range(1, MAX_SIZE + 1):
    truth = bfs(n)
    for base in permutations(range(1, n + 1)):
        for signs in product([1, -1], repeat=n):
            genome = [s * x for s, x in zip(signs, base)]
            want = truth[tuple(genome)]
            got = hp.reversal_distance(genome)
            if got == want:
                passed += 1
            else:
                failed += 1
                if failed <= 5:
                    print("wrong:", genome, "expected", want, "got", got)
    print("size %d checked, %d wrong so far" % (n, failed))

print()
print("accuracy: %d/%d = %.2f%%" % (passed, passed + failed, 100.0 * passed / (passed + failed)))