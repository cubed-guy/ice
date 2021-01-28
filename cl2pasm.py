# This file converts source code to pseudo assembly (pasm)
# (pasm because I still have to learn assembly)

'''Outline:
Pass 1 - dict of variable locations, shapes and sizes
       - dict of function return shapes and sizes
Pass 2 - method substitution (including __data_definition__ methods)
       - assignment substitution
       - functions and .text section
'''

from sys import argv
if   len(argv) <2: raise ValueError('Input file not specified')
elif len(argv)==2: argv.append('a.pasm')
infile  = open(argv[1])
outfile = open(argv[2], 'w')
# argv[0] is the path of this python file

''' ------------------------------PATTERNS-------------------------------- '''
import re

space_pattern = re.compile(r'\s+')
word_re = r'[\w_][\w\d_]*'
word_pattern = re.compile(word_re)
exp_re = fr'(\d*|{word_re})'	# only identifiers and numbers for now

unit_re = r'[0-8]'	# will add tuples later
shape_re = r'(\[\d+\]|[0-8])*'

dec_re = fr'({shape_re}{unit_re})({word_re})'
args_re = fr'\({exp_re} (\s*,\s*{exp_re})*\)'
dec_pattern = re.compile(dec_re)
func_pattern = re.compile(r'^'+dec_re+args_re+':')
label_pattern = re.compile('#'+dec_re+fr'\({word_re}\)'+':')

blank_pattern = re.compile(r'^(--.*)?$')

alloc_re = fr'\[{exp_re}\]+'	# shape and unit alloc later
alloc_pattern = re.compile(alloc_re+word_re)

'''  -------------------------PASS 1 - CREATING DICTS--------------------- '''
data = {'': (None, {'':(None, {})})}
# {label: (label_type, {func: (func_type, {var: var_type})})}

indent = ''
meth_indent = ''	# indentation level of method header

loc = 0
head_func = ''
head_label = ''
for line_no, line in enumerate(infile, 1):
	# ignore blank/commented lines
	if blank_pattern.match(line): continue

	# indent right under label
	if head_label and not meth_indent:
		indent_groups = space_pattern.match(line)
		if indent_groups: indent = meth_indent = indent_groups[0]

	elif head_func and 1: pass


	# indent
	if line.startswith(indent):
		indent_groups = space_pattern.match(line)
		if indent_groups: indent = indent_groups[0]
	# dedent
	else:
		curr_indent = re.match(r'\s*', line)[0]
		if indent.startswith(curr_indent):
			indent = curr_indent
			if meth_indent.startswith(indent): head_func = ''
			if not indent: head_label = ''
		else: raise TabError('inconsistent use of tabs and spaces.')


	# update dicts
	if   decl:=label_pattern.match(line):
		label_type = decl[1]
		label = decl[3]
		Dict = data
		if label in Dict: raise ValueError(
			f"Label '{label}' already declared before line {line_no}.")
		Dict[label] = (label_type, {})
		head_label = ''

	elif decl:=func_pattern.match(line):
		func_type = decl[1]
		func = decl[3]
		Dict = data[head_label][1]
		if func in Dict: raise ValueError(
			f"Function '{func}' already declared before line {line_no}.")
		Dict[func] = (func_type, {})
		head_func = ''

	elif decl:=dec_pattern.match(line):
		var_type = decl[1]
		var = decl[3]
		if var in Dict: raise ValueError(
			f"Variable '{var}' already declared before line {line_no}.")
		Dict = data[head_label][1][head_func][1]
		Dict[var] = var_type

	loc += len(line)

print(data)
