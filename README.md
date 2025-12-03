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

## Day 2: Chez scheme

I love S-Expressions, in contrast with yesterday's solution, today's solution is
76 lines long.

```scheme
(define (split-string s delim)
  (letrec ([run
    (lambda (xs curr acc)
      (if (null? xs)
        (reverse (cons (list->string (reverse curr)) acc))
        (if (equal? (car xs) delim)
          (run (cdr xs) '() (cons (list->string (reverse curr)) acc))
          (run (cdr xs) (cons (car xs) curr) acc))))
  ]) (run (string->list s) '() '())))

(display "enter your puzzle input: ")
(define puzzle (get-line (current-input-port)))

(define parsed (map (lambda (s) (map string->number (split-string s #\-))) (split-string puzzle #\,)))

;; inclusive end
(define (range start end)
  (map (lambda (x) (+ x start)) (iota (- end start -1))))

(define (log10 n)
  (/ (log n) (log 10)))

(define (num-digits n)
  (inexact->exact (floor (1+ (log10 n)))))

(define (split-num n)
  (let [(delim (expt 10 (/ (num-digits n) 2)))]
    (cons (floor (/ n delim)) (mod n delim))))

(define (invalid n)
  (if (odd? (num-digits n))
    #f
    (let [(x (split-num n))]
      (= (car x) (cdr x)))))


;; x is number of digits in each split
(define (split-num2 n x)
  (letrec [(run (lambda (n acc)
    (if (<= (num-digits n) x)
      (cons n acc)
      (let [(delim (expt 10 x))]
        (run (floor (/ n delim)) (cons (mod n delim) acc))
      ))
  ))] (run n '())))

(define (invalid2 n)
  (letrec [(num (num-digits n)) (run (lambda (x)
    (if (= x 0)
      #f
      (if (and (zero? (mod num x)) (apply = (split-num2 n x)))
        #t
        (run (1- x))
      )
    )
  ))] (run (1- (num-digits n))))
)

(define (sol parsed invalid)
  (fold-left
    (lambda (x y)
      (+ x (fold-left
        (lambda (x y)
          (if (invalid y)
            (+ x y)
            x))
        0
        (apply range y))))
    0
    parsed))

(display (sol parsed invalid))

(newline)

(display (sol parsed invalid2))
```

## Day 3: C and Uiua

For day 3, I solved it first in C using a typical DP solution. Then I solved it
again in Uiua using a greedy approach. The DP solution is quite boring so I
won't paste it here, but the Uiua solution is just 69 bytes!

```
&fras"3"
⊜∘⊸≠@\n
A←/+≡(⋕≡⊡⊙¤-1↘1⊸˜\(++1⊙(⊢⍖˜↘)⟜↘))¤⊂[0]+1⇌⇡¯
⊃(A12|A2)
```
