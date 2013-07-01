#!/usr/bin/python

import MySQLdb as mdb
import sys
import time

count_by = 10

try:
    con = mdb.connect('localhost', 'beal_admin', 'husdfuwe78234', 'BEALDATA');

    cur = con.cursor()
    
    x = 0
    y = 0
    
    while(True):
      for m in xrange(x * count_by + 1, (x * count_by + 1) + count_by+1):
        for n in xrange(3, m+3):
          cur.execute("INSERT INTO uc_new_attempts (exp_m, exp_n) VALUES (%s, %s)", (m+2, n));
          con.commit()
          print m+2, n
      
          con.commit()
          cur.execute("SELECT COUNT(id) FROM uc_new_attempts")
          count = cur.fetchone()  
          while(count[0] > count_by**2):
            time.sleep(1)
            con.commit()
            cur.execute("SELECT COUNT(id) FROM uc_new_attempts")
            count = cur.fetchone()
      x = x + 1
      y = y + 1
    
     
    
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()
