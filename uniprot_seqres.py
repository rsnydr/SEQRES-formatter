# script for SEQRES protein sequence formatting for one sequence and user-provided chain names (from Uniprot)

import os
import re
import shutil
import sys

import helpers


def sequence_extractor(file):
    """ Given an imput file, uses a regex to find the protein sequence
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
    with open(filename, 'r') as file:
        s = sequence_extractor(file)

    try:
        total_length = len(s)
    except ValueError:
        print('Sequence not found. Check the formatting of your input file.')
        return

    try:
        aa_list = [helpers.d[char] for char in s]
    except KeyError:
        print('Sequence not formatted properly.')
        return

    if not chains:
        print('You must supply at least one chain name.')
        return

    aa_list_split = helpers._split(aa_list, helpers.NUM_OF_AMINO_ACIDS_PER_LINE)
    num_of_lines = len(aa_list_split)

    path = os.getcwd()
    name, _ = os.path.splitext(filename)

    if option == 'y':
        filenames = []
    for chain in chains:
        formatted_filename = '{}-formatted-{}.txt'.format(name, chain)
        if formatted_filename in os.listdir():
            os.unlink(formatted_filename)
        if option == 'y':
            filenames.append(formatted_filename)
        with open(formatted_filename, 'a') as f:
            for i in range(num_of_lines):
                sequence = ' '.join(aa_list_split[i])
                f.write(helpers._format(helpers.PROGRAM_CODE, i + 1, chain, total_length, sequence))
                
    if option == 'y':
        combined_file = '{}-formatted.txt'.format(name)
        if combined_file in os.listdir():
            os.unlink(combined_file)
        with open(combined_file, 'w') as outfile:
            for file in filenames:
                with open(file, 'r') as infile:
                    shutil.copyfileobj(infile, outfile)



if __name__ == "__main__":
    filename = sys.argv[1].strip()
    chains = sys.argv[2:]

    if len(chains) > 1:
        option = input("Do you also want your files combined into a single file? [y/n]: ").strip()
        if option not in ['y', 'n']:
            sys.exit("You must enter a valid option (y or n).")
    else:
        option = None 

    writer(chains, filename, option)
