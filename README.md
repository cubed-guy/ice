# Intro? Preface? Disclaimer? idk

This language/readme doesn't focus on making things easy for beginners. If it ends up being, then good, but it isn't a priority.

The aim is ease of programming. Here's the idea of what _could_ make it easier. We'll find out if it actually makes it easier once it's done.

# Variables

Data types are aimed to be as basic as possible while still providing enough functionality to be Turing complete and not too obscure to be usable.

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

*The following sections introduce more things to the start of the declaration. We'll refer to what comes before the variable name in a declaration as the "declaration expression" from now (or `declexp` for short). Eg. The `declexp` for `[4][5]6mangoes` is `[4][5]6`.*

## Variable Length Arrays (or as I like to call them: "varrs")

The length of arrays can't be changed. To make it changeable, you need to declare it as a varr instead. This is done by replacing a squared number with a digit `v` from 0-8 (`[10]6apples` would become `26apples`). The length of the varr is represented as a 2<sup>v</sup>-bit integer.

The length is changed by adding a number enclosed in square brackets before the variable name. So, if `apples` is declared as `26apples`, you'd make it 10 long with:

```lua
[10]apples
```

Since the length can be represented as a 2<sup>v</sup>-bit integer, we can use an integer variable declared as `<v>name` in the brackets. So if `2boxes` was declared, the length of `apples` can be set to `boxes` like so:

```lua
[boxes]apples
```

Varrs are dynamically allocated, and every time the length is changed, it is first deallocated and then reallocated to fit the new requested memory.

This means that changing the length of a varr will erase its contents, so to keep the old contents you would store it elsewhere first.

## Pointers

There are two types of pointers - full pointers and size pointers.

### Full Pointer

Full pointers associate the `declexp` to the pointed data. The data that is being pointed to will be treated the same as regular data with that `declexp`.

A full pointer is declared with `*` in the `declexp`. A pointer to `[10][10]3guavas` will be `*[10][10]3guavaPointer`. It can also be declared like a varr. Thus, a pointer to `[10][10]3guavas` can also be `*223guavarrPointer`.

A full pointer declared like a varr is actually a varr itself. This means that a full pointer pointing to an array _is_ a varr, and the `declexps` `223` and `*223` mean the same thing.

# Functions

# Labels

