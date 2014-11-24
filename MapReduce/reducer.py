#!/usr/bin/env python

from itertools import groupby
from operator import itemgetter
import sys
import time
import math
from gmpy import gcd
import urllib

#Does nothing right now, I want it to reflect the memory/thread used for each set_id.
memory = 0        

#This value reflects the number of base values, currently 
#bealstreasure.com can only support exactly 10000
max_base = 10000 

def read_mapper_output(file, separator='\t'):
  for line in file:
    yield line.rstrip().split(separator, 1)

def main(max_base, separator='\t'):
  max_exp = max([m, n])
  table = initial_data_table(max_base, m, n)

  (m, n, set_id) = read_mapper_output(sys.stdin, separator=separator)
 
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
  print '(%d, %d, %s)' % (m, n, set_id)
         
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

if __name__ == "__main__":
  main(max_base)
