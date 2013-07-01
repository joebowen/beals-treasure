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

from multiprocessing import Process, Queue
import time
import math

processors = 6    #Number of processors on machine
chunk_num = 100    #Number of chunks to split problem set into    

def beal(max_base, max_power):
  table, pow = initial_data(max_base, max_power)

  chunk_size = int(math.ceil(max_base / chunk_num))  #Determining how many bases are included in each problem set

  print 'Chunk Size:', chunk_size

  start_queue = Queue()
  
  pool = []
  for process in xrange(processors):  #Create the same number of multiprocesses as processors available
    p = Process(target=beal_parallel, args=(start_queue, max_base, max_power, chunk_size, table, pow))
    p.start()
    pool.append(p)
  
  for i in xrange(chunk_num): #Prepare the queue with section numbers
    start_queue.put(i)

  for i in xrange(processors):  #Add the process termination signals to the queue
    start_queue.put(None)

  for p in pool:  #Wait for all processes to finish
    p.join()

def beal_parallel(start_queue, max_base, max_power, chunk_size, table, pow):
  mod_val = max_base / 10

  base = range(1, max_base+1)
  power = range(3, max_power+1)

  start = start_queue.get()
  while (start <> None):
    for x in base[start * chunk_size:(start + 1) * chunk_size]:
      powx = pow[x]
      if x % mod_val == 0: print 'x(', x / chunk_size ,'%)'
      for y in base:
        if y > x or gcd(x,y) > 1: continue
        powy = pow[y]
        for m in power:
          xm = powx[m]
          for n in power:
            sum = xm + powy[n]
            r = table.get(sum)
            if r: report(x, m, y, n, nth_root(sum, r), r)
    start = start_queue.get()
              
def initial_data(max_base, max_power):
  table = {}
  pow = [None] * (max_base+1)
  for z in xrange(1, max_base+1):
    pow[z] = [None] * (max_power+1)
    for r in xrange(3, max_power+1):
      zr = long(z) ** r
      pow[z][r] = zr
      table[zr] = r
  print 'initialized %d table elements' % len(table)
  return table, pow  

def report(x, m, y, n, z, r):
  x, y, z = map(long, (x, y, z))
  if (min(x, y, z) > 0 and min(m, n, r) > 2 ):
    if (x ** m + y ** n == z ** r):  
      if gcd(x,y) == gcd(x,z) == gcd(y, z) == 1: 
        print 'Yay!!!: %d ^ %d + %d ^ %d = %d ^ %d = %s' % ( x,   m,   y,   n,   z,   r,  z**r)

def gcd(u, v):
  # simple cases (termination)
  if (u == v):
    return u
  if (u == 0):
    return v
  if (v == 0):
    return u
 
  # look for factors of 2
  if (~u & 1): # u is even
    if (v & 1): # v is odd
      return gcd(u >> 1, v)
    else: # both u and v are even
      return gcd(u >> 1, v >> 1) << 1
  if (~v & 1): # u is odd, v is even
    return gcd(u, v >> 1)
 
  # reduce larger argument
  if (u > v):
    return gcd((u - v) >> 1, v)
  return gcd((v - u) >> 1, u)

def nth_root(base, n): 
  return long(round(base ** (1.0/n)))

def timer(b, p):
  start_timer = time.time()  #time.clock() is unusable due to multiprocessing
  beal(b, p)
  secs = time.time() - start_timer  #time.clock() is unusable (see above)
  print 'timer(', b, ',', p, ')'
  return {'secs': secs, 'mins': secs/60, 'hrs': secs/60/60}

#Memory Test
#table, pow = initial_data(100000, 100)
#table, pow = initial_data(250000, 1000)  

#Test Run    
#print timer( 100, 100)
#print timer( 100, 1000)  
print timer( 1000, 10)

#New Runs
print timer( 100000, 30)
#print timer( 10000, 100)  
#print timer(100000,  10)  
#print timer(250000,   7)  

#Brand New Data
print timer( 1000, 1000)
print timer( 10000, 1000)
print timer( 100000, 30)
print timer( 100000, 100)
#print timer( 100000, 1000)
#print timer( 250000, 10)
#print timer( 250000, 30)
#print timer( 250000, 100)
#print timer( 250000, 1000)
