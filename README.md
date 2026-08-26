# hp-reversal
An implementation of the Hannenhalli-Pevzner algorithm to compute the reversal distance and identify a sequence of reversals that transforms one unichromosomal genome into the other. 

To-do: extend for multichromosomal genomes

# Usage
```
python main.py <genome1> [genome 2]
python main.py 4,-3,1,-2,5
python main.py "2 -3 1" "3 1 -2"
```

The first genome is required, and the second is optional and defaults to the identity permutation (1, 2, ..., n). Genes are signed integers, comma- or space-separated, with optional surrounding brackets. Output includes reversal distance and an optimal step-by-step scenario. `accuracy.py` checks the algorithm against BFS in the reversal graph for every signed permutation up to 6 genes (50,362 cases).

# References
[A very elementary presentation of the Hannenhalli–Pevzner theory](https://www.sciencedirect.com/science/article/pii/S0166218X04003440)

[Transforming Cabbage into Turnip: Polynomial Algorithm for Sorting Signed Permutations by Reversals](https://dl.acm.org/doi/pdf/10.1145/300515.300516)

[Human and mouse genomic sequences reveal extensive breakpoint reuse in mammalian evolution ](https://pubmed.ncbi.nlm.nih.gov/12810957/)
