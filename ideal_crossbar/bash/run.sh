#!/usr/bin/zsh

for i in {1..$4}
do
    for rows in {$1..$2..$3}
    do
        echo "Iteration $i for $rows rows"
        python ../src/main.py $rows 4 $i
    done
done