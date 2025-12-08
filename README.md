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

## Day 6: Elixir

Today, I initially solved with Python, then solved part 2 with Uiua and Elixir
cause part 1 is pretty boring... that counts right?

View my Uiua code
[on the iteractive editor](https://www.uiua.org/pad?src=0_18_0-dev_3__JmZyYXMiNiIK4oqc4oiY4oq44omgQFxuCuKfnCjiipziiqLiirjiiaBAIOKKoykK4o2J4oaYwq8xCuKKnCjilqHii5Up4oq4KOKJoDDiiaEvK-KJoEAgKQovK8uc4omh4peHKOKorC8rL8OX4oqiPUAqKQo=).

```
&fras"6"
⊜∘⊸≠@\n
⟜(⊜⊢⊸≠@ ⊣)
⍉↘¯1
⊜(□⋕)⊸(≠0≡/+≠@ )
/+˜≡◇(⨬/+/×⊢=@*)
```

I also explained how my Uiua code worked on the NUS Hackers AOC discord channel,
so I pasted it over to a readme file [in the day6 folder](/day6/README.md)

Here is my part 2 Elixir code:

```elixir
{:ok, file} = File.read("6")
inputs = String.split(file, "\n")
nums = Enum.map(Enum.slice(inputs, 0..3), fn x -> String.graphemes(x) end)
zipped = Enum.zip_with(nums, fn [w, x, y, z] -> [w, x, y, z] end)
ops = String.split(Enum.at(inputs, 4))

defmodule Part2 do
  def solve([], [], acc) do
    acc
  end

  def solve([nums | rest_nums], [op | rest_ops], acc) do
    if op == "*" do
      solve(rest_nums, rest_ops, acc + Enum.reduce(nums, fn x, y -> x * y end))
    else
      solve(rest_nums, rest_ops, acc + Enum.sum(nums))
    end
  end

  def parse([], acc) do
    Enum.reverse(acc)
  end

  def parse([head | tail], [acc_head | acc_tail]) do
    if head == [" ", " ", " ", " "] do
      parse(tail, [[] | [acc_head | acc_tail]])
    else
      parsed = String.to_integer(String.trim(List.to_string(head)))
      parse(tail, [[parsed | acc_head] | acc_tail])
    end
  end

  def parse(nums) do
    parse(nums, [[]])
  end
end

IO.puts(Part2.solve(Part2.parse(zipped), ops, 0))
```

## Day 7: Go and Uiua

Day 7 was super easy, my Go solution was pretty much just a port of my Python
solution.

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	filePath := "7"

	file, _ := os.Open(filePath)
	defer file.Close()

	scanner := bufio.NewScanner(file)

	scanner.Scan()
	line := scanner.Text()

	beams := make([]int, len(line))
	beams[strings.IndexByte(line, 'S')] = 1
	part1 := 0

	for scanner.Scan() {
		line := scanner.Text()
		new_beams := make([]int, len(line))

		for i, r := range line {
			if r == '^' {
				if beams[i] != 0 {
					new_beams[i-1] += beams[i]
					new_beams[i+1] += beams[i]
					part1 += 1
				}
			} else {
				new_beams[i] += beams[i]
			}
		}

		beams = new_beams
	}

	part2 := 0

	for _, n := range beams {
		part2 += n
	}

	fmt.Println(part1)
	fmt.Println(part2)
}
```

My Uiua solution is the shortest one yet, when golfed it is just 59 bytes! The
solution method also slightly differs, as I iterate through the input, I keep
track of the number of beams in each column. For each row in the input, I mask
the beams the hit a splitter, apply a rotate left and right to simulate them
splitting, and add them up together with the beams that did not hit the
splitters. At the end of the iteration I can just do a `reduce add`.

```
0
&fras"7"
⊜∘⊸≠@\n # Parse by new line
=@S°⊂   # create array of 0s except for start
˜⊙∘
Part₁ ← +/+≠0× # Count number of beams that hit splitters
# Get beams that hit splitters,
# rotate 1 and rotate -1,
# add together with beams that miss splitters
Part₂ ← ++⊃(⊃(↻1|↻¯1)×|×¬)
∧(⊃(Part₂|Part₁)=@^)
/+
```

## Day 8: OCaml

My favourite day so far, probably cause its the hardest so far. The
implementation is quite simple, stick all pair combinations in a heap, where the
priority is the euclidean distance between the two points, then use a UFDS to
efficiently track the circuits. Luckily OCaml added priority queues to the
standard library about 2 months ago, but there's no UFDS so I implemented my
own.

UFDS:

```ocaml
type 'a t = {
  parent : ('a, 'a) Hashtbl.t;
  rank : ('a, int) Hashtbl.t ;
}

