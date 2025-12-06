# Day 6 Uiua solve

Here is an explanation of my Uiua code for day 6. You may view my code with
syntax highlighting on the interactive editor on the Uiua website
[here](https://www.uiua.org/pad?src=0_18_0-dev_3__JmZyYXMiNiIK4oqc4oiY4oq44omgQFxuCuKfnCjiipziiqLiirjiiaBAIOKKoykK4o2J4oaYwq8xCuKKnCjilqHii5Up4oq4KOKJoDDiiaEvK-KJoEAgKQovK8uc4omh4peHKOKorC8rL8OX4oqiPUAqKQo=).

## Brief introduction to Uiua

Functions in Uiua aren't directly applied to arguments like in conventional prog
langs, instead the arguments live on a stack, and functions are applied to them
and transform them in place.

Another thing about Uiua is it is primarily an array programming language,
meaning the primary data structure are arrays and most functions are built to
efficiently manipulate them, Uiua also looks at how your functions are
compounded together and compiles these functions down into optimized SIMD
instructions, so it's really fast when used properly.

Uiua code is read line by line, each line is read right to left. When Uiua sees
a literal value, it pushes it directly to the stack. For example, if your code
was `1 2`, then 2 gets pushed to the stack first, then 1. So `+ 1 2` returns 3.

Uiua has 4 main data types: number, complex, char, and box. number and char are
self explanatory, complex is just complex numbers, and box is just like a
container object, that stores some value which can be anything, even arrays.
Values in arrays must be of a single data type, and can be multi dimensional.

Many functions in Uiua are also _pervasive_ (think numpy arrays), so
`mult 2 [1 2 3 4]` produces the array `[2 4 6 8]`

## Code explanation

Now I'll explain my code, line by line

```
&fras"6"
⊜∘⊸≠@\n
⟜(⊜⊢⊸≠@ ⊣)
⍉↘¯1
⊜(□⋕)⊸(≠0≡/+≠@ )
/+˜≡◇(⨬/+/×⊢=@*)
```

The first line just reads from the file called 6 and pushes it to the stack,
nothing fancy here. Note that strings in Uiua are just arrays of characters.

The next line `⊜∘⊸≠@\n` parses the input. Ill replace the glyphs with their
names to make it more readable. This line is `partition identity by neq @\n`.
The `@\n` at the end is just the new line character. As I mentioned above,
literal values gets pushed onto the stack, so now our stack looks something like

1.Some really long array of characters \
0.`@\n`, the newline character

Since there is no bool data type, != just returns 1 if neq and 0 otherwise. !=
is also a pervasive function, so `≠ @- "This-is-a-string"` will return the array
`[1 1 1 1 0 1 1 0 1 0 1 1 1 1 1 1]`.
[Try it out here](https://www.uiua.org/pad?src=0_18_0-dev_3__4omgIEAtICJUaGlzLWlzLWEtc3RyaW5nIgo=)

So `≠@\n` just transforms the string into an array of 1's and 0's where the
newlines are replaced with 0 and the other characters are 1. But once we apply
this function, our string input is gone, so we need to make use of a function
modifier called `by` that modifies the function to keep it's last argument on
the stack after its outputs. So when we do `by neq @\n`, our stack now looks
like this:

1.Some really long array of characters \
0.Some really long array of 1s and 0s

Lastly, I'll just copy paste what the partition function does from the docs:

```
Takes a function and two arrays.

The arrays must be the same ⧻ length.

The first array is called the "markers". It must be rank 1 and contain integers.

Consecutive rows in the second array that line up with groups of the same key in the markers will be grouped together.

Keys ≤0 will be omitted.

The function then processes each group in order. The result depends on what the function is.
```

So something like `partition identity  [0 0 2 2 1 1 3 3] [1 2 3 4 5 6 7 8]` will
return a multidimensional array with 3 rows `[[3 4] [5 6] [7 8]]`

Since partition makes use of the function provided and applies that function to
each group in the new array, if instead we did
`partition (mult 2)  [0 0 2 2 1 1 3 3] [1 2 3 4 5 6 7 8]`, it will multiply each
group by 2 to produce `[[3 4] [5 6] [7 8]]`.

The idiom `partiton identity by neq` is really useful for splitting strings, in
fact the Uiua formatter automatically converts `pibm` into `⊜∘⊸≠`.

Now thanks to the not equals function, we can partition our string input by the
newlines, so thats all `⊜∘⊸≠@\n` does, it just splits the input into an array of
lines.

`⟜(⊜⊢⊸≠@ ⊣)` is `on (partition first by neq @\space last)`

This line is very similar to the previous one, except now there is a `on`
modifier to the whole function. `on` is very similar to `by`, except it keeps
the last argument before its outputs.

This partition function splits by white space instead of new lines, and acts on
the last row of the input, thanks to the `last` function. So this basically just
parses the operator line in the input. The reason we use `first` instead of
`identity` is because otherwise the partition function would put each op
character into its own array. Now our stack looks like:

1.Array of operator characters (Recall `on` puts this after the original
arguments) \
0.Array of lines from the input

The next line `⍉↘¯1` is quite simple, it is just `transpose drop negate 1`.

`negate 1` just produces -1 (you can’t use - as the unary negation operator
because - is used to represent minus).

Drop is a function that takes a number and an array, and drops that number of
elements from that array, and returns the new array. `drop negate 1` will just
drop from the end instead of the start. Since the top of our stack is the input
split by lines, we are basically just dropping the line of operators, retaining
just the lines of numbers.

Lastly, we transpose this new array, so that the columns are now rows, making it
easier to work with. Recall that strings are just character arrays, so that’s
why transpose works.

The next line `⊜(□⋕)⊸(≠0≡/+≠@ )` is
`partition (box parse) by (neq 0 rows reduce plus neq @\space) `

It looks a bit more complicated, but all it does is to group our array of
numbers and convert them from string to numbers.

Let’s focus on the first part on the right
`(neq 0 rows reduce plus neq @\space)`.

`neq` also works on multidimensional arrays, let’s say the first few rows of the
array is

```
[
  “1234"
  " 567”
  “  89”
  “    “
]
```

`neq @\space` will transform it to

```
[
  [1 1 1 1]
  [0 1 1 1]
  [0 0 1 1]
  [0 0 0 0]
]
```

now when we call `rows reduce plus` on this array, what we are doing is just
mapping the `reduce plus` function into each row of the array, basically just
summing each row. Continuing with the above example input, we will get
`[4 3 2 0]`. Now we see that the strings that correspond to `”    “` just gets
reduced to 0, while the other strings of numbers are non zero. We can apply
another `neq 0` to it and we end up with `[1 1 1 0]` this is perfect for our
partition function, allowing us to group numbers in the same column on the
original input.

Lastly, the function we apply to each group in the partition is `box parse`.
Parse will parse each string in the group into numbers, ignoring leading and
trailing spaces. Now we use box to wrap each array in a container, this is
needed because each group of numbers may be of different length, so they can’t
be contained in the array. Wrapping each group in a box prevents this issue.

The last line `/+˜≡◇(⨬/+/×⊢=@*)` is actually quite simple. It is
`reduce plus backwards rows content (switch reduce plus reduce mult first = @*)`

the inner function `switch reduce plus reduce mult first = @*` conditionally
chooses whether to apply the reduce add function or the reduce mult function
depending on whether our operator is a \* or a +. This function expects the
operator to be in front of the stack first, followed by the array of numbers.

Next we have the `content` modifier, which just unboxes the input before running
our switch function above.

Next we have `backwards rows`, the backwards flips the order of the first 2
inputs on the stack, which is why we can assume the operator character is in
front of the array of numbers. One nice thing about rows is it can detect the
number of input arguments that the function to be mapped takes, since it notices
our function acts on two inputs, it does something like a zip over the two
arrays on the stack.

Now when we put all this together, we have an array that has applied the
operator to each column of numbers!

Then we just wrap it up with a `reduce plus` to add it all up, and Uiua prints
the value left on the stack
