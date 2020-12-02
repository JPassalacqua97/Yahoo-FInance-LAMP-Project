# CS288 Homework 8
# Read the skeleton code carefully and try to follow the structure
# You may modify the code but try to stay within the framework.

import sys
import os
import commands
import re
import sys

import MySQLdb

from xml.dom.minidom import parse, parseString

# for converting dict to xml 
from cStringIO import StringIO
from xml.parsers import expat

def get_elms_for_atr_val(tag):
   lst=[]
   elms = dom.getElementsByTagName(tag)
   #f_elms = filter(lambda x: len(x.childNodes), elms)    #print(elms)                          #gets element adresses
   lst = elms
   #lst = lst[1:]
   return lst

# get all text recursively to the bottom
def get_text(e):
   lst=[]
   if e.nodeType in (3,4):
       lst.append(e.nodeValue.encode('utf8'))
   else:
        for x in e.childNodes:
            lst += get_text(x)
                
   return lst

# replace whitespace chars
def replace_white_space(str):
   p = re.compile(r'\s+')
   new = p.sub(' ',str)   # a lot of \n\t\t\t\t\t\t
   return new.strip()

# replace but these chars including ':'
def replace_non_alpha_numeric(s):
   p = re.compile(r'[^a-zA-Z0-9:-]+')
   #   p = re.compile(r'\W+') # replace whitespace chars
   new = p.sub(' ',s)
   return new.strip()

# convert to xhtml
# use: java -jar tagsoup-1.2.jar --files html_file
def html_to_xml(fn):
    html_to_xml = "java -jar tagsoup-1.2.1.jar --files "+ fn        #I used 1.2.1.jar
    os.system(html_to_xml)                                          #runs it in your system
    xhtml_file = fn.replace(".html",".xhtml")                       #replaces .html w .xhtml
    return xhtml_file

def extract_values(dm):
   lst = []
   
   l = get_elms_for_atr_val('tr')
   lst = list(map(lambda x: get_text(x), l))

   
   lstHeaders = lst[0]
   l_ths = get_elms_for_atr_val('th')
   hdr_txts = list(map(lambda x: get_text(x), l_ths))

   hdr_txts = flatten(hdr_txts)

   #print(hdr_txts)


   lst = lst[1:]
   for i in lst:
       i.append('None')


   d = list(map(lambda x: to_dict(x),lst))
   print(d)
   

   
   return d

def flatten(l):
   return list(map(lambda x: x[0] if x else 'None', l))

def to_dict(vals):
    #return dict(map(lambda k,v: (k,v), keys, vals))
    keys = ['symbol','name', 'price', 'chnge', 'pchnge','volume', 'avg_volume','market_cap','pe_ratio','52_range']
    return dict(map(lambda i: (keys[i],vals[i]),range(len(keys))))

# mysql> describe most_active;
def insert_to_db(l,tbl):
   mydb = MySQLdb.connect(host = "localhost", user = 'cs288', password = 'cs288pwd', db ="stocks")
   print("connected")
   mycursor = mydb.cursor() 
   print(tbl)
   table = "CREATE TABLE IF NOT EXISTS " + "`"  + tbl + "`" +   " (symbol VARCHAR(10), name VARCHAR(80), price VARCHAR(20), chnge VARCHAR(20), pchnge VARCHAR(20), volume VARCHAR(20), avg_volume VARCHAR(20), market_cap VARCHAR(20), pe_ratio VARCHAR(20), 52_range VARCHAR(20))"
   mycursor.execute(table)
   
   if(mycursor.execute("SELECT 1 FROM " + "`"  + tbl + "`") == 0):
      for i in l:
         insert = ("insert into " + "`"  + tbl + "`" + " (symbol, name, price, chnge, pchnge, volume, avg_volume, market_cap, pe_ratio, 52_range) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
         data = (i["symbol"], i["name"], i["price"], i["chnge"], i["pchnge"], i["volume"], i["avg_volume"], i["market_cap"], i["pe_ratio"], i["52_range"])
         mycursor.execute(insert,data)
   
   mydb.commit()

   return mycursor

def select_from_db(cursor,fn):
   
   table = ("Select * from " + "`" + fn +"`")
   cursor.execute(table)
   info = cursor.fetchall()

   print("\nSTOCKS: ")

   for i in info:
      print(i)

   return info


def main():
   html_fn = sys.argv[1]
   fn = html_fn.replace('.html','')
   xhtml_fn = html_to_xml(html_fn)

   global dom
   dom = parse(xhtml_fn)

   lst = extract_values(dom)

   #print(lst)


   # make sure your mysql server is up and running
   cursor = insert_to_db(lst,fn) # fn = table name for mysql

   l = select_from_db(cursor,fn) # display the table on the screen

   # make sure the Apache web server is up and running
   # write a PHP script to display the table(s) on your browser

   #return xml
# end of main()

if __name__ == "__main__":
    main()

# end of hw7.py
