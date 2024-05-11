from helplib import *
import graph
import sys
from threading import Thread
from time import sleep, time
import os
sys.setrecursionlimit(10000)

start = time()
n = 6
print(f"Counting planes for n={n}...")
planes = formfigures(figure(), n)
print(f"{len(planes)} planes for n={n}")

seq = []
threads: list[Thread] = []
maxthreads = 4
freethreads = 7

def threadfunc(k):
    global seq, n, planes, freethreads
    print(f"Counting for k={k}...")
    suit_count = 0
    notsuit_count = 0
    if k != n:
        figs = formfigures(figure(), k)
    else:
        figs = planes
    print(f"{len(figs)} variants for k={k}, linking with planes...")
    for f in figs:
        for p in planes:
            if f.suit(p):
                suit_count += 1
            else:
                notsuit_count += 1
    seq.append( (k, suit_count/(suit_count+notsuit_count)) )
    print(f"succesfully counted & linked for k={k}")
    freethreads += 1

for k in range(n+1):
    threads.append( Thread(target=threadfunc, args=(k,), daemon=True) )


threadsc = threads.copy()
print("starting threads...")
while len(threads)>0:
    if freethreads>0:
        threads[0].start()
        threads.pop(0)
        freethreads -= 1
    else:
        sleep(10)

for i in threadsc:
    i.join()

seq.sort(key= lambda p: p[0])
end = time()

graph.init()
graph.sequense(seq, True, color=(255,0,0), proportions=0, x_legend=1, y_legend=1, legend=1)
graph.done()
dirname = f"n={n}/"
try:
    os.mkdir(dirname)
except:
    pass
graph.save(f"{dirname}graph for n={n}")
with open(f"{dirname}log for n={n}.txt", 'w') as f:
    f.write(f"n = {n}\nmaxthreads = {maxthreads}\nstart = {start} sec\nend = {end} sec\ntime = {int(round((end-start)/60))} mins")
    f.close()
#graph.show()
#input()

#22 11 -начало для n=10
