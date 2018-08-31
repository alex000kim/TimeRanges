# -------------------------------------------------------------------------------
# Name: TimeRanges.py
# Purpose: Manipulate and modify lists of datetime ranges
# Author:      Alexander Kim
# -------------------------------------------------------------------------------


import calendar
from datetime import datetime as dt
from datetime import timedelta as td


def to_dt(u):
    return dt.utcfromtimestamp(u)


def to_ut(d):
    return calendar.timegm(d.timetuple())


def validate_item(dt_range):
    if type(dt_range) is not list and type(dt_range) is not tuple:
        raise TypeError("{} is not a list or a tuple".format(dt_range))
    if len(dt_range) != 2:
        raise ValueError(
            "{} contains {} element(s). Exactly two elements are expected.".format(dt_range, len(dt_range)))
    if type(dt_range[0]) is not dt or type(dt_range[1]) is not dt:
        raise TypeError("One of the elements in {} is not of datetime type".format(dt_range))
    if dt_range[1] < dt_range[0]:
        raise ValueError("End of the datetime range: {} is before its start: {}".format(dt_range[1], dt_range[0]))


class TimeRanges(list):
    def __init__(self, dt_ranges):
        for dt_range in dt_ranges:
            validate_item(dt_range)
        list.__init__(self, [tuple(dt_range) for dt_range in dt_ranges])

    def append(self, new_member):
        validate_item(new_member)
        super(TimeRanges, self).append(tuple(new_member))

    def remove(self, member):
        super(TimeRanges, self).remove(tuple(member))

    def __str__(self):
        if len(self) == 0:
            return "[]"

        lst = ["[{}, {}]".format(dt_range[0].strftime("%Y-%m-%d %H:%M:%S"), dt_range[1].strftime("%Y-%m-%d %H:%M:%S"))
               for dt_range in self]
        result = "\n".join(lst)
        return "{}\n".format(result)

    def __add__(self, rhs):
        return TimeRanges(list.__add__(self, rhs))

    def __sub__(self, rhs):
        if type(rhs) is not TimeRanges:
            rhs = TimeRanges(rhs)

        class IntervalTree:
            def __init__(self, h, left, right):
                self.h = h
                self.left = left
                self.right = right

        def merged(A, B, op, l=-float("inf"), u=float("inf")):
            if l > u:
                return None
            if not isinstance(A, IntervalTree):
                if isinstance(B, IntervalTree):
                    opT = op
                    A, B, op = B, A, (lambda x, y: opT(y, x))
                else:
                    return op(A, B)
            left = merged(A.left, B, op, l, min(A.h, u))
            right = merged(A.right, B, op, max(A.h, l), u)
            if left is None:
                return right
            elif right is None or left == right:
                return left
            return IntervalTree(A.h, left, right)

        def to_range_list(T, l=-float("inf"), u=float("inf")):
            if isinstance(T, IntervalTree):
                return to_range_list(T.left, l, T.h) + to_range_list(T.right, T.h, u)
            return [(l, u - 1)] if T else []

        def range_list_to_tree(L):
            return reduce(lambda x, y: merged(x, y, lambda a, b: a or b),
                          [IntervalTree(R[0], False, IntervalTree(R[1] + 1, True, False)) for R in L])

        lst1 = []
        for dt_range in self:
            lst1.append([to_ut(dt_range[0]), to_ut(dt_range[1])])
        lst2 = []
        for dt_range in rhs:
            lst2.append([to_ut(dt_range[0]), to_ut(dt_range[1])])

        r1 = range_list_to_tree(lst1)
        r2 = range_list_to_tree(lst2)
        diff = merged(r1, r2, lambda a, b: a and not b)
        result = to_range_list(diff)
        new_ranges = []
        for item in result:
            if to_dt(item[1]) > to_dt(item[0]):
                new_ranges.append([to_dt(item[0]), to_dt(item[1])])

        return TimeRanges(new_ranges)

    def __contains__(self, new_dt_range):
        validate_item(new_dt_range)
        for dt_range in self:
            start = dt_range[0]
            end = dt_range[1]
            if start <= new_dt_range[0] <= end and start <= new_dt_range[1] <= end:
                return True
        return False

    def sort_by(self, start_or_end):
        if start_or_end == "start":
            indx = 0
        elif start_or_end == "end":
            indx = 1
        else:
            raise ValueError('Should be either "start" or "end"')
        self.sort(key=lambda x: x[indx])

    def merge(self):
        # Merge overlapping time ranges
        i = sorted(set([tuple(sorted(x)) for x in self]))
        if len(i) > 0:
            merged_ranges = [i[0]]
            for c, d in i[1:]:
                a, b = merged_ranges[-1]
                if c <= b < d:
                    merged_ranges[-1] = a, d
                elif b < c < d:
                    merged_ranges.append((c, d))
                else:
                    pass
            self.__init__(merged_ranges)

    def merge_min_separation(self, years=None, months=None, days=None, hours=None, minutes=None, seconds=None):
        # Merge time ranges if space between them is less a given number years, months, days, etc
        dct = locals()
        keywords = {}
        for key in dct:
            if key != 'self' and dct[key]:
                keywords[key] = dct[key]

        delta = td(**keywords)
        new_ranges = []
        self.sort(key=lambda dt_range: dt_range[0])
        for i, dt_range in enumerate(self):
            start = dt_range[0]
            end = dt_range[1]
            if i != len(self) - 1:  # not last range
                next_start = self[i + 1][0]
                new_end = end + delta
                if new_end > next_start:
                    end = new_end if new_end < self[i + 1][1] else self[i + 1][1]
            new_ranges.append([start, end])

        self.__init__(new_ranges)
        self.merge()

    def get_starts(self):
        # get start times of all times ranges
        return [dt_range[0] for dt_range in self]

    def get_ends(self):
        # get end times of all times ranges
        return [dt_range[1] for dt_range in self]

    def get_centers(self):
        # get midpoints of all times ranges 
        return [(start + td(seconds=(end - start).total_seconds() / 2.0)) for start, end in self]

    def shift_starts(self, years=None, months=None, days=None, hours=None, minutes=None, seconds=None):
        
        dct = locals()
        keywords = {}
        for key in dct:
            if key != 'self' and dct[key]:
                keywords[key] = dct[key]

        delta = td(**keywords)

        new_ranges = []
        for dt_range in self:
            start_tm = dt_range[0]
            end_tm = dt_range[1]
            shifted_start = start_tm + delta
            new_ranges.append([shifted_start, end_tm])
        self.__init__(new_ranges)

    def shift_ends(self, years=None, months=None, days=None, hours=None, minutes=None, seconds=None):
        dct = locals()
        keywords = {}
        for key in dct:
            if key != 'self' and dct[key]:
                keywords[key] = dct[key]
        delta = td(**keywords)
        new_ranges = []
        for dt_range in self:
            start_tm = dt_range[0]
            end_tm = dt_range[1]
            shifted_end = end_tm + delta
            new_ranges.append([start_tm, shifted_end])
        self.__init__(new_ranges)


    def shift(self, years=None, months=None, days=None, hours=None, minutes=None, seconds=None):
        dct = locals()
        keywords = {}
        for key in dct:
            if key != 'self' and dct[key]:
                keywords[key] = dct[key]

        try:
            self.shift_starts(**keywords)
            self.shift_ends(**keywords)
        except ValueError:
            self.shift_ends(**keywords)
            self.shift_starts(**keywords)

    def extend(self, years=None, months=None, days=None, hours=None, minutes=None, seconds=None):
        dct = locals()
        keywords = {}
        keywords2 = {}
        for key in dct:
            if key != 'self' and dct[key]:
                keywords[key] = dct[key]

        for key in keywords:
            keywords2[key] = -1 * keywords[key]

        try:
            self.shift_starts(**keywords2)
            self.shift_ends(**keywords)
        except ValueError:
            self.shift_ends(**keywords2)
            self.shift_starts(**keywords)

    def contains_shorter_than(self, years=None, months=None, days=None, hours=None, minutes=None, seconds=None):
        dct = locals()
        keywords = {}
        for key in dct:
            if key != 'self' and dct[key]:
                keywords[key] = dct[key]

        delta = td(**keywords)

        for dt_range in self:
            duration = dt_range[1] - dt_range[0]
            if duration < delta:
                return True

        return False

    def remove_if_shorter(self, years=None, months=None, days=None, hours=None, minutes=None, seconds=None):
        dct = locals()
        keywords = {}
        for key in dct:
            if key != 'self' and dct[key]:
                keywords[key] = dct[key]

        delta = td(**keywords)
        new_ranges = []
        for dt_range in self:
            duration = dt_range[1] - dt_range[0]
            if duration >= delta:
                new_ranges.append(dt_range)
        self.__init__(new_ranges)


    def get_boundary(self):
        start_times = self.get_starts()
        end_times = self.get_ends()
        left_boundary = min(start_times)
        right_boundary = max(end_times)
        return [left_boundary, right_boundary]

    def reversed(self):
        return (TimeRanges([self.get_boundary()]) - self)

    def get_durations_sec(self):
        durations = []
        for dt_range in self:
            duration = (dt_range[1] - dt_range[0]).total_seconds()
            durations.append(duration)
        return durations

    def divide(self, years=None, months=None, days=None, hours=None, minutes=None, seconds=None):
        dct = locals()
        keywords = {}
        for key in dct:
            if key != 'self' and dct[key]:
                keywords[key] = dct[key]

        delta = td(**keywords)

        new_ranges = []
        for dt_range in self:
            start = dt_range[0]
            end = dt_range[1]
            start2 = start
            end2 = start2 + delta
            if end2 < end:
                while end2 < end:
                    old_start2 = start2
                    old_end2 = end2
                    new_ranges.append([old_start2, old_end2])
                    start2 = old_end2 + td(seconds=1)
                    end2 = start2 + delta
                new_ranges.append([old_end2 + td(seconds=1), end])
            else:
                new_ranges.append([start, end])

        self.__init__(new_ranges)

