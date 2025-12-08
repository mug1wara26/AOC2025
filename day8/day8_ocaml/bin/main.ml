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
                      |> List.map (fun s -> int_of_string (String.trim s)) in
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
