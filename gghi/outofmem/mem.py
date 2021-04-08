import tracemalloc # from 3.4
from pympler import tracker,summary,muppy
tracemalloc.start(25)
snapshot = tracemalloc.take_snapshot()
mt = tracker.SummaryTracker()

# tracemalloc
'''
if __name__ == '__main__':
	tracemalloc.start() # 开始跟踪内存分配

	d = [dict(zip('xy',(5, 6))) for i in range(1000000)]
	t = [tuple(zip('xy',(5, 6))) for i in range(1000000)]

	snapshot = tracemalloc.take_snapshot() # 快照，当前内存分配
	top_stats = snapshot.statistics('lineno') # 快照对象的统计

	for stat in top_stats:
		print(stat)

'''
class A(object):
    def __init__(self):
        self.data = [x for x in range(100000)]
        self.child = None
 
    def __del__(self):
        pass
 
def cycle_ref():
    a1 = A()
    a2 = A()
 
    a1.child = a2
    a2.child = a1


if __name__ == '__main__':
    import time
    while True:
        time.sleep(0.5)
        cycle_ref()
        snapshot1 = tracemalloc.take_snapshot()
        top_stats = snapshot1.compare_to(snapshot, 'lineno')
        print("[ Top 10 differences ]")
        for stat in top_stats[:10]:
            if stat.size_diff < 0:
                continue
            print(stat)
        snapshot = tracemalloc.take_snapshot()
        #mt.print_diff()
