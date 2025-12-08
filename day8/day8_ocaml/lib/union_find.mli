type 'a t = {
  parent : ('a, 'a) Hashtbl.t;
  rank : ('a, int) Hashtbl.t ;
}

val create : int -> 'a t
val find : 'a t -> 'a -> 'a
val union : 'a t -> 'a -> 'a -> unit
