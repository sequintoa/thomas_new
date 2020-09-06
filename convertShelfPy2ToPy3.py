# Opening Python 2 Shelf database files in Python 3
# https://stackoverflow.com/questions/27493733/use-python-2-shelf-in-python-3

import shelve
import dumbdbm
import anydbm
import dbm 

def dumbdbm_shelve(filename,flag="c"):
    return shelve.Shelf(dumbdbm.open(filename,flag))

out_shelf=dumbdbm_shelve("cv_optimal_picsl_parameters.dumbdbm.shelve")
in_shelf=shelve.open("cv_optimal_picsl_parameters.shelve")

key_list=in_shelf.keys()
for key in key_list:
    new_key = "PICSL"
    out_shelf[new_key]=in_shelf[key]
    print('Key: ',key)
    print('inp: ', in_shelf[key])
    print('op: ', out_shelf[new_key])
    
out_shelf.close()
in_shelf.close()

