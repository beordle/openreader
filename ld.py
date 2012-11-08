#coding=utf-8
from __future__ import division
import math
from collections import Counter
#有待于写出更好的相似度算法

def simiar(m,n):
  l=len(m)
  m=Counter(m)
  n=Counter(n)
  m.subtract(n)
  add=0
  for key,times in m.most_common():
      add+=math.fabs(times)
#  print  add/l,
  return add/l

if __name__ == '__main__':
  simiar('dasdasdfasasdfasdfasdfasdfasd','sdafasdfasdfasfasdfasdfasdf')