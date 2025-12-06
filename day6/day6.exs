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
