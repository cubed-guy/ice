# Ice

Ice is a compiled language with pythonic code blocks and some unique features.

## Basic types

The type of a variable is stated with type prefixes as below. The fundamental data structures are unsigned integers, static and dynamic arrays, typed and void pointers and structs.

1. **Integers**: An integer is prefixed with a digit `0-6`. The integer will use the number of bits equal to two raised to the power of the prefixed number.
	
	| Prefix | Number of bits |
	| ------ | -------------- |
	| 0      | 1              |
	| 1      | 2              |
	| 2      | 4              |
	| 3      | 8              |
	| 4      | 16             |
	| 5      | 32             |
	| 6      | 64             |
	
2. **Static Arrays**: The integer size prefix can be prefixed with a number enclosed in square brackets to declare a static array of that length. You can prefix this similarly many times to create multidimensional arrays.
     ![](doc_images/array_declaration.png)
*an array of 56 16-bit integers called `this`*

3. **Dynamic arrays**: Using a digit `0-6` instead of the enclosed number makes it a dynamic array. The digit refers to the size of the integer used to store the length of the array (similar to the number of bits used for an integer using the integer size prefix)

4. **Typed pointers**: *(Look. 99.9% of all the code I've ever written is in python; I might do some stupid things with pointers and stuff. Don't laugh)*
     Prefixing this sequence of digits and brackets with an asterisk makes it a pointer (eg. `*[56]4that`). Dynamic arrays are always pointers and they store the address along with the array length. The compiler knows the type information, which is not stored during run-time.

5. **Void Pointers**: Prefixing the integer size prefix with a caret `^` makes it a void pointer that stores the size and the address of the data pointed to.

6. **Structs**: Replacing the integer size prefix with comma separated type prefixes enclosed within parenthesis makes a struct. *(i might make it so you can name the fields of a struct)*

Variables can be declared one or more times anywhere in a scope (which is different inside and outside functions). The type in all the declarations must match.

### Ownership of pointers

Every pointer has an ownership bit which tells whether it owns the data. If a pointer that owns data goes out of scope, the pointed data is dereferenced. Also, when an owning pointer is assigned different data, the owned data is also dereferenced.

Ownership only can be *transferred* from pointer to pointer, and not copied. This makes pointers unique owners. (There exists a workaround, but I won't tell you how to break a language I made.)

### Assignments

Here is the place-holder syntax for the different types of assignments:

```python
varL = varR          # `varL` gets the data of `varR`
varL = pointerR      # `varL` gets the data `pointerR` points to
pointerL = varR      # `pointerL` points to `varR`
pointerL = pointerR  # `pointerL` points to the data `pointerR` points to
pointerL := pointerR # `pointerL` points to the data `pointerR` points to and ownership is transferred
pointerL -> pointerR # data pointed by `pointerR` gets data pointed by `pointerL`
```

## Functions

Functions are defined with headers similar to variable declarations.

```python
[56]4get_this(43string, 3chr):
	# some code
```

Omit the type prefix if there is no return type.

The arguments are part of the function scope; they can be declared in the header or the body.

## Labels

A label is a collection of methods. A variable gets associated with a label during compile time. This introduces an object-oriented aspect with absolutely no sacrifice in run-time performance.

Also, since it's associated during compile-time, it can change throughout the code; a variable can have a label in one place in the code and a different label somewhere else.

A label is created using the `@` symbol followed by the shape of the variables you want to use with the label. Then you add the label name and a colon for a code block. All the methods for the label will go into the code block.

Take an example of a label `slippery` for variables of the shape `4`.

```python
@4slippery:
	slip(self):
		# There are built-in functions. Just like in python.
		print(self)
		print('Oh no the value just slipped into the screen!')
```

A label is assigned to a variable like how variables are declared in C or C++, but with the `@` symbol. Remember, variables don't have to be declared with a label. You can assign labels to variables. A variable can have a label in one part of your code and another in another part.

```
4guava = 34	# declaring a variable of shape `4`

@slippery guava	# the label has been assigned

guava.slip()	# the slip method of the slippery label is called for guava
```

Just like in python, the object is passed in as the `self` argument in the method. The above method call is equivalent to `@slippery.slip(guava)` directly calling the method of the label and passing the self argument explicitly.

Refer [the test file](Examples/Test%20file.ice) for syntax examples.
