# README

## Variables

### Integers

A variable is an unsigned integer of $2^n$ bits and initialised as `<n>name`.

So, for example to initialise a 32-bit integer variable called `orange`, you'd type `5orange`, since $2^5=32$.

This $n$ is an integer that ranges from 0-8 (both inclusive) which means we can have variables that range from being 1-bit to 256-bit.

```lua
0bit
1crumb
2nibble
3byte
4word
5dword
6qword
7sixteenBytes
8thirty2Bytes
```

Since the initialisation has no spaces, the delimiter to differentiate initialisations is whitespace. You can initialise multiple variables of different sizes in the same line.

### Arrays

Adding a number enclosed in square brackets to the start of the initialisation creates an array of that length.

So, `[10]6apples` creates an array called `apples` with 10 elements in it, and each element is a 64-bit integer.

This can be done recursively to create multidimensional arrays.

`[10][10]3guavas` is a 10 by 10 matrix of bytes.

### Variable Length Arrays (or as I like to call them: "varrs")

The length of arrays can't be changed. To make it changeable, you need to initialise it differently to make a varr instead. This is done by replacing a squared number with a digit $v$ from 0-8. (`[10][10]3guavas` would become `223guavas` or `2[10]3guavas` or `[10]23guavas`, based on what is required)

$v$ represents how many bits is required to represent the length of the varr. `3` means $2^3=8$ bits to represent the length, `2` means $2^2=4$. (just like integer initialisations)

The syntax to change the length is to add a number enclosed in square brackets before the variable name. (like initialising an array)

So, if `guavas` is initialised as `2[10]3guavas`, you'd make it a 10 by 10 matrix with the following:

```lua
[10]guavas
```

Here, the length should be capable of being represented with $2^2=4$ bits as `guavas` was initialised with $v=2$.

The length can be any expression that can be represented in $2^v$.

So if `peach` is initialised as `2peach`, we can change the length of `guavas` to `peach` like so:

```lua
[peach]guavas
```

Varrs are dynamically allocated, and every time the length is changed, it is first deallocated and then reallocated to fit the new requested memory.

This means that changing the length of a varr will erase its contents. So, to keep the old contents you would store it elsewhere first.

## Functions

## Labels

