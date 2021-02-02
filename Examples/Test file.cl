-- Here's just a comment. It should be ignored.
		-- Here's a comment, but there's some whitespace too. This also, should be ignored.

3newVar
[2]3newArr -- inline comment

-- multiple assignments in a line
33newVarr *223guavarrPointer

#33thisLabel:
-- test comment
	3firstFunc(self, 3arg): -- oh no, arguments aren't considered yet
	  3localVar = 2
	  localVar += arg
	  return localVar

	-- here's a comment INSIDE the label
	[2]3secondFunc(self):
		3firstReturn
		-- comment in the function
		3secondReturn
	-- with different indentation
		firstReturn = 3
		secondReturn = 4

		[2]3out

		out[0] = firstReturn
		out[1] = secondReturn
		return out

#thisLabel newVarr

#*223guavarrLabel(thisLabel): -- Inheritence. This too isn't implemented yet.
-- so this won't cause problems, though it should
-- need to add this to the data dict as well
	2orange(self): return 2 -- inline block

	-- what about a function that doesn't return a value?
	-- not yet implemented
	procedure(self, 2w, 2h, 3val):
		[w][h]self
		for 2x in range(w): -- not sure yet how for should work
			-- now, an inline control block
			for 2y in range(h): 3oval = val; self[x][y] = oval
	-- Right, the first indentation level under a label head must contain
	-- only function heads. Need to implement that as well.

3loneFunction(2x, 2y):
	return guavarrPointer[x][y]

#guavarrLabel guavarrPointer

guavarrPointer.procedure(3, 6, 12)

newVar = loneFunction(2, 0)

print(str(newVarr.firstFunc(newVar)))
-- Some sort of *args syntax can be implemented.
-- Not the same syntax of course, because `*` is used for pointers.