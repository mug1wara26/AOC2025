const fs = require("fs");

let memo = {};
let edges = {};

function num_paths(src, dst) {
  const key = `${src} ${dst}`;
  if (!(key in memo)) {
    ret = 0;

    edges[src].forEach((x) => {
      if (x === dst) ret += 1;
      else ret += num_paths(x, dst);
    });

    memo[key] = ret;
  }

  return memo[key];
}

fs.readFile("11", "utf8", (err, data) => {
  if (err) {
    console.log(err);
    return;
  }

  data.split("\n").forEach((line) => {
    if (line.length != 0) {
      let temp = line.split(":");
      edges[temp[0]] = temp[1].trim().split(" ");
    }
  });

  edges["out"] = [];

  console.log(`Part 1: ${num_paths("you", "out")}`);
  console.log(
    `Part 2: ${num_paths("svr", "fft") * num_paths("fft", "dac") * num_paths("dac", "out")}`,
  );
});
