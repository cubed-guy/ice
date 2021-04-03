# Pass 1 converts the source file to an intermediate format

import re
class Patterns:
	word_re = r'[a-zA-Z_][a-zA-Z\d_]*'
	word = re.compile(word_re)
	space = re.compile(r'\s*')

	string1_re = r'\'(\\\'|.)*?\''
	string2_re = r'\"(\\\"|.)*?\"'
	string = re.compile(string1_re+'|'string2_re)

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


from sys import argv
# if len(argv) <2: print('Input file not specified'); quit(1)
if len(argv)<2: argv.append('Examples/Test file.cl')
if len(argv)<3: argv.append('a.pasm')
if len(argv)<4: argv.append('a.temp') #intermediate file?

ismodule = __name__ != '__main__'
dprint = (lambda *args, **kwargs: None) if ismodule else print

def err(Error, message = None):
	print(f'File "{argv[1]}", line {Global.line_no}')
	print('\t'+line.strip())
	if message is None: print(Error.__name__)
	else: print(Error.__name__, message, sep = ': ')
	quit(1)

class Global:
	infile  = open(argv[1])
	outfile = open(argv[3], 'w')
	def __new__(cls, line_no, line):
		Global.line_no, Global.line = line_no, line

# def output(*args, file = Global.outfile, **kwargs): print(*args, file = file, **kwargs)
output = print


class VarMeta:
	def __repr__(self): return f'VarMeta({self.shape}, {self.label_stack})'
	def __init__(self, shape, label_stack):
		self.shape = shape
		self.label_stack = label_stack

def getVars(region, level_ = None):
	Dict = data[head_label][1][head_func][1]
	
	if ismodule:
	  if level_ is None: level_ = level
	  args = Patterns.head_args.match(region)
	  if args:
	    first_arg = args['first']
	    if head_label:
	    	Dict[first_arg] = (data[head_label][0], [])
	    	dprint(n, ' '*level_ +
	    		f'{first_arg} of shape {data[head_label][0]}.', sep = '\t')

	str_spans = [string.span() for string in Patterns.string.finditer(region)]
	curr_span = str_spans[0]
	span_number = 0

	for decl in Patterns.decl.finditer(region):
		while curr_span[-1] < decl.span()[-1]:
			if span_number >= len(str_spans)-1:
			   span_number  = len(str_spans)-1; break
			span_number += 1
			curr_span = str_spans[span_number]
		else:
			if curr_span[0] < decl.span()[0]: continue

		shape = decl[1]
		var   = decl[3]
		dprint(n, ' '*level_ + f'{var} of shape {shape}.', sep = '\t')
		if var not in Dict: Dict[var] = VarMeta(shape, []); continue
		if Dict[var] != shape: err(ValueError 'Declaring variable '
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
quote = ''

for n, line in enumerate(infile, 1):
	Global(n, line)

	# ignore comments outside strings
	escape = False
	cStart = False
	isblank = True
	for pos, c in enumerate(line):
		if quote:
			if not escape:
				if c == '\\': escape = True
				elif c == quote: quote = ''
		elif c in '"\'': quote = c; isblank = False
		elif c == '-':
			if cStart: break
			else: cStart = True
		else:
			if isblank and not c.isspace(): isblank = False
			cStart = False
	if quote and not escape: err(SyntaxError, 'EOL while parsing string.')
	if isblank: continue	# ignore blank lines

	line = line[:pos-2]

	# INDENTATION
	curr_indent = Patterns.space.match(line)[0]
	if curr_indent != ''.join(indent_stack):
	  indent_diff = curr_indent
	  for level, indent in enumerate(indent_stack):
	    if indent_diff.startswith(indent):	# consistent indentation so far
	      indent_diff = indent_diff[len(indent):]
	    elif indent_diff: err(TabError, 'inconsistent use of tabs and spaces.')
	    else: break	# dedent
	  # indent if indent_diff else dedent
	  if indent_diff: indent_stack.append(indent_diff); level_diff = 1
	  else: level_diff = level-len(indent_stack); del indent_stack[level:]
	else: level_diff = 0
	level = len(indent_stack)

	if expect_indent and level_diff <= 0:
		err(IndentationError, 'expected indent block.')
	elif not expect_indent and level_diff > 0:
		err(IndentationError, 'unexpected indent block.')

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
		if label in Dict: err(ValueError, f"Label '{label}' already declared.")
		
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
		if func in Dict:err(ValueError, f"Function '{func}' already declared.")
		
		Dict[func] = (shape, {})
		head_func = func
		args = decl['args']
		getVars(args, level+1)
		getVars(line.partition(':')[2])

	elif line.count(':') > 1: err(SyntaxError, 'invalid syntax.')

	else: getVars(line)

	loc += len(line)

if ismodule: print('Pass 1 successful'); infile.seek(0)
else:
	for l, f in data.items(): print(repr(l), f, sep = ':\t')
