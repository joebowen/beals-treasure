#!/usr/bin/env python

#MapReduce based solution to integrate with www.bealstreasure.com
#to work on finding counterexamples to Beal's conjecture.
#That is, find positive integers x,m,y,n,z,r such that:
#x^m + y^n = z^r and m,n,r > 2 and x,y,z co-prime (pairwise no common factor).

#ALGORITHM: Initialize the variables table, pow, bases, powers such that:
#        table.get(sum) = r if there is a z such that z**r = sum.  
#        bases = [1, 2, ... max_base]
#        powers = [3, 4, ... max_power]
#Then enumerate x,y,m,n,	and do table.get(pow[x][m]+pow[y][n]).  
#If we get something back, report it as a result.  We consider all 
#values of x,y,z in bases, and all values of m,n,r in powers.

import urllib
import sys

#NOTE: Enter your email address here in case you find the solution
#This will make tracking down the user who's computer finds the solution
#easier to get in touch with.
username = "charity"     

#This value reflects the number of base values, currently 
#bealstreasure.com can only support exactly 10000
max_base = 10000          

def main(separator='\t'):
  f = urllib.urlopen("http://bealstreasure.com/members/getwork.php?username="+ username + "&max_base=" + str(max_base)).read()
    
  param = f.split(",")

  print '%d%s%d%s%s' % (int(param[0]), separator, int(param[1]), separator, param[2])

if __name__ == "__main__":
  main()
