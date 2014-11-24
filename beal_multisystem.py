#!/usr/bin/python

#Print counterexamples to Beal's conjecture.
#That is, find positive integers x,m,y,n,z,r such that:
#x^m + y^n = z^r and m,n,r > 2 and x,y,z co-prime (pairwise no common factor).

#ALGORITHM: Initialize the variables table, pow, bases, powers such that:
#        table.get(sum) = r if there is a z such that z**r = sum.  
#        bases = [1, 2, ... max_base]
#        powers = [3, 4, ... max_power]
#Then enumerate x,y,m,n,	and do table.get(pow[x][m]+pow[y][n]).  
#If we get something back, report it as a result.  We consider all 
#values of x,y,z in bases, and all values of m,n,r in powers.

from multiprocessing import Process, Queue, cpu_count
import time
import math
from gmpy import gcd
import urllib

processors = cpu_count()

#Does nothing right now, I want it to reflect the memory/thread used for each set_id.
memory = 0        

#NOTE: Enter your email address here in case you find the solution
#This will make tracking down the user who's computer finds the solution
#easier to get in touch with.
username = "charity"     

#This value reflects the number of base values, currently 
#bealstreasure.com can only support exactly 10000
max_base = 10000 

def beal_parallel(max_base, queue):
  m=200;
  n=200;
  max_exp = max([m, n])
  table = initial_data_table(max_base, m, n)

  (m, n, set_id) = queue.get()
  while(True):
    print '(%d, %d, %s)' % (m, n, set_id)
     
    if (max_exp < max([m, n]) + 10):
      table = initial_data_table(max_base, m, n)
      max_exp = max([m, n])
         
    powx, powy = initial_data_pow(max_base, m, n)

    for x in xrange(1, max_base):
      powx_tmp = powx[x]
      for y in xrange(1, x):
        if gcd(x,y) > 1: continue
        sum = powx_tmp + powy[y]
        zr = table.get(sum)
        if zr:
          report(x, m, y, n)

    f = urllib.urlopen("http://bealstreasure.com/members/savework.php?result=false&memory=" + str(memory) + "&id=" + str(set_id)).read()
         
    (m, n, set_id) = queue.get()
       
def initial_data_table(max_base, m, n):  
  table = {}
  for i in xrange(1, max_base):
    for r in xrange(3, max([m, n]) + 1):
      zr = long(i) ** r
      table[zr] = r
  return table
  
def initial_data_pow(max_base, m, n):
  powx = [None] * (max_base+1)
  powy = [None] * (max_base+1)

  for i in xrange(1, max_base):
    xm = long(i) ** m
    powx[i] = xm
    
    yn = long(i) ** n
    powy[i] = yn
  return powx, powy

def report(x, m, y, n):
  x, y = map(long, (x, y))
  if (min(x, y) > 0 and min(m, n) > 2 ):
    if gcd(x,y) == 1: 
      print 'We might have a solution!!  Contact bealstreasure.com for details: %d ^ %d + %d ^ %d' % ( x,   m,   y,   n)
      f = urllib.urlopen("http://bealstreasure.com/members/savework.php?&result=true&x=" + str(x) + "&m=" + str(m) + "&y=" + str(y) + "&n=" + str(n)).read()
          
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
    f = urllib.urlopen("http://bealstreasure.com/members/getwork.php?username="+ username + "&max_base=" + str(max_base)).read()
    
    param = f.split(",")
    queue.put((int(param[0]), int(param[1]), param[2]))
      
    while (queue.qsize() > 1):
      time.sleep(5)

beal()

