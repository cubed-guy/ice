'''
Pass1.py - What can we get from the first pass?
	- return types
	- expressions (maybe save the variable names as numbers in a dict)
	- infer types and give errors when it doesn't match
'''

from sys import argv
# if len(argv) <2: print('Input file not specified'); quit(1)
if len(argv)<2: argv.append('Examples/Test file.cl')
if len(argv)<3: argv.append('a.pasm')
infile  = open(argv[1])
# argv[0] is the path of this python file

ismodule = __name__ != '__main__'
dprint = (lambda *args, **kwargs: None) if ismodule else print
class dPrinter:
	if ismodule: __rmatmul__ = lambda self, other: other
	else: __rmatmul__ = lambda self, other: (print('', other), other)[1]
d = dPrinter()

def err(Error, message = None):
	print(f'File "{argv[1]}", line {Global.line_no}')
	print('\t'+line.strip())
	if message is None: print(Error)
	else: print(Error, message, sep = ': ')
	quit(1)

class Global:
	def __new__(cls, line_no, line):
		Global.line_no, Global.line = line_no, line

''' ------------------------------PATTERNS-------------------------------- '''
import re

class Patterns:
	word_re = r'[a-zA-Z_][a-zA-Z\d_]*'
	word = re.compile(word_re)
	space = re.compile(r'\s*')

	unit_re  = r'\^?[0-8]'	# will add tuples later
	shape_re = r'\*?(\[\d+\]|[0-8])*?'

	decl_re  = fr'({shape_re}{unit_re})({word_re})'
	ident_re = fr'({shape_re}{unit_re})?({word_re})'
	token_re = fr'(\d+|{ident_re})'
	
	decl  = re.compile(decl_re)
	ident = re.compile(ident_re)
	token = re.compile(token_re)

	args_re = fr'\(({token_re}(\s*,\s*{token_re})*)?\)'
	head_args_re = (fr'\(((?P<first>{ident_re})(\s*,\s*{ident_re})*)?\)')

	head_args = re.compile(head_args_re)
	func  = re.compile(ident_re+fr'(?P<args>{head_args_re})')
	label = re.compile('#'+decl_re+fr'(?P<parent>\({word_re}\))?'+':')

	dim = re.compile(r'(\*?\d|\[\d+\])(?!\w)')

	alloc_re = fr'\[{token_re}\]+'	# shape and unit alloc later
	alloc = re.compile(alloc_re+word_re)

'''  -------------------------PASS 1 - CREATING DICTS--------------------- '''
class VarMeta:
	def __init__(self, shape, label_stack):
		self.shape = shape
		self.label_stack = label_stack
	def __repr__(self): return f'VarMeta({self.shape}, {self.label_stack})'

def getVars(region, level_ = None):
	Dict = data[head_label][1][head_func][1]
	
	if level_ is None: level_ = level
	args = Patterns.head_args.match(region)
	if args:
		first_arg = args['first']
		if head_label:
			Dict[first_arg] = (data[head_label][0], [])
			dprint(n, ' '*level_ +
				f'{first_arg} of shape {data[head_label][0]}.', sep = '\t')
		
	for decl in Patterns.decl.finditer(region):
		shape = decl[1]
		var = decl[3]
		dprint(n, ' '*level_+#f'under {head_label}.{head_func} 
			f'{var} of shape {shape}.', sep = '\t')
		if var not in Dict: Dict[var] = VarMeta(shape, []); continue
		if Dict[var] != shape: err('ValueError', "Declaring variable "
			f"'{var}' with shape {shape}. "
			f"(Already declared with {Dict[var].shape})")

data = {'': (None, {'':(None, {})}, None)}
# {label:
# 	(label_type,
# 	{func: (func_type, {var: (var_type, label_stack)})},
# 	parent)}

loc = 0
head_func = ''
head_label = ''
indent_stack = []
expect_indent = False
no_indent = False

for n, line in enumerate(infile, 1):
	# ignore blank lines
	if not line or line.isspace(): continue
	
	Global(n, line)

	# INDENTATION
	curr_indent = Patterns.space.match(line)[0]
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
	expect_indent = parts[1] and (not parts[2] or parts[2].isspace())

	if level_diff < 0:	# if dedent
		if not level: head_func = head_label = ''
		elif head_label and level == 1: head_func = ''

	# UPDATE DICT
	if   decl:=Patterns.label.match(line):
		shape = decl[1]
		label = decl[3]
		Dict = data
		dprint(n, ' '*level+f'#{label} with {shape = }', sep = '\t', end = ' ')
		if label in Dict:
			err('ValueError',f"Label '{label}' already declared.")
		
		parent = decl['parent']
		if parent: parent = parent[1:-1]
		else: parent = None
		dprint(f"extends {parent!r}.")
		Dict[label] = (shape, {}, parent)
		head_label = label

	elif decl:=Patterns.func.match(line):
		shape = decl[1]
		func = decl[3]
		Dict = data[head_label][1]
		dprint(n, ' '*level+f'{func}() with {shape = }', sep = '\t')
		if func in Dict:
			err('ValueError', f"Function '{func}' already declared.")
		
		Dict[func] = (shape, {})
		head_func = func
		args = decl['args']
		getVars(args, level+1)
		getVars(line.partition(':')[2])

	elif line.count(':') > 1: err('SyntaxError', 'invalid syntax.')

	else: getVars(line)

	loc += len(line)

if ismodule: print('Pass 1 successful'); infile.seek(0)
else:
	for l, f in data.items(): print(repr(l), f, sep = ':\t')
