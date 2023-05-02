# Results for basic experiment

This experiment has 3 sizes of crossbar and only 2 values for the variation, one zero and one high.
The crossbars have 10, 250, 500 rows and 250 columns.
The variations are set to 0 for both relative and abs, and 1 for each abs and relative respectively.
Each experiment is repeated 100 times (for 250*100=2500 results for each)

## Experiments

|--|----|-----|----|----|----|
| #| rep| size| abs| rel|conf|
|--|----|-----|----|----|----|
|01| 10 |  10 | 0  |  0 | 1  |
|02| 10 |  10 | 1  |  0 | 1  |
|03| 10 |  10 | 0  |  1 | 1  |
|04| 10 |  10 | 1  |  1 | 1  |
|05| 10 | 250 | 0  |  0 | 2  |
|06| 10 | 250 | 1  |  0 | 2  |
|07| 10 | 250 | 0  |  1 | 2  |
|08| 10 | 250 | 1  |  1 | 2  |
|09| 10 | 500 | 0  |  0 | 3  |
|10| 10 | 500 | 1  |  0 | 3  |
|11| 10 | 500 | 0  |  1 | 3  |
|12| 10 | 500 | 1  |  1 | 3  |
|--|----|-----|----|----|----|

Total 120 runs, split into 3 running scripts using 4 configuration files.
