'''
    Script for SEQRES formatting from PDB fasta files.
'''

import os
import re
import sys

import helpers


def chain_extractor(line):
    """ Uses regexes to extract the chain names from a given line.

        Example: 
            Calling chain_extractor on 'some-text|Chains A, B, C|some-more-text' 
            will return the list '[A, B, C]'.
    """
    regex = re.compile(r'(?<=\|Chain)(.*?)(?=\|)')
    mo = regex.search(line)
    try:
        chains = mo.group().split(',')
        chains[0] = re.sub(r's', '', chains[0])
        chains = map(lambda x: x.strip(), chains)
        return chains
    except AttributeError as err:
        print('No chain name found. Check the formatting of your file.', err)
        return


def extractor(file):
    """ Given an input file, returns a zip object pairing
        each protein sequence found with its associated chain names.
    """
    chains = []
    sequences = []
    for line in file:
        if line[0] == '>':
            chains.append(chain_extractor(line))
        else:
            line = line.strip()
            sequences.append(line)

    return zip(chains, sequences)


def write_helper(chain_pair, file):
    """ Given a tuple consisting of a list of chain names paired
        with a protein sequence, and an output file, writes this 
        information in the correct formatting to the output file.
    """
    chains = chain_pair[0]
    s = chain_pair[1]
    total_length = len(s)
    try:
        aa_list = [helpers.d[char] for char in s]
    except KeyError as err:
        print(
            f'Code corresponding to chains {list(chains)} not formatted properly.', err)
        return
    aa_list_split = helpers.splitter(
        aa_list, helpers.NUM_OF_AMINO_ACIDS_PER_LINE)
    num_of_lines = len(aa_list_split)

    for chain in chains:
        for i in range(num_of_lines):
            sequence = ' '.join(aa_list_split[i])
            file.write(helpers.formatter(helpers.PROGRAM_CODE,
                       i + 1, chain, total_length, sequence))


def writer(filename):
    """ Given the input file, extracts the data
        and iterates write_helper to the output 
        file labeled filename-formatted.txt
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data = extractor(file)

    name, _ = os.path.splitext(filename)
    formatted_filename = f'{name}-formatted.txt'

    if formatted_filename in os.listdir():
        os.unlink(formatted_filename)
    with open(formatted_filename, 'a', encoding='utf-8') as file:
        for pair in data:
            write_helper(pair, file)


if __name__ == "__main__":
    user_filename = sys.argv[1].strip()
    writer(user_filename)
