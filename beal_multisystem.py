#!/usr/bin/python
#Print counterexamples to Beal's conjecture.
#That is, find positive integers x,m,y,n,z,r such that:
#x^m + y^n = z^r and m,n,r > 2 and x,y,z co-prime (pairwise no common factor).

#ALGORITHM: Initialize the variables table, pow, bases, powers such that:
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
import urllib2
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='urllib2')

processors = cpu_count()

username = ""      #NOTE: Create a free username on bealstreasure.com
password = ""      

memory = 0        #Does nothing right now, I want it to reflect the memory/thread used for each set_id.
max_base = 10000  #DO NOT CHANGE!

def beal_parallel(max_base, queue):
  (m, n, set_id) = queue.get()
  while(True):
    print '(%d, %d, %s)' % (m, n, set_id)

    powx, powy, table = initial_data(max_base, m, n)

    for x in xrange(1, max_base):
      powx_tmp = powx[x]
      for y in xrange(1, x):
        if gcd(x,y) > 1: continue
        sum = powx_tmp + powy[y]
        zr = table.get(sum)
        if zr:
          passman = urllib2.HTTPPasswordMgrWithDefaultRealm( )
          passman.add_password(None, "http://bealstreasure.com/members/", username, password)
          authhandler = urllib2.HTTPBasicAuthHandler(passman)
          opener = urllib2.build_opener(authhandler)
          print 'Yay!!!: %d ^ %d + %d ^ %d = %s' % ( x,   m,   y,   n,   zr)
          f = opener.open("http://bealstreasure.com/members/savework.php?&result=true&x=" + str(x) + "&m=" + str(m) + "&y=" + str(y) + "&n=" + str(n) + "&z=" + str(nth_root(sum, zr))).read()
          
          report(x, m, y, n, nth_root(sum, zr), zr)
    
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm( )
    passman.add_password(None, "http://bealstreasure.com/members/", username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    f = opener.open("http://bealstreasure.com/members/savework.php?result=false&memory=" + str(memory) + "&id=" + str(set_id)).read()
         
    (m, n, set_id) = queue.get()
       
def initial_data(max_base, m, n):
  powx = [None] * (max_base+1)
  powy = [None] * (max_base+1)
  
  table = {}
  for i in xrange(1, max_base):
    for r in xrange(3, max([m, n])):
      zr = long(i) ** r
      table[zr] = r
  
  for i in xrange(1, max_base):
    xm = long(i) ** m
    powx[i] = xm
    
    yn = long(i) ** n
    powy[i] = yn
  return powx, powy, table

def report(x, m, y, n, z, r):
  x, y, z = map(long, (x, y, z))
  if (min(x, y, z) > 0 and min(m, n, r) > 2 ):
    if (x ** m + y ** n == z ** r):  
      if gcd(x,y) == gcd(x,z) == gcd(y, z) == 1: 
        print 'Yay!!!: %d ^ %d + %d ^ %d = %d ^ %d = %s' % ( x,   m,   y,   n,   z,   r,  z**r)

def nth_root(base, n): 
  return long(round(base ** (1.0/n)))

def beal():
  queue = Queue()
  pool = []
  for process in xrange(processors):  #Create the same number of processes as processors available
    pr = Process(target=beal_parallel, args=(max_base, queue))
    pr.start()
    pool.append(pr)
    
  while (True):
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm( )
    passman.add_password(None, "http://bealstreasure.com/members/", username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    f = opener.open("http://bealstreasure.com/members/getwork.php?username="+ username + "&max_base=" + str(max_base)).read()
    
    param = f.split(",")
    queue.put((int(param[0]), int(param[1]), param[2]))
      
    while (queue.qsize() > 1):
      time.sleep(5)

beal()

