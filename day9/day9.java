import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;

public class day9 {

    public static void main(String[] args) {
        List<Point> points = new ArrayList<>();
        Scanner sc = new Scanner(System.in);

        while (sc.hasNext()) {
            String[] line = sc.next().split(",");
            points.add(new Point(line));
        }

        sc.close();

        List<Line> verticals = new ArrayList<>();
        List<Line> horizontals = new ArrayList<>();
        long part1 = 0;

        for (int i = 0; i < points.size(); i++) {
            for (int j = i + 1; j < points.size(); j++) {
                part1 = Math.max(part1, Point.area(points.get(i), points.get(j)));
            }

            if (i % 2 == 0)
                verticals.add(new Line(points.get(i), points.get(i + 1)));
            else if (i + 1 < points.size())
                horizontals.add(new Line(points.get(i), points.get(i + 1)));
        }

        System.out.println(String.format("Part 1: %d", part1));

        verticals.sort(new Comparator<Line>() {
            @Override
            public int compare(Line arg0, Line arg1) {
                return arg0.p1.x - arg1.p1.x;
            }
        });
        verticals.sort(new Comparator<Line>() {
            @Override
            public int compare(Line arg0, Line arg1) {
                return arg0.p1.x - arg1.p1.x;
            }
        });

        horizontals.sort(new Comparator<Line>() {
            @Override
            public int compare(Line arg0, Line arg1) {
                return arg1.horizontalLength() - arg0.horizontalLength();
            }
        });

        Point mid1 = horizontals.get(0).getRightPoint();
        Point mid2 = horizontals.get(1).getRightPoint();

        if (mid1.y < mid2.y) {
            Point temp = mid2;
            mid2 = mid1;
            mid1 = temp;
        }

        int mid1_ylimit = 0;
        int mid2_ylimit = 0;

        for (Line line : horizontals) {
            int left = line.getLeft();
            int right = line.getRight();
            if (line.p1.y > mid1.y && left <= mid1.x && mid1.x <= right)
                mid1_ylimit = line.p1.y;
            if (line.p1.y < mid2.y && left <= mid2.x && mid2.x <= right)
                mid2_ylimit = line.p1.y;
        }

        long part2 = 0;

        for (Point point : points) {
            Point m = null;

            if (point.x >= mid1.x)
                continue;

            if (mid1.y <= point.y && point.y <= mid1_ylimit)
                m = mid1;
            else if (mid2.y <= point.y && point.y <= mid2_ylimit)
                m = mid2;

            if (m != null) {
                Point p1 = new Point(point.x, m.y);
                Point p2 = new Point(m.x, point.y);

                if (Point.area(m, point) > part2 && p1.inPolygon(verticals) && p2.inPolygon(verticals))
                    part2 = Point.area(m, point);
            }
        }

        System.out.println(String.format("Part 2: %d", part2));
    }
}

class Point {
    int x;
    int y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    Point(String[] line) {
        this.x = Integer.valueOf(line[0]);
        this.y = Integer.valueOf(line[1]);
    }

    static long area(Point p1, Point p2) {
        return Math.multiplyFull((Math.abs(p1.x - p2.x) + 1), (Math.abs(p1.y - p2.y) + 1));
    }

    // Assumes verticals are sorted.
    boolean inPolygon(List<Line> verticals) {
        int num_crossings = 0;

        Set<Integer> lows = new HashSet<>();
        Set<Integer> highs = new HashSet<>();

        for (Line line : verticals) {
            if (line.p1.x >= this.x)
                break;

            int lower = line.getLower();
            int higher = line.getHigher();
            if (lower <= this.y && this.y <= higher) {
                if (lower == this.y && highs.contains(this.y))
                    continue;
                if (higher == this.y && lows.contains(this.y))
                    continue;

                lows.add(lower);
                highs.add(higher);
                num_crossings += 1;
            }
        }

        return num_crossings % 2 == 1;
    }

    @Override
    public String toString() {
        return String.format("(%s, %s)", x, y);
    }
}

class Line {
    Point p1;
    Point p2;

    Line(Point p1, Point p2) {
        this.p1 = p1;
        this.p2 = p2;
    }

    int getLeft() {
        return Math.min(p1.x, p2.x);
    }

    int getRight() {
        return Math.max(p1.x, p2.x);
    }

    int getHigher() {
        return Math.max(p1.y, p2.y);
    }

    int getLower() {
        return Math.min(p1.y, p2.y);
    }

    Point getRightPoint() {
        return p1.x > p2.x ? p1 : p2;
    }

    int horizontalLength() {
        return Math.abs(p1.x - p2.x);
    }

    @Override
    public String toString() {
        return String.format("[%s, %s]", p1, p2);
    }
}
