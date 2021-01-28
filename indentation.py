'''Outline
indent on head
on dedent, pop heads
else TabError
'''
import re

word_re = r'[\w_][\w\d_]*'
exp_re = fr'(\d*|{word_re})'	# only identifiers and numbers for now
word_pattern = re.compile(word_re)
space_pattern = re.compile(r'\s+')
blank_pattern = re.compile(r'^(--.*)?$')

unit_re = r'[0-8]'	# will add tuples later
shape_re = r'(\[\d+\]|[0-8])*'

args_re = fr'\({exp_re} (, {exp_re})*\)'
dec_re  = fr'({shape_re}{unit_re})({word_re})'
dec_pattern = re.compile(dec_re)
func_pattern = re.compile(r'^'+dec_re+args_re+':')
label_pattern = re.compile('#'+dec_re+fr'\({word_re}\)'+':')

alloc_re = fr'\[{exp_re}\]+'	# shape and unit alloc later
alloc_pattern = re.compile(alloc_re+word_re)

indent = ''
expect_indent = False

# raise TabError('inconsistent use of tabs and spaces.')
for line_no, line in enumerate(file, 1):
	curr_indent = space_pattern.match(line)[0]
	same_level  = curr_indent == indent
	isDedent = indent.startswith(curr_indent)

	if expect_indent:
		if same_level or isDedent: raise IndentationError('expected indent block.')
		indent = curr_indent
	elif not same_level:
		if isDedent: indent = curr_indent
		else: raise IndentationError('unexpected indent block.')

	func_head_match  =  func_pattern.match(line)
	label_head_match = label_pattern.match(line)
	head = func_head_match or label_head_match
	if head: expect_indent = bool(blank_pattern.match(line[head.span[1]:]))
