from cl2pasm import argv, infile
from cl2pasm import data, Patterns

outfile = open(argv[2], 'w')

head_label = head_func = ''

for line in infile:
	if ident:=Patterns.ident.match(line):
		shape = ident[1]
		name = ident[2]
		if not shape: shape = data[head_label][1][head_func][name][0]