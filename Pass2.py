# This file converts source code to pseudo assembly (pasm)
# (pasm because I still have to learn assembly)
# This is pass 2 and uses data extracted during pass 1

from Pass1 import argv, infile
from Pass1 import data, Patterns

outfile = open(argv[2], 'w')

head_label = head_func = ''

for line in infile:
	if ident:=Patterns.ident.match(line):
		shape = ident[1]
		name = ident[2]
		if not shape: shape = data[head_label][1][head_func][name][0]