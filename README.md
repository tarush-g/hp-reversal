# hp-reversal
An implementation of the Hannenhalli-Pevzner (HP) algorithm for finding the minimum reversal distance and a minimum reversal scenario between two unichromosomal genomes. The implementation constructs the required breakpoint, cycle, overlap, and hurdle structures to compute the reversal distance and identify a sequence of reversals that transforms one genome into the other.

# Usage
```python hp.py <genome1> [genome 2]```

Genomes are signed genes, e.g. "4,-3,1,-2,5"\n
Genome 2 defaults to the identity permutation (1..n)
## Examples
```
python hp.py 4,-3,1,-2,5
python hp.py "2 -3 1" "3 1 -2"
```
# References
[A very elementary presentation of the Hannenhalli–Pevzner theory](https://www.sciencedirect.com/science/article/pii/S0166218X04003440)

[Transforming Cabbage into Turnip: Polynomial Algorithm for Sorting Signed Permutations by Reversals](https://dl.acm.org/doi/pdf/10.1145/300515.300516)
