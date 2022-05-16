##  Spiral Numbers
##  by Mike Phillips, 9/5/2018

import numpy as np

def skip(num):
    print(""*num)

n = int(input("\n"*2 + "Please type an integer greater than or equal to 3:\t"))
skip(1)
if n < 3 or n > 100:
    print("ERROR: invalid integer chosen, n=%i." % n)
    skip(1)
else:
    print("You have chosen n=%i" % n)
    skip(1)

def rotate(m):
    res = m.copy()
    res = list(zip(*res))
    res.reverse()
    return res

mat = [ [[] for i in range(n) ] for j in range(n) ]
j = 1
    
for rot in range(2*n-1):
    for row in range(n//2+1):
        if [] in mat[row]:
            mat[row] = list(mat[row])
            imin = mat[row].index([])
            icnt = mat[row].count([])
            for i in range(imin,imin+icnt):
                mat[row][i] = j
                j += 1
            mat = rotate(mat)
            break

while mat[0][0] != 1:
    mat = rotate(mat)

print("Spiral Matrix:")
skip(1)
##print(mat)
print(np.matrix(mat))
skip(2)
