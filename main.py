import sys
from hp import reversal_distance, reverse, sort_by_reversals

## Parse a genome from a command line argument, e.g. "4,-3,1,-2,5" or "[4 -3 1 -2 5]"
def parse_genome(text):
    cleaned = text.strip().strip("[]()").replace(",", " ")
    if not cleaned.strip():
        raise ValueError("empty genome")
    try:
        genome = [int(tok) for tok in cleaned.split()]
    except ValueError:
        raise ValueError("genome must be whitespace or comma separated integers: %r" % text)
    if any(g == 0 for g in genome):
        raise ValueError("genes are numbered from 1. 0 is not a valid gene.")
    if len(set(abs(g) for g in genome)) != len(genome):
        raise ValueError("each gene may appear only once.")
    return genome


def main(argv):
    if len(argv) not in (2, 3):
        print("usage: python hp.py <genome1> [genome 2]")
        print("       genomes are signed genes, e.g. \"4,-3,1,-2,5\"")
        print("       genome 2 defaults to the identity permutation (1..n)")
        print()
        print("examples:")
        print("python hp.py 4,-3,1,-2,5")
        print("python hp.py \"2 -3 1\" \"3 1 -2\"")
        return 2

    try:
        g1 = parse_genome(argv[1])
        g2 = parse_genome(argv[2]) if len(argv) == 3 else None
        if g2 is not None and sorted(map(abs, g1)) != sorted(map(abs, g2)):
            raise ValueError("both genomes must contain the same genes.")
    except ValueError as err:
        print("Error:", err)
        return 2

    target = g2 if g2 is not None else list(range(1, len(g1) + 1))
    print("source:", g1)
    print("target:", target)
    print("reversal distance:", reversal_distance(g1, g2))

    cur = list(g1)
    steps = sort_by_reversals(g1, g2)
    if steps:
        print()
        print("scenario:")
        for i, j in steps:
            cur = reverse(cur, i, j)
            print("  reverse genes %d,%d -> %s" % (i + 1, j + 1, cur))
    if cur != target:
        print("Warning: scenario did not reach the target genome")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))