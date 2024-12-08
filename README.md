# SEQRES formatter

SEQRES formatter is a collection of two Python scripts for formatting protein sequences from FASTA files from PDB and UniProt databases. The SEQRES file is formatted for structure deposition to PDB. There are two scripts:

```python3
pdb_seqres.py
```

This script takes as input FASTA files from PDB (which contain chain names) and automatically formats them properly for deposition.

```python3
uniprot_seqres.py
```

This script takes as input FASTA files from Uniprot (which do not contain chain names) and relies on user-provided chain names to complete the formatting.

## Installation

Clone this repo:

```bash
git clone
```

## Usage

This script only requires that you have Python 3 installed. Place the files you want formatted in the same directory containing the scripts. For formatting a FASTA file from PDB run

```bash
python3 pdb_seqres.py example_pdb.fasta
```

This yields the formatted output file

```bash
example_pdb-formatted.txt
```

For formatting a file containing a single protein sequence from Uniprot and user-provided chain names, run:

```bash
python3 uniprot_seqres.py example_uniprot.txt A B C
```

Here, the user-provided chain names are 'A', 'B', and 'C', each separated by a single space.
This yields the prompt

```bash
Do you also want your files combined into a single file? [y/n]:
```

Entering 'y' will write the following formatted files:

```bash
example_uniprot-A.txt
example_uniprot-B.txt
example_uniprot-C.txt 
example_uniprot-formatted.txt
```

Here, 'example_uniprot-formatted.txt' is a single file containing the concatenation of the previous files, whereas the other files contain the SEQRES formatting of the protein sequence with each corresponding chain name.

## License

[MIT](https://choosealicense.com/licenses/mit/)
