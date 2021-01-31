# Cool Lang <sub><sup>(placeholder name)</sup></sub>

The language has been designed to have a one-to-one relation with assembly code for maximum performance, while still providing features to make it easy to code.

There is a sense of object orientation with a concept I call "label". A label is like a class, except we define only methods, no attributes. A label is not instantiated, but rather assigned to a variable. The advantage is that, based on the needs, a variable can be assigned different labels at different times.

To maintain performance and the one-to-one relation with assembly, labels are not assigned during runtime, *but during compile-time*. It is assigned to a variable based on *where* it is in the program and the method calls are simply converted to function calls with the appropriate variable as the `this` or the `self` argument. A quirk of compile-time label assignment is that labels need no constructor method as there is no instantiation nor are there any attributes.

I've also borrowed the data definition methods (aka `__dunder__` methods) and the indentation from Python, because that's what makes Python great (and that I am primarily a Python programmer).

Note that, unlike a class in Python or C++, the label is not the type of a variable. You may say the type *comprises* of the label and is only the label. Apart from defining how the data interacts with everything, we also need to define how it is stored. Here's that aspect of the data type.

## Integers

An unsigned integer of 2<sup>n</sup> bits is declared as `<n>name`. For example, `5orange` would declare a variable called `orange` which is a 2<sup>5</sup> = 32-bit unsigned integer.

`n` is an integer that ranges from 0-8 (both inclusive), which means we can have variables that range from being 1-bit to 256-bit.

```lua
0bit            --  1-bit uint
1crumb          --  2-bit uint
2nibble         --  4-bit uint
3byte           --  8-bit uint
4word           -- 16-bit uint
5dword          -- 32-bit uint
6qword          -- 64-bit uint
7sixteenBytes   --128-bit uint
8thirty2Bytes   --256-bit uint
```

Since the declaration has no spaces, any whitespace acts as a delimiter and you can declare multiple variables of different sizes in the same line.

## Arrays

Adding a number enclosed in square brackets to the start of the declaration creates an array of that length.

So, `[10]6apples` creates an array called `appleBoxes` with 10 elements in it, and each element is a 64-bit integer.

This can be done recursively to create multidimensional arrays.

`[10][10]3guavas` is a 10 by 10 matrix of bytes.

You can access elements of arrays by adding a number after the variable enclosed in square brackets. `apples[2]` will get the third element (indices start from 0) in `apples`.

*The following sections introduce more things to the start of the declaration. We'll refer to what comes before the variable name in a declaration as its "shape" from now. Eg. The shape for `[4][5]6mangoes` is `[4][5]6`.*

## Variable Length Arrays (or as I like to call them: "varrs")

The length of arrays can't be changed. To make it changeable, you need to declare it as a varr instead. This is done by replacing a squared number with a digit `v` from 0-8 (`[10]6apples` would become `26apples`). The length of the varr is represented as a 2<sup>v</sup>-bit integer.

The length is changed by adding a number enclosed in square brackets before the variable name. So, if `apples` is declared as `26apples`, you'd make it 10 long with:

```lua
[10]apples
```

Since the length can be represented as a 2<sup>v</sup>-bit integer, we can use an integer variable with shape `v` in the brackets. So if `2boxes` was declared, the length of `apples` can be set to `boxes` like so:

```lua
[boxes]apples
```

Varrs are dynamically allocated, and every time the length is changed, it is first deallocated and then reallocated to fit the new requested memory.

This means that changing the length of a varr will erase its contents, so to keep the old contents you would store it elsewhere first.

## Pointers

There are two types of pointers - shape pointers and size pointers.

### Shape Pointers

Shape pointers associate the shape to the pointed data. The data that is being pointed to will be treated the same as regular data with that shape. It is declared with `*` in the shape. A pointer to `[10][10]3guavas` will be `*[10][10]3guavaPointer`.

A pointer to `[10][10]3guavas` can also be `*223guavarrPointer`. In fact, a varr is a shape pointer, so `223` is the same as `*223`.

Since the `*` is also a part of the shape, we can point to pointers too. For example, `**3peach` is a shape pointer that points to a shape pointer pointing to a byte.

### Size Pointers

Size pointers associate only a size to the pointed data. They are declared using `^` followed by a digit (0-8) representing the number of bits it uses to store the size of the pointed data. To point to data with size, say 12, you would declare a size pointer as `^2watermelon` since 12 can be represented with 2<sup>2</sup>=4 bits.

This is useful to recursively point to pointers (in linked lists for examples) when you don't know how many pointers will be pointed to or there are just too many. If you wanted to recursively point 80 times to a byte, you would have to have a declaration that looks something like this:

```lua
********************************************************************************3watermelon
```

With size pointers you just need to reserve some space to store the size of a pointer and point to it.

```lua
^2watermelon
```

### Ownership

Every pointer has an ownership bit. When true, the pointer owns the data. This means that when the pointer dereferences the data or goes out of scope, the pointed data gets deallocated. In these cases the ownership bit is set to false.

Ownership can be only transferred from pointer to pointer, but cannot be copied. This is to avoid more than one pointer to own the same data (though there exists a workaround, but I won't discuss breaking my language here).

## Tuples

A tuple is a sequence of items of different shapes. The syntax for this is to replace the last number of the shape with a sequence of shapes enclosed in parentheses.

```lua
(2, 3)CherryAndBanana
```

We can also nest tuples.

```lua
([10]6, (2, 3))Apples_and_CherryAndBanana
```

Elements of a tuple can be accessed like in arrays but only literals are allowed (to make the language _faster_ and to assure the return shape _(not return type)_ during compile time).

## Functions

The function header should mention the shape of the return value. If none mentioned, it must not return a value.

```lua
3makeJuice(2apple):
	3juice
	-- more code
	return juice -- juice has the same shape as makeJuice so it's accepted
```

_Note: The shape of a variable needs to be mentioned with the variable anywhere at least once in a program. Every shape mentioned for a variable must be the same. If the shape of a variable is mentioned in a function (or its argument list), it will be treated as a local variable and can have a different shape within the function._

## Assignments

Here is the place-holder syntax for the different types of assignments (remember that varrs are pointers):

```sql
varL = varR          -- `varL` gets data of `varR`
varL = pointerR      -- `varL` gets data pointed by `pointerR`
pointerL = varR      -- `pointerL` points to `varR`
pointerL = pointerR  -- `pointerL` points to data pointed by `pointerR`
pointerL := pointerR -- `pointerL` points to data pointed by `pointerR` and is its new owner if `pointerR` was
pointerL -> pointerR -- data pointed by `pointerR` gets data pointed by `pointerL`
```