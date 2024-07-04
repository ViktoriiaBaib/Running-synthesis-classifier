#!/bin/bash

for VAR in $(seq 0 1 10)
do
    sed -i '/python classify.py/c\python classify.py -i '"$VAR"' -b 200000 -c A' batch.sub
    sbatch batch.sub
done