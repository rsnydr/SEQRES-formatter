"""
    Script for SEQRES protein sequence formatting for one sequence
    and user-provided chain names (from Uniprot).
"""

import os
import re
import shutil
import sys

import helpers


def sequence_extractor(file):
    """ Given an input file, uses a regex to find the protein sequence
        contained in the file.
    """
    regex = re.compile(r'[GAVLITSMCPFYWHKRDENQ]')
    for line in file:
        line = line.strip()
        res = regex.findall(line)
        if len(line) == len(res):
            return ''.join(res)


def writer(chains, filename, option):
    """ Given a list of chain names and an input file, writes 
        to output files for each chain number. If option is 'y', 
        will also combine the output of those files to a single file.

        Example: 
            Inputs 'file.txt A B' followed by 'y' will write the following files:

            file-formatted-A.txt
            file-formatted-B.txt
            file-formatted.txt
    """
    with open(filename, 'r', encoding='utf-8') as file:
        s = sequence_extractor(file)

    try:
        total_length = len(s)
    except TypeError as err:
        print('Sequence not found. Check the formatting of your input file.', err)
        return

    try:
        aa_list = [helpers.d[char] for char in s]
    except KeyError as err:
        print('Sequence not formatted properly.', err)
        return

    aa_list_split = helpers.splitter(
        aa_list, helpers.NUM_OF_AMINO_ACIDS_PER_LINE)
    num_of_lines = len(aa_list_split)

    name, _ = os.path.splitext(filename)

    if option == 'y':
        filenames = []
    for chain in chains:
        formatted_filename = f'{name}-formatted-{chain}.txt'
        if formatted_filename in os.listdir():
            os.unlink(formatted_filename)
        if option == 'y':
            filenames.append(formatted_filename)
        with open(formatted_filename, 'a', encoding='utf-8') as f:
            for i in range(num_of_lines):
                sequence = ' '.join(aa_list_split[i])
                f.write(helpers.formatter(helpers.PROGRAM_CODE,
                        i + 1, chain, total_length, sequence))

    if option == 'y':
        combined_file = f'{name}-formatted.txt'
        if combined_file in os.listdir():
            os.unlink(combined_file)
        with open(combined_file, 'w', encoding='utf-8') as outfile:
            for file in filenames:
                with open(file, 'r', encoding='utf-8') as infile:
                    shutil.copyfileobj(infile, outfile)


if __name__ == "__main__":
    user_filename = sys.argv[1].strip()
    user_chains = sys.argv[2:]

    if not user_chains:
        sys.exit('You must supply at least one chain name.')

    if len(user_chains) > 1:
        user_option = input(
            "Do you also want your files combined into a single file? [y/n]: ").strip()
        if user_option not in ['y', 'n']:
            sys.exit("You must enter a valid option (y or n).")
    else:
        user_option = None

    writer(user_chains, user_filename, user_option)
