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
# if   len(argv) <2: print('Input file not specified'); quit(1)
elif len(argv)==2: argv.append('a.pasm')
infile  = open(argv[1])
outfile = open(argv[2], 'w')
# argv[0] is the path of this python file

class dPrinter: __rmatmul__ = lambda self, other: (print('', other), other)[1]
d = dPrinter()

def err(Error, message = None):
	print(f'"{argv[1]}", error in line {line_no}')
	print('\t'+line.strip())
	if message is None: print(Error)
	else: print(Error, message, sep = ': ')
	quit(1)

''' ------------------------------PATTERNS-------------------------------- '''
import re

space_pattern = re.compile(r'\s+')
word_re = r'[\w_][\w\d_]*'
word_pattern = re.compile(word_re)
space_pattern = re.compile(r'\s*')
exp_re = fr'(\d*|{word_re})'	# only identifiers and numbers for now

unit_re = r'[0-8]'	# will add tuples later
shape_re = r'\*?(\[\d+\]|[0-8])*'

declexp_re = fr'({shape_re}{unit_re})({word_re})'
func_declexp_re = fr'({shape_re}{unit_re})?({word_re})'
args_re = fr'\(({exp_re}(\s*,\s*{exp_re})*)?\)'
dec_pattern = re.compile(declexp_re)
func_pattern = re.compile(func_declexp_re+args_re)
label_pattern = re.compile('#'+declexp_re+fr'(\({word_re}\))?'+':')

blank_pattern = re.compile(r'\s*(--.*)?$')

alloc_re = fr'\[{exp_re}\]+'	# shape and unit alloc later
alloc_pattern = re.compile(alloc_re+word_re)

'''  -------------------------PASS 1 - CREATING DICTS--------------------- '''
def getVars(region, level_ = None):
	if level_ is None: level_ = level
	decls = dec_pattern.findall(region)
	for decl in decls:
		declexp = decl[0]
		var = decl[2]
		Dict = data[head_label][1][head_func][1]
		if var in Dict: err('ValueError', f"Label '{var}' already declared.")
		print(line_no, ' '*level_+f'under {head_label}.{head_func} {var = } of {declexp}')
		Dict[var] = declexp

data = {'': (None, {'':(None, {})}, None)}
# {label: (label_type, {func: (func_type, {var: var_type})}, parent)}

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
	    elif indent_diff:err('TabError','inconsistent use of tabs and spaces.')
	    else: break	# dedent
	  # indent if indent_diff else dedent (if exhausted)
	  if indent_diff: indent_stack.append(indent_diff); level_diff = 1
	  else: level_diff = level-len(indent_stack); del indent_stack[level:]
	else: level_diff = 0
	level = len(indent_stack)

	if expect_indent and level_diff <= 0:
		err('IndentationError', 'expected indent block.')
	elif not expect_indent and level_diff > 0:
		err('IndentationError', 'unexpected indent block.')

	line = line.strip()
	parts = line.partition(':')
	expect_indent = parts[1] and bool(blank_pattern.match(parts[2]))

	if level_diff < 0:	# if dedent
		if not level: head_func = head_label = ''
		elif head_label and level == 1: head_func = ''

	# UPDATE DICT
	if   decl:=label_pattern.match(line):
		declexp = decl[1]
		label = decl[3]
		parent = decl[4]
		Dict = data
		if label in Dict:err('ValueError',f"Label '{label}' already declared.")
		print(line_no, ' '*level+f'under {head_label}.{head_func} {label = } of {declexp}')
		
		if not parent: parent = None
		Dict[label] = (declexp, {}, parent)
		head_label = label

	elif decl:=func_pattern.match(line):
		declexp = decl[1]
		func = decl[3]
		Dict = data[head_label][1]
		if func in Dict: err('ValueError',f"Label '{func}' already declared.")
		print(line_no, ' '*level+f'under {head_label}.{head_func} {func = } of {declexp}')
		
		Dict[func] = (declexp, {})
		head_func = func
		args = decl[4]
		getVars(args, level+1)

	else: getVars(line.partition('--')[0])

	loc += len(line)

for l, f in data.items(): print(repr(l), f, sep = ':\t')
