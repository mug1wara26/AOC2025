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