let create (n : int) : 'a t = {
  parent = Hashtbl.create n;
  rank = Hashtbl.create n;
}

let rec find ds x = match Hashtbl.find_opt ds.parent x with
  | Some parent ->
      if parent = x then parent
      else begin
        let parent = find ds parent in
        Hashtbl.replace ds.parent x parent;
        parent
      end;
  | None -> (
      Hashtbl.add ds.parent x x;
      Hashtbl.add ds.rank x 0;
      x
    )

let union ds a b =
  let a = find ds a in
  let b = find ds b in
  if a <> b then
    let a_rank = Hashtbl.find ds.rank a in
    let b_rank = Hashtbl.find ds.rank b in
    if a_rank < b_rank then
      Hashtbl.replace ds.parent a b
    else begin
      Hashtbl.replace ds.parent b a;
      if a_rank = b_rank then Hashtbl.replace ds.rank a (a_rank + 1)
    end
```

Main solution:

```ocaml
open Day8

module Prio : Pqueue.OrderedType with type t = int = struct
  type t = int
  let compare = compare
end

module PrioQueue = Pqueue.MakeMinPoly(struct
  type 'a t = Prio.t * 'a
  let compare (p1, _) (p2, _) = Prio.compare p1 p2
end)

exception Value_not_found of string

let () =
  let start_time = Sys.time() in
  let pq = PrioQueue.create() in
  let ic = open_in "../8" in
  let rec read_lines ic acc =
  match input_line ic with
  | exception End_of_file -> acc
  | line ->
      let nums = line |> String.split_on_char ','
                      |> List.map (fun s -> int_of_string ) in
      match nums with
      | [x; y; z] -> read_lines ic ((x, y, z) :: acc)
      | _ -> failwith ("Invalid line: " ^ line)
  in
  let result = read_lines ic [] in

  let rec all_pair_combinations coords acc = match coords with
    | [] -> acc
    | hd :: tl -> all_pair_combinations tl ((List.map (fun x -> (hd, x)) tl) @ acc)
  in

  let square x = x * x in
  let distance (x1, y1, z1) (x2, y2, z2) = square (x1 - x2) + square (y1 - y2) + square (z1 - z2) in

  List.iter (fun x -> PrioQueue.add pq (distance (fst x) (snd x), x)) (all_pair_combinations result []);

  let get_x (x, _, _) = x in
  let uf = List.length result |> Union_find.create in

  let rec solve i n =
    let pair = match PrioQueue.pop_min pq with
      | Some (x, y) -> y
      | None -> raise (Value_not_found "Expected a pair")
    in
    if i = 1000 then begin
      Hashtbl.to_seq_keys uf.parent
      |> Seq.iter (fun x -> Union_find.find uf x |> ignore);

      Hashtbl.to_seq_values uf.parent
      |> Seq.fold_left (fun acc x -> (match Hashtbl.find_opt acc x with
      | Some v -> Hashtbl.replace acc x (v+1)
      | None -> Hashtbl.add acc x 1
      ); acc)
      (Hashtbl.create 100)
      |> Hashtbl.to_seq_values
      |> List.of_seq
      |> List.sort (fun x y -> -(compare x y))
      |> List.take 3
      |> List.fold_left (fun x y -> x * y) 1
      |> Printf.printf "Part 1: %d\n"
    end;

    if Union_find.find uf (fst pair) <> Union_find.find uf (snd pair) then begin
      Union_find.union uf (fst pair) (snd pair);
      if n = 2 then
        Printf.printf "Part 2: %d\n" ((fst pair |> get_x) * (snd pair |> get_x))
      else
        solve (i + 1) (n - 1)
    end
    else solve (i + 1) n
  in

  solve 0 (List.length result);
  Printf.printf "Execution time: %f seconds\n" (Sys.time() -. start_time);
```
