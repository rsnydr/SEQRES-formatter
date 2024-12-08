# helpers.py 
# global amino acid dictionary, formatting parameters, and helper functions for seqres-pdb.py and seqres-uniprot.py


d = {'G' :'GLY', 'A' : 'ALA', 'V' : 'VAL' , 'L' : 'LEU', 'I' :'ILE', 'T' :'THR', 'S' :'SER',
    'M' :'MET', 'C' :'CYS', 'P' :'PRO',  'F' : 'PHE', 'Y' :'TYR', 'W' : 'TRP', 'H' :'HIS', 
    'K' : 'LYS', 'R' : 'ARG', 'D' : 'ASP', 'E' : 'GLU', 'N' : 'ASN', 'Q' : 'GLN'}

NUM_OF_AMINO_ACIDS_PER_LINE = 13
PROGRAM_CODE = 'SEQRES'

def _split(alist, k):
    """ Given a list and an int k, returns a list
        containing all sublists of size k with possibly 
        a final sublist of size at most k - 1
    """
    res = []
    n = len(alist)
    if n <= k:
        res.append(alist)
        return res

    multiples = [i * k for i in range(n // k)]
    for idx in multiples:
        res.append(alist[idx : idx + k])

    if n % k != 0:
        rem = alist[n//k * k : n // k * k + n % k]
        res.append(rem)

    return res


def _format(program_code, line_num, chain_num, length, sequence):
    """ Helper function for proper line formatting.
    """
    line_num_with_space = '{: >4}'.format(line_num)
    chain_with_space = '{: <3}'.format(chain_num)
    length_with_space = '{: <5}'.format(length)
    return '{}{} {}{}{}\n'.format(program_code, 
                                      line_num_with_space, 
                                      chain_with_space,
                                      length_with_space,
                                      sequence)