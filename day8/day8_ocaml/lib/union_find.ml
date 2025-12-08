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
