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
