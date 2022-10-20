# TODO Парсер результатов DeepTMHMM в xls\csv таблицу
#TODO Сделать так чтобы он либо добавлял к имеющейся таблице инфу из парсера \\
# тогда нужно чтобы он соотносил результаты TM по именам генов
# TODO  Либо отдельную таблицу где имена генов из его аутпута
#TODO Так же добавить опцию с тем чтобы делать или не делать столбце с TM топологией
# если делать что нужно запрашивать второй аутпут TM

import argparse
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument('input', help='Path to .3line file')
parser.add_argument('output')
parser.add_argument('-simple')
parser.add_argument('-topology')

args = parser.parse_args()


def simple_parser(line_data, topol=None):
    splited_list = [line_data[i:i + 3] for i in range(0, len(line_data) + 1, 3)]
    table_data = pd.DataFrame({'Type':splited_list})
    return table_data

def parser_merj():
    pass


if __name__ == '__main__':

    table = pd.DataFrame()

    with open(rf'{args.input}', 'r') as read_file:
        line_data = read_file.readlines()
        line_data = [i.strip('\n') for i in line_data]
        read_file.close()

    if args.topology is not None:
        with open(rf'{args.topology}', 'r') as topol_file:
            topol_data = read_file.readlines()

        topol_data = topol_data[4::]

        new_data = []

        for i in topol_data:
            new_data.append(i.strip("'").strip('\n'))
            if i == '\n':
                new_data.pop()


    if args.simple is not None:
        simple_parser(line_data)