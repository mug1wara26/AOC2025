const std = @import("std");
const fs = std.fs;
const twople = struct { start: i64, end: i64, };
const ArrayList = std.ArrayList;

fn compareTwople(_: void, a: twople, b: twople) bool {
    return a.start < b.start;
}

pub fn main() !void {
    const file = try fs.cwd().openFile("5", .{});
    const reader = file.reader().any();

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var buf: [1024]u8 = undefined;
    var ranges = ArrayList(twople).init(allocator);
    defer ranges.deinit();
    var ids = ArrayList(i64).init(allocator);
    defer ids.deinit();

    while (try reader.readUntilDelimiterOrEof(buf[0..], '\n')) |line| {
        if (line.len == 0) {
            break;
        }
        var it = std.mem.splitScalar(u8, line, '-');
        const range = twople{ .start = try std.fmt.parseInt(i64, it.next() orelse "" , 10), .end = try std.fmt.parseInt(i64, it.next() orelse "", 10) };
        try ranges.append(range);
    }

    while (try reader.readUntilDelimiterOrEof(buf[0..], '\n')) |line| {
        try ids.append(try std.fmt.parseInt(i64, line, 10));
    }

    std.mem.sort(twople, ranges.items, {}, compareTwople);

    var i: usize = 0;

    while (i < ranges.items.len - 1) {
        const curr_range = ranges.items[i];
        const next_range = ranges.items[i+1];

        if (next_range.start <= curr_range.end + 1) {
            if (next_range.end > curr_range.end) {
                ranges.items[i] = twople { .start = curr_range.start, .end = next_range.end};
            }
            _ = ranges.orderedRemove(i+1);
        }
        else {
            i += 1;
        }
    }

    var part1: i16 = 0;

    for (ids.items) |id| {
        for (ranges.items) |r| {
            if (r.start <= id and id <= r.end) {
                part1 += 1;
                break;
            }
        }
    }


    var part2: i64 = 0;
    for (ranges.items) |r| {
        part2 += r.end - r.start + 1;
    }

    std.debug.print("{d}\n", .{part1});
    std.debug.print("{d}\n", .{part2});

}
