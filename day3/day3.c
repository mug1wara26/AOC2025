#include <stdio.h>
#include <math.h>

long long getDigit(char line[100], int i) {
  return line[i] - 48;
}

long long sol(char line[100], int n) {
  // let dp[i][n] denote the max joltage only considering index i onwards, with n digits
  long long dp[100][n + 1];

  dp[99][0] = 0;
  dp[99][1] = getDigit(line, 99);
  for (int i = 1; i < 100; i++) {
    for (int j = 0; j < n + 1; j++) {
      if (j == i+1) {
        dp[99 - i][j] = dp[99 - i + 1][j - 1] + getDigit(line, 99 - i) * pow(10, j - 1);
        break;
      }
      if (j)
        dp[99 - i][j] = fmax(dp[99 - i + 1][j], dp[99 - i + 1][j - 1] + getDigit(line, 99 - i) * pow(10, j - 1));
      else
        dp[99 - i][0] = 0;
    }
  }

  return dp[0][n];
}

int main() {
  FILE *fptr = fopen("3", "r");

  char line[100];
  int part1 = 0;
  long long part2 = 0;

  while (fscanf(fptr, "%s", line) == 1) {
    part1 += sol(line, 2);
    part2 += sol(line, 12);
  }

  printf("Part 1: %d\n", part1);
  printf("Part 2: %lli", part2);
}
