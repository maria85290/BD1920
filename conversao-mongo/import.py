#!/bin/python3

import os

print(os.listdir('.'))

for x in os.listdir('.'):
  if x.endswith('.json'):
    print(f"Importing file: {x}")
    os.system(f"mongoimport -d TestesClinicos -c {x[:-5]} --jsonArray < {x}")


