import unittest
from TimeRanges import TimeRanges
from datetime import datetime as dt


class TestTimeRanges(unittest.TestCase):
    def test_raises_type_error_element(self):
        list1 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 dt(2015, 1, 1, 12, 30, 00)]
        self.assertRaises(TypeError, TimeRanges, list1)

    def test_raises_type_error_subelement(self):
        list1 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [1, 2]]
        self.assertRaises(TypeError, TimeRanges, list1)

    def test_raises_value_error_end_before_start(self):
        list1 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 14, 20, 30), dt(2015, 1, 1, 13, 01, 10)]]
        self.assertRaises(ValueError, TimeRanges, list1)

    def test_append(self):
        list1 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)]]
        addition = [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]
        result = TimeRanges(list1)
        result.append(addition)
        list2 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        expected = TimeRanges(list2)
        self.assertEqual(result, expected)

    def test_remove(self):
        list1 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        result = TimeRanges(list1)
        result.remove([dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)])
        list2 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        expected = TimeRanges(list2)
        self.assertEqual(result, expected)

    def test_str_repr(self):
        list1 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)]]
        result = str(TimeRanges(list1))
        expected = "[2015-01-01 13:01:10, 2015-01-01 14:20:30]\n" \
                   "[2015-01-01 12:30:00, 2015-01-01 13:00:30]\n"
        self.assertEqual(result, expected)

    def test_add(self):
        list1 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)]]
        list2 = [[dt(2015, 1, 1, 14, 01, 10), dt(2015, 1, 1, 15, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        list3 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 14, 01, 10), dt(2015, 1, 1, 15, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        tr1 = TimeRanges(list1)
        tr2 = TimeRanges(list2)
        result = tr1 + tr2
        expected = TimeRanges(list3)
        self.assertEqual(result, expected)

    def test_sub(self):
        list1 = [[dt(2015, 1, 1, 13, 00, 00), dt(2015, 1, 1, 14, 00, 00)],
                 [dt(2015, 1, 1, 14, 30, 00), dt(2015, 1, 1, 15, 00, 00)]]

        list2 = [[dt(2015, 1, 1, 13, 20, 00), dt(2015, 1, 1, 13, 40, 00)]]

        list3 = [[dt(2015, 1, 1, 13, 00, 00), dt(2015, 1, 1, 13, 19, 59)],
                 [dt(2015, 1, 1, 13, 40, 01), dt(2015, 1, 1, 14, 00, 00)],
                 [dt(2015, 1, 1, 14, 30, 00), dt(2015, 1, 1, 15, 00, 00)]]
        tr1 = TimeRanges(list1)
        tr2 = TimeRanges(list2)
        result = tr1 - tr2
        expected = TimeRanges(list3)
        self.assertEqual(result, expected)

    def test_contains(self):
        list1 = [[dt(2015, 1, 1, 13, 00, 00), dt(2015, 1, 1, 14, 00, 00)],
                 [dt(2015, 1, 1, 14, 30, 00), dt(2015, 1, 1, 15, 00, 00)]]
        tr1 = TimeRanges(list1)
        list2 = [dt(2015, 1, 1, 13, 20, 00), dt(2015, 1, 1, 13, 40, 00)]
        result = list2 in tr1
        expected = True
        self.assertEqual(result, expected)

    def test_sort_by_start(self):
        list1 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 14, 01, 10), dt(2015, 1, 1, 15, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        result = TimeRanges(list1)
        result.sort_by("start")
        list2 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 14, 01, 10), dt(2015, 1, 1, 15, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        expected = TimeRanges(list2)
        self.assertEqual(result, expected)

    def test_sort_by_end(self):
        list1 = [[dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)],
                 [dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 14, 01, 10), dt(2015, 1, 1, 15, 20, 30)]]
        result = TimeRanges(list1)
        result.sort_by("end")
        list2 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 14, 01, 10), dt(2015, 1, 1, 15, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        expected = TimeRanges(list2)
        self.assertEqual(result, expected)

    def test_merge(self):
        list1 = [[dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 13, 00, 40), dt(2015, 1, 1, 15, 00, 30)],
                 [dt(2015, 1, 1, 15, 00, 20), dt(2015, 1, 1, 16, 20, 20)]]
        result = TimeRanges(list1)
        result.merge()
        list2 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 13, 00, 40), dt(2015, 1, 1, 16, 20, 20)]]
        expected = TimeRanges(list2)
        self.assertEqual(result, expected)

    def test_merge_min_separation(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 14, 01, 10), dt(2015, 1, 1, 15, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        result = TimeRanges(list1)
        result.merge_min_separation(minutes=1)
        list2 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 15, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        expected = TimeRanges(list2)
        self.assertEqual(result, expected)

    def test_get_starts(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 14, 01, 10), dt(2015, 1, 1, 15, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        result = TimeRanges(list1).get_starts()
        expected = [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 01, 10),
                    dt(2015, 1, 1, 16, 30, 00)]
        self.assertEqual(result, expected)

    def test_get_ends(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 14, 01, 10), dt(2015, 1, 1, 15, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        result = TimeRanges(list1).get_ends()
        expected = [dt(2015, 1, 1, 13, 00, 30), dt(2015, 1, 1, 14, 20, 30), dt(2015, 1, 1, 15, 20, 30),
                    dt(2015, 1, 1, 17, 00, 30)]
        self.assertEqual(result, expected)

    def test_shift(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 13, 01, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 00), dt(2015, 1, 1, 17, 00, 30)]]
        result = TimeRanges(list1)
        result.shift(hours=1, minutes=2, seconds=10)
        list2 = [[dt(2015, 1, 1, 13, 32, 10), dt(2015, 1, 1, 14, 02, 40)],
                 [dt(2015, 1, 1, 14, 03, 20), dt(2015, 1, 1, 15, 22, 40)],
                 [dt(2015, 1, 1, 17, 32, 10), dt(2015, 1, 1, 18, 02, 40)]]
        expected = TimeRanges(list2)
        self.assertEqual(result, expected)

    def test_extend(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 13, 00, 30)],
                 [dt(2015, 1, 1, 13, 10, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 20), dt(2015, 1, 1, 17, 00, 25)]]
        result = TimeRanges(list1)
        result.extend(hours=1, minutes=2, seconds=5)
        list2 = [[dt(2015, 1, 1, 11, 27, 55), dt(2015, 1, 1, 14, 02, 35)],
                 [dt(2015, 1, 1, 12, 8, 05), dt(2015, 1, 1, 15, 22, 35)],
                 [dt(2015, 1, 1, 15, 28, 15), dt(2015, 1, 1, 18, 02, 30)]]
        expected = TimeRanges(list2)
        self.assertEqual(result, expected)

    def test_true_contains_shorter_than(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 12, 35, 00)],
                 [dt(2015, 1, 1, 13, 10, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 20), dt(2015, 1, 1, 17, 00, 25)]]
        self.assertTrue(TimeRanges(list1).contains_shorter_than(minutes=6))

    def test_false_contains_shorter_than2(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 12, 35, 00)],
                 [dt(2015, 1, 1, 13, 10, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 20), dt(2015, 1, 1, 17, 00, 25)]]
        self.assertFalse(TimeRanges(list1).contains_shorter_than(minutes=1))

    def test_remove_if_shorter(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 12, 35, 00)],
                 [dt(2015, 1, 1, 13, 10, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 20), dt(2015, 1, 1, 17, 00, 25)]]
        result = TimeRanges(list1)
        result.remove_if_shorter(minutes=6)
        list2 = [[dt(2015, 1, 1, 13, 10, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 20), dt(2015, 1, 1, 17, 00, 25)]]
        expected = TimeRanges(list2)

        self.assertEqual(result, expected)

    def get_boundary(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 12, 35, 00)],
                 [dt(2015, 1, 1, 13, 10, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 20), dt(2015, 1, 1, 17, 00, 25)]]
        result = TimeRanges(list1).get_boundary()
        expected = [dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 17, 00, 25)]
        self.assertEqual(result, expected)

    def test_reverse(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 12, 35, 00)],
                 [dt(2015, 1, 1, 13, 10, 10), dt(2015, 1, 1, 14, 20, 30)],
                 [dt(2015, 1, 1, 16, 30, 20), dt(2015, 1, 1, 17, 00, 25)]]
        result = TimeRanges(list1).reversed()
        list2 = [[dt(2015, 1, 1, 12, 35, 01), dt(2015, 1, 1, 13, 10, 9)],
                 [dt(2015, 1, 1, 14, 20, 31), dt(2015, 1, 1, 16, 30, 19)]]
        expected = TimeRanges(list2)
        self.assertEqual(result, expected)

    def test_get_durations_sec(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 12, 35, 00)],
                 [dt(2015, 1, 1, 13, 10, 00), dt(2015, 1, 1, 14, 20, 30)]]
        result = TimeRanges(list1).get_durations_sec()
        expected = [300, 4230]
        self.assertEqual(result, expected)

    def test_divide(self):
        list1 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 12, 59, 00)],
                 [dt(2015, 1, 1, 13, 10, 00), dt(2015, 1, 1, 14, 20, 30)]]
        result = TimeRanges(list1)
        result.divide(minutes=25)
        list2 = [[dt(2015, 1, 1, 12, 30, 00), dt(2015, 1, 1, 12, 55, 00)],
                 [dt(2015, 1, 1, 12, 55, 1), dt(2015, 1, 1, 12, 59, 00)],
                 [dt(2015, 1, 1, 13, 10, 00), dt(2015, 1, 1, 13, 35, 00)],
                 [dt(2015, 1, 1, 13, 35, 1), dt(2015, 1, 1, 14, 00, 1)],
                 [dt(2015, 1, 1, 14, 00, 2), dt(2015, 1, 1, 14, 20, 30)]]
        expected = TimeRanges(list2)
        self.assertEqual(result, expected)

    if __name__ == '__main__':
        unittest.main()
