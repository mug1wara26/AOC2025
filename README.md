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

I love S-Expressions.

In contrast with yesterday's solution, today's solution is 76 lines long.

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

We basically just find the index of the max character from \[0:-11\], lets call
this index `n`. Then we find the index of the max character from \[n:-10\], and
keep repeating this procedure until we get the all 12 characters. Uiua has a
handy function called [`fall`](https://www.uiua.org/docs/fall) that returns the
indices of the list if its elements were sorted in descending order, while this
is `O(n log n)`, if we use the [`first`](https://www.uiua.org/docs/first)
function to only get the max index, the Uiua interpreter optimizes it to `O(n)`.

## Day 4: Rust

I originally solved today's solution with a simple brute force in Python because
I was busy. After reaching home at midnight, I decided I did not want to waste
Python on such an easy day, so I learnt Rust and wrote a more efficient
solution.

```rust
use std::fs;

fn get_surrounding_rolls(contents: &[Vec<u8>], row: usize, col: usize) -> Vec<(usize, usize)> {
    let height = contents.len();
    let width = contents[0].len();

    let row_start = row.saturating_sub(1);
    let row_end = (row + 2).min(height);
    let col_start = col.saturating_sub(1);
    let col_end = (col + 2).min(width);

    contents[row_start..row_end]
        .iter()
        .enumerate()
        .flat_map(|(i, r)| {
            r[col_start..col_end]
                .iter()
                .enumerate()
                .filter(move |&(j, &cell)| {
                    cell == b'@' && (row_start + i, col_start + j) != (row, col)
                })
                .map(move |(j, _)| (row_start + i, col_start + j))
        })
        .collect()
}

fn main() {
    let binding = fs::read_to_string("4").expect("read the file");
    let mut contents: Vec<Vec<u8>> = binding.lines().map(|s| s.as_bytes().to_vec()).collect();

    let height = contents.len();
    let width = contents[0].len();

    let mut indices = Vec::new();
    for row in 0..height {
        for col in 0..width {
            if contents[row][col] == b'@' && get_surrounding_rolls(&contents, row, col).len() < 4 {
                indices.push((row, col));
                contents[row][col] = b'.';
            }
        }
    }

    let mut total = indices.len();

    println!("Part 1: {}", total);

    while !indices.is_empty() {
        let mut temp = Vec::new();
        for (r, c) in indices {
            for (row, col) in get_surrounding_rolls(&contents, r, c) {
                if get_surrounding_rolls(&contents, row, col).len() < 4 {
                    temp.push((row, col));
                    contents[row][col] = b'.';
                }
            }
        }

        total += temp.len();
        indices = temp;
    }

    println!("Part 2: {}", total);
}
```

## Day 5: Zig

Once again, I initially solved it in Python then revisited the problem at the
end of the day in a new language. Having an implementation reference is really
useful when trying to solve these days with a completely new language so I think
I'll be doing the same for future days with foreign languages. Since the Zig
implementation is quite long, and the logic is basically the same as the Python
one, I'll just paste the Python solution here

```py
inp = [i for i in open("5").read().splitlines()]
ranges = [list(map(int, i.split("-"))) for i in inp[: inp.index("")]]
ids = map(int, inp[inp.index("") + 1 :])

total = 0
for i in ids:
    for r in ranges:
        if r[0] <= i <= r[1]:
            total += 1
            break

print(f"part 1: {total}")

ranges.sort(key=lambda x: x[0])

i = 0
while i < len(ranges) - 1:
    curr = ranges[i]
    next_range = ranges[i + 1]
    if next_range[0] <= curr[1] + 1:
        if next_range[1] > curr[1]:
            curr[1] = next_range[1]
        del ranges[i + 1]
    else:
        i += 1

print(f"part 2: {sum(map(lambda x: x[1] - x[0] + 1, ranges))}")
```
