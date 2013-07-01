#Print counterexamples to Beal's conjecture.
#That is, find positive integers x,m,y,n,z,r such that:
#x^m + y^n = z^r and m,n,r > 2 and x,y,z co-prime (pairwise no common factor).

#ALGORITHM: Initialize the variables table, pow, bases, powers such that:
#        pow[z][r] = z**r
#        table.get(sum) = r if there is a z such that z**r = sum.  
#        bases = [1, 2, ... max_base]
#        powers = [3, 4, ... max_power]
#Then enumerate x,y,m,n,	and do table.get(pow[x][m]+pow[y][n]).  If we get 
#something back, report it as a result.  We consider all values of x,y,z
#in bases, and all values of m,n,r in powers.

from multiprocessing import Process, Queue, cpu_count
import time
import math
from gmpy import gcd

processors = cpu_count()  #Number of processors on machine 

def beal_parallel(max_base, max_power, queue):
  table = {}
  for i in xrange(1, max_base):
    for r in xrange(3, max_power):
      zr = long(i) ** r
      table[zr] = r

  (m, n) = queue.get()
  while ((m, n) <> (None, None)): 
    print '(%d, %d)' % (m, n)
    powx, powy = initial_data(max_base, m, n)
    
    for x in xrange(1, max_base):
      powx_tmp = powx[x]
      for y in xrange(1, x):
        if gcd(x,y) > 1: continue
        sum = powx_tmp + powy[y]
        zr = table.get(sum)
        if zr:
          print "Building Report... Possible Find" 
          report(x, m, y, n, nth_root(sum, zr), zr)        
    (m, n) = queue.get()
     
def initial_data(max_base, m, n):
  powx = [None] * (max_base+1)
  powy = [None] * (max_base+1)
  
  for i in xrange(1, max_base):
    xm = long(i) ** m
    powx[i] = xm
    
    yn = long(i) ** n
    powy[i] = yn
  return powx, powy

def report(x, m, y, n, z, r):
  x, y, z = map(long, (x, y, z))
  if (min(x, y, z) > 0 and min(m, n, r) > 2 ):
    if (x ** m + y ** n == z ** r):  
      if gcd(x,y) == gcd(x,z) == gcd(y, z) == 1: 
        print 'Yay!!!: %d ^ %d + %d ^ %d = %d ^ %d = %s' % ( x,   m,   y,   n,   z,   r,  z**r)

def nth_root(base, n): 
  return long(round(base ** (1.0/n)))

def beal(max_base, max_power):
  start_timer = time.time()  #time.clock() is unusable due to multiprocessing
  
  queue = Queue()
  pool = []
  for process in xrange(processors):  #Create the same number of processes as processors available
    pr = Process(target=beal_parallel, args=(max_base, max_power, queue))
    pr.start()
    pool.append(pr)
    
  for m in xrange(3, max_power):
    for n in xrange(3, max_power):
      queue.put((m, n))
  
  for v in xrange(processors):
    queue.put((None, None))
       
  for p in pool:  #Wait for all processes to finish
    p.join()
        
  secs = time.time() - start_timer  #time.clock() is unusable (see above)
  print 'beal(', max_base, ',', max_power, ')'
  return {'secs': secs, 'mins': secs/60, 'hrs': secs/60/60, 'days': secs/60/60/24}



#Memory Test
#table, pow = initial_data(5000000, 3, 7, 10)
#table, pow = initial_data(250000, 1000)  

#print "Memory Test Complete"  

#Test Run    
#print beal( 100, 1000)  
#print beal( 1000, 10)
print beal( 100, 100)
#print beal( 1000, 100)
#print beal( 1000, 1000)

#New Runs
#print beal( 10000, 30)
#print beal( 10000, 100)  
#print beal(100000,  10)  
#print beal(250000,   7)  

print beal(1000000, 9)

#Brand New Data
#print beal( 1000, 1000)
#print beal( 10000, 1000)
#print beal( 100000, 30)
#print beal( 100000, 100)
#print beal( 100000, 1000)
#print beal( 250000, 10)
#print beal( 250000, 30)
#print beal( 250000, 100)
#print beal( 250000, 1000)
