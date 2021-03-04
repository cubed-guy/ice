# Ice

Ice is a compiled language with pythonic code blocks. The fundamental data structures are unsigned integers, static and dynamic arrays, typed and void pointers and structs.

The type of a variable is stated with type prefixes as below.

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

3. **Dynamic arrays**: Using a digit `0-6` instead of the enclosed number makes it a dynamic array. The digit refers to the size of the integer used to store the length of the array (similar to the number of bits used for an integer using the integer size prefix)

4. **Typed pointers**: Prefixing this sequence of digits and brackets with an asterisk makes it a pointer (`*[56]4that`). Dynamic arrays are always pointers and they store the address along with the array length. The compiler knows the type information and is not stored during run-time.

5. **Void Pointers**: Prefixing the integer size prefix with a carat `^` makes it a void pointer that stores the size and the address of the data pointed to.

6. **Structs**: Replacing the integer size prefix with comma separated type prefixes enclosed within parenthesis makes a struct. *(i might make it so you can name the fields of a struct)*

Here is the place-holder syntax for the different types of assignments:

```lua
varL = varR          -- `varL` gets data of `varR`
varL = pointerR      -- `varL` gets data pointed by `pointerR`
pointerL = varR      -- `pointerL` points to `varR`
pointerL = pointerR  -- `pointerL` points to data pointed by `pointerR`
pointerL := pointerR -- `pointerL` points to data pointed by `pointerR` and is its new owner if `pointerR` was
pointerL -> pointerR -- data pointed by `pointerR` gets data pointed by `pointerL`
```