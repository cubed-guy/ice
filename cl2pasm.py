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

class dPrinter: __rmatmul__ = (lambda self, other: (print('', other), other)[1])
d = dPrinter()

''' ------------------------------PATTERNS-------------------------------- '''
import re

space_pattern = re.compile(r'\s+')
word_re = r'[\w_][\w\d_]*'
word_pattern = re.compile(word_re)
space_pattern = re.compile(r'\s*')
exp_re = fr'(\d*|{word_re})'	# only identifiers and numbers for now

unit_re = r'[0-8]'	# will add tuples later
shape_re = r'(\[\d+\]|[0-8])*'

dec_re = fr'({shape_re}{unit_re})({word_re})'
args_re = fr'\({exp_re}(\s*,\s*{exp_re})*\)'
dec_pattern = re.compile(dec_re)
func_pattern = re.compile(r'^'+dec_re+args_re)
label_pattern = re.compile('#'+dec_re+fr'(\({word_re}\))?'+':')

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
indent_stack = []
expect_indent = False

for line_no, line in enumerate(infile, 1):
	# ignore blank/commented lines
	if blank_pattern.match(line): continue

	# INDENTATION
	curr_indent = space_pattern.match(line)[0]
	if curr_indent != ''.join(indent_stack):
	  indent_diff = curr_indent
	  for level, indent in enumerate(indent_stack):
	    if indent_diff.startswith(indent):	# consistent indentation so far
	      indent_diff = indent_diff[len(indent):]
	    elif indent_diff:
	      raise TabError(f'inconsistent use of tabs and spaces at line {line_no}')
	    else: break	# dedent
	  # indent if indent_diff else dedent (if exhausted)
	  if indent_diff: indent_stack.append(indent_diff); level_diff = 1
	  else: level_diff = level-len(indent_stack); del indent_stack[level:]
	else: level_diff = 0
	level = len(indent_stack)

	if expect_indent and level_diff <= 0:
		raise IndentationError(f'expected indent block at line {line_no}')
	elif not expect_indent and level_diff > 0:
		raise IndentationError(f'unexpected indent block at line {line_no}')

	line = line.strip()
	expect_indent = not bool(blank_pattern.match(line.partition(':')[2]))

	if level_diff < 0:	# if dedent
		if not level: head_func = head_label = ''
		elif head_label and level == 1: head_func = ''

	# UPDATE DICT
	if   decl:=label_pattern.match(line):
	    label_type = decl[1]
	    label = decl[3]
	    Dict = data
	    if label in Dict: raise ValueError(
	      f"Label '{label}' already declared before line {line_no}.")
	    print(f'{label = } at line {line_no}')
	    Dict[label] = (label_type, {})
	    head_label = label

	elif decl:=func_pattern.match(line):
	    func_type = decl[1]
	    func = decl[3]
	    Dict = data[head_label][1]
	    if func in Dict: raise ValueError(
	      f"Function '{func}' already declared before line {line_no}.")
	    print(' '*level+f'{func = } at line {line_no} under {head_label!r}')
	    Dict[func] = (func_type, {})
	    head_func = func

	else:
	  line = line.partition('--')[0]
	  words = line.split()
	  for word in words:
	    decl = dec_pattern.match(word)
	    if not (decl): continue
	    var_type = decl[1]
	    var = decl[3]
	    Dict = data[head_label][1][head_func][1]
	    if var in Dict: raise ValueError(
	      f"Variable '{var}' already declared before line {line_no}.")
	    print(' '*level+f'{var = } at line {line_no} under {head_label!r}->{head_func!r}')
	    Dict[var] = var_type

	loc += len(line)

print(data)
