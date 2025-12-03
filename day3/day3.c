#include <stdio.h>
#include <math.h>

long long getDigit(char line[100], int i) {
  return line[i] - 48;
}

long long getRest(char line[100], int i) {
  long long ret = 0;
  for (; i < 100; i++) {
    ret *= 10;
    ret += getDigit(line, i);
  }

  return ret;
}

long long max(long long a, long long b) {
  return a > b ? a : b;
}

long long sol(char line[100], int n) {
  // let dp[i][n] denote the max joltage only considering index i onwards, with n digits
  long long dp[100][n + 1];

  for (int i = 0; i < 100; i++) {
    dp[i][0] = 0;
    if (100 - i < n + 1) {
      dp[i][100 - i] = getRest(line, i);
    }
  }

  for (int i = 1; i < 100; i++) {
    for (int j = 1; j < n + 1; j++) {
      if (j > i) {
        continue;
      }
      dp[99 - i][j] = max(dp[99 - i + 1][j], dp[99 - i + 1][j - 1] + getDigit(line, 99 - i) * pow(10, j - 1));
    }
  }

  return dp[0][n];
}

int main() {
  FILE *fptr = fopen("3", "r");

  if (fptr == NULL) {
    printf("Error opening file\n");
    return 1;
  }

  char line[100] ;
  int part1 = 0;
  long long part2 = 0;
  while (fscanf(fptr, "%s", line) == 1) {
    part1 += sol(line, 2);
    part2 += sol(line, 12);
  }

  printf("Part 1: %d\n", part1);
  printf("Part 2: %lli", part2);
}
