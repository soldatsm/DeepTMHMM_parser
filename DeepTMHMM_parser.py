import argparse
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument('input', help='Path to .3line file')
parser.add_argument('output', help='Path for output file')
parser.add_argument('-delimiter', help='Choose delimiter if output file 1 - tab, 2 - comma',
                    choices=[1, 2], type=int)
parser.add_argument('-simple', help='Make table only from 3line file ')
parser.add_argument('-topology', help='Make topology reformation'
                                      'in addition it is a path to TMRs.gff3')


args = parser.parse_args()


def simple_parser(line_data):
    table_data = pd.DataFrame()
    splited_list = [line_data[i:i + 3] for i in range(0, len(line_data) + 1, 3)]
    for i in splited_list:  # remove empty lists
        if len(i) == 0:
            splited_list.remove(i)
    for idx, val in enumerate(splited_list):
        table_data.loc[idx, 'Name'] = val[0].split(' | ')[0].replace('>','')
        table_data.loc[idx, 'Type'] = val[0].split(' | ')[1]
        table_data.loc[idx, 'AA'] = val[1]
        table_data.loc[idx, 'Topology'] = val[2]
    return table_data


def topol_parser(topology_file):

    plain_list = []
    nested_list = []
    accum = []
    protein_name = []
    tm_composition = []

    with open(topology_file, 'r') as topol_read_file:
        text = topol_read_file.readlines()
        for i in text:
            if '##' in i:
                continue
            else:
                plain_list.append(i.replace('# ', ''))
    for j in plain_list:
        if '//' in j:
            nested_list.append(accum)
            accum = []
        else:
            accum.append(j)
    for structure in nested_list:
        accum = []
        protein_name.append(structure[0].split('\t')[0].split(' ')[0])

        for data in structure[2::]:
            processed_composition = data.split('\t')
            accum.append(f'{processed_composition[1][0].lower()}{processed_composition[2]}-{processed_composition[3]}')
        tm_composition.append(' '.join(accum).strip())

    table_for_merge = pd.DataFrame({
            'IDs': protein_name,
            'TM_composition': tm_composition})

    return table_for_merge


if __name__ == '__main__':

    table = pd.DataFrame()

    with open(rf'{args.input}', 'r') as read_file:
        line_data = read_file.readlines()
        line_data = [i.strip('\n') for i in line_data]
        read_file.close()

    out_table = simple_parser(line_data)

    if args.simple is not None:
        if args.delimiter == 1:

            out_table.to_csv(rf'{args.output}',
                             index=False, sep='\t')
        elif args.delimiter == 2:

            out_table.to_csv(rf'{args.output}',
                             index=False)

    elif args.topology is not None:
        print(1)
        topology_table = topol_parser(args.topology)

        topology_table.to_csv(rf'{args.output}_tolp.csv')

        out_table = out_table.merge(topology_table, how='inner',
                                    right_on='IDs', left_on='Name')

        out_table = out_table.iloc[:, [0, 1, 2, 5]]

        if args.delimiter == 1:

            out_table.to_csv(rf'{args.output}',
                             index=False, sep='\t')
        elif args.delimiter == 2:

            out_table.to_csv(rf'{args.output}',
                             index=False)
