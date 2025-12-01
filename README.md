# AOC2025 Solutions

Here are my solutions to [AOC2025](https://adventofcode.com/2025). I aim to use
a different language every day.

## Day 1: Uiua

From Uiua's [website](https://www.uiua.org/)

> Uiua (wee-wuh) is a general purpose array-oriented programming language with a
> focus on simplicity, beauty, and tacit code.

My solution for both parts is just 126 bytes:

```
&fras"1"
⬚0+[50]×⊙≡(˜ⁿ¯1=@L↙1°□)⊸≡(⋕↘1°□)⊜□⊸≠@\n
Part₁←/+=0\(◿100+)
Part₂←/+≡(/+°□=0)◿100+⊃(≡□↘¯1\+)(≡(□+⇡⟜(>0))↘1)
⊃Part₂Part₁
```
