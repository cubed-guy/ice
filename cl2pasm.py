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
# if   len(argv) <2: raise ValueError('Input file not specified')
if   len(argv) <2: argv.append('Test file.cl')
# if   len(argv) <2: print('Input file not specified'); quit(1)
elif len(argv)==2: argv.append('a.pasm')
infile  = open(argv[1])
# argv[0] is the path of this python file

class dPrinter: __rmatmul__ = lambda self, other: (print('', other), other)[1]
d = dPrinter()

def err(Error, message = None):
	print(f'File "{argv[1]}", line {line_no}')
	print('\t'+line.strip())
	if message is None: print(Error)
	else: print(Error, message, sep = ': ')
	quit(1)

''' ------------------------------PATTERNS-------------------------------- '''
import re

word_re = r'[a-zA-Z_][a-zA-Z\d_]*'
word_pattern = re.compile(word_re)
space_pattern = re.compile(r'\s*')
exp_re = fr'(\d*|{word_re})'	# only identifiers and numbers for now

unit_re = r'[0-8]'	# will add tuples later
shape_re = r'\*?(\[\d+\]|[0-8])*?'

decl_re = fr'({shape_re}{unit_re})({word_re})'
optional_decl_re = fr'({shape_re}{unit_re})?({word_re})'
args_re = fr'\(({exp_re}(\s*,\s*{exp_re})*)?\)'
head_args_re = (fr'\(((?P<first>{optional_decl_re})(\s*,\s*{decl_re})*)?\)')
head_args_pattern = re.compile(head_args_re)
decl_pattern = re.compile(decl_re)
func_pattern = re.compile(optional_decl_re+fr'(?P<args>{head_args_re})')
label_pattern = re.compile('#'+decl_re+fr'(?P<parent>\({word_re}\))?'+':')

alloc_re = fr'\[{exp_re}\]+'	# shape and unit alloc later
alloc_pattern = re.compile(alloc_re+word_re)

'''  -------------------------PASS 1 - CREATING DICTS--------------------- '''
def getVars(region, level_ = None):
	Dict = data[head_label][1][head_func][1]
	
	if level_ is None: level_ = level
	decls = decl_pattern.finditer(region)
	args = head_args_pattern.match(region)
	if args:
		first_arg = args["first"]
		if head_label:
			Dict[first_arg] = data[head_label][0]
			print(line_no, ' '*level_+#f'under {head_label}.{head_func} '
			f'{first_arg} of shape {data[head_label][0]}.', sep = '\t')
		
	for decl in decls:
		declexp = decl[1]
		var = decl[3]
		print(line_no, ' '*level_+#f'under {head_label}.{head_func} 
			f'{var} of shape {declexp}.', sep = '\t')
		if var not in Dict: Dict[var] = declexp; continue
		if Dict[var] != declexp: err('ValueError', "Declaring variable "
			f"'{var}' with declexp {declexp}. "
			f"(Already declared with {Dict[var]})")

data = {'': (None, {'':(None, {})}, None)}
# {label: (label_type, {func: (func_type, {var: var_type})}, parent)}

loc = 0
head_func = ''
head_label = ''
indent_stack = []
expect_indent = False

for line_no, line in enumerate(infile, 1):
	# ignore comment
	# TODO: don't ignore '--' if in string
	line = line[:-1].partition('--')[0]

	# ignore blank lines
	if not line or line.isspace(): continue

	# INDENTATION
	curr_indent = space_pattern.match(line)[0]
	if curr_indent != ''.join(indent_stack):
	  indent_diff = curr_indent
	  for level, indent in enumerate(indent_stack):
	    if indent_diff.startswith(indent):	# consistent indentation so far
	      indent_diff = indent_diff[len(indent):]
	    elif indent_diff:err('TabError','inconsistent use of tabs and spaces.')
	    else: break	# dedent
	  # indent if indent_diff else dedent
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
	expect_indent = parts[1] and bool(space_pattern.fullmatch(parts[2]))
	# if line and not line.isspace(): print(' '*level+line[:-1])

	if level_diff < 0:	# if dedent
		if not level: head_func = head_label = ''
		elif head_label and level == 1: head_func = ''

	# UPDATE DICT
	if   decl:=label_pattern.match(line):
		declexp = decl[1]
		label = decl[3]
		Dict = data
		print(line_no, ' '*level+#f'under {head_label}.{head_func} '
			f'#{label} of shape {declexp}', sep = '\t', end = ' ')
		if label in Dict:err('ValueError',f"Label '{label}' already declared.")
		
		parent = decl['parent']
		if parent: parent = parent[1:-1]
		else: parent = None
		print(f"extends {parent!r}.")
		Dict[label] = (declexp, {}, parent)
		head_label = label

	elif decl:=func_pattern.match(line):
		declexp = decl[1]
		func = decl[3]
		Dict = data[head_label][1]
		print(line_no, ' '*level+#f'under {head_label}.{head_func} '
			f'{func}() of shape {declexp}', sep = '\t')
		if func in Dict: err('ValueError', f"Function '{func}' already declared.")
		
		Dict[func] = (declexp, {})
		head_func = func
		args = decl['args']
		getVars(args, level+1)
		getVars(line.partition(':')[2])

	elif line.count(':') > 1: err('SyntaxError', 'invalid syntax.')

	else: getVars(line)

	loc += len(line)

for l, f in data.items(): print(repr(l), f, sep = ':\t')
