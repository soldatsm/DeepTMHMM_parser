# Read Me

## Description

This is parser of data from [DeepTMHMM](https://dtu.biolib.com/DeepTMHMM/)

It takes file `.3line` and\or `.gff3 ` to create table.

This table consist of next colums:
* Name -- protein id according to 3line and gff3
* Type -- protein type (TM, GLOB,SP or TM+SP)
* AAs -- amino acid sequence
* TM_composition -- protein structure in format **o1-12 t13-20 s21-30**, where o - ouside localisation of AA and number of such AA, t - membrane localisation, s - signal part.

## Dependence 

*`pandas`

*`argparse`

## Help message
To print help message use flag -h

`DeepTMHMM_parser.py -h`
