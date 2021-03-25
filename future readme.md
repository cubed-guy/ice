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

Ownership only can be *transferred* from pointer to pointer, and not copied. This makes pointers unique owners. (There exists a workaround though, but why would I share methods of causing unintended behaviour.)

### Assignments

Here is the place-holder syntax for the different types of assignments:

```lua
varL = varR          -- `varL` gets the data of `varR`
varL = pointerR      -- `varL` gets the data `pointerR` points to
pointerL = varR      -- `pointerL` points to `varR`
pointerL = pointerR  -- `pointerL` points to the data `pointerR` points to
pointerL := pointerR -- `pointerL` points to the data `pointerR` points to and ownership is transferred
pointerL -> pointerR -- data pointed by `pointerR` gets data pointed by `pointerL`
```

## Functions

Functions are defined with headers similar to variable declarations.

```lua
[56]4get_this(43string, 3chr):
	-- some code
```

Omit the type prefix if there is no return type.

The arguments are part of the function scope; they can be declared in the header or the body.

## Labels

A label is a collection of methods. A variable gets associated with a label during compile time. This introduces an object-oriented aspect with absolutely no sacrifice in run-time performance.

Also, since it's associated during compile-time, it can change throughout the code; a variable can have a label in one place in the code and a different label somewhere else.

