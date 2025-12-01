# AOC2025 Solutions

Here are my solutions to [AOC2025](https://adventofcode.com/2025). I aim to use
a different language every day.

## Day 1: Uiua

From Uiua's [website](https://www.uiua.org/):

> Uiua (wee-wuh) is a general purpose array-oriented programming language with a
> focus on simplicity, beauty, and tacit code.

My solution for both parts is just 109 bytes:

```code
&fras"1"
⬚0+[50]×⊙≡(˜ⁿ¯1=@L↙1°□)⊸≡(⋕↘1°□)⊜□⊸≠@\n
A←◿100+
B←/+=0\A
C←/+≡(/+°□=0)A⊃(≡□↘¯1\+)(≡(□+⇡⟜(>0))↘1)
⊃C B
```

Yes this looks incomprehensible, but that is just cause you don't understand the
glyphs. If you have worked in a functional language before, I would say its
relatively easy to pick up. I had a lot of fun figuring out how to solve this
with Uiua and would recommend you to learn it too through the
[language tutorial](https://www.uiua.org/tutorial/Introduction).
