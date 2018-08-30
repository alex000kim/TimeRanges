# TimeRanges
Manipulate and modify lists of datetime ranges

Example:
```python
from TimeRanges import TimeRanges
tr1_str = [('02 Jan 2018', '10 Feb 2018'), ('20 Mar 2018', '20 Apr 2018')]
tr2_str = [('10 Mar 2018', '25 May 2018'), ('23 May 2018', '05 Jun 2018')]
tr1 = [(dt.strptime(t1, '%d %b %Y'), dt.strptime(t2, '%d %b %Y')) for (t1,t2) in tr1_str]
tr1 = TimeRanges(tr1)
tr1
> [(datetime.datetime(2018, 1, 2, 0, 0), datetime.datetime(2018, 2, 10, 0, 0)),
 (datetime.datetime(2018, 3, 20, 0, 0), datetime.datetime(2018, 4, 20, 0, 0))]

tr2 = [(dt.strptime(t1, '%d %b %Y'), dt.strptime(t2, '%d %b %Y')) for (t1,t2) in tr2_str]
tr2 = TimeRanges(tr2)
tr2
> [(datetime.datetime(2018, 3, 10, 0, 0), datetime.datetime(2018, 5, 25, 0, 0)),
 (datetime.datetime(2018, 5, 23, 0, 0), datetime.datetime(2018, 6, 5, 0, 0))] 
 
tr3 = tr1 + tr2
tr3
> [(datetime.datetime(2018, 1, 2, 0, 0), datetime.datetime(2018, 2, 10, 0, 0)),
 (datetime.datetime(2018, 3, 20, 0, 0), datetime.datetime(2018, 4, 20, 0, 0)),
 (datetime.datetime(2018, 3, 10, 0, 0), datetime.datetime(2018, 5, 25, 0, 0)),
 (datetime.datetime(2018, 5, 23, 0, 0), datetime.datetime(2018, 6, 5, 0, 0))]
 
# Merge overlapping time ranges
tr3.merge()
tr3
> [(datetime.datetime(2018, 1, 2, 0, 0), datetime.datetime(2018, 2, 10, 0, 0)),
 (datetime.datetime(2018, 3, 10, 0, 0), datetime.datetime(2018, 6, 5, 0, 0))]
# [('02 Jan 2018', '10 Feb 2018'), ('10 Mar 2018', '05 Jun 2018')]
```
