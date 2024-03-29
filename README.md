# Sudoku Solver

## What's the objective?
To find fastest algorithm to solve sudoku while making sure the algorithm gaurantees a solution. Hence this code is constantly updating as I come up with new ideas to spead up current procedures or remove redundencies. Feel free to contribute.

## How to use it?
The function reads an input of 9x9 numpy array.
The matrix takes zero where cell is not determined (value is unknown and to be solved).

example:
```python
  array_to_solve = numpy.array(
      [[1,0,4,0,0,0,5,0,2],
      [6,0,0,0,3,1,9,0,7],
      ...
      ]
      )
```

To run the solver function import it first and then use it to get the solution as a numpy array:


 ```python
 from sudoku_solver import solve_sudoku

 result, solution = solve_sudoku(array_to_solve)
```
 Note that the `result` will be `True` if and only if the module could find a feasible solution.

 If the default method fails you can use a dumber solution by calling it with option `smart = False`.

## Feasible Combinations - The intuitive way
Given the currently sitting numbers backward method ask if there is any cell that could be filled by only one specific number. This is what most people do when they try to solve Sudoku by pen and paper. If all one-combination cells are filled the code will try to go for two combinations and guess one, then three and ... untill there is a feasible solution.


## What's the smart option then?
The main part of algorithm is a recursive funtion which tries all the feasible combinations to find one that results in a solution. A feasible combination is any choice that does not voilate any of other sitting numbers (fundemental Sudoku rules).
Smart choice will try to speed-up the recursive method by finding all numbers which could only sit in one cell.

### More details
This imprvement ask if there is any number that could only sit in one place out of all possible places in a row, in a column or in a 3*3 block. It will fill-out all those cases with their inevitable choices.

To make it more clear assume we have a row as such
[0,0,0,1,2,3,4,5,6]
and let's say from feasible combinations we know that for the first three cells, the first could be filled by 7,8,9, second and third with 7,8. In this situation no cell has a determined number to choose but number 9 could only sit at the first cell and hence its place is determined.

In every iteration, which is guessing a feasible number for an undetermined cell, both forward and backward improvments will run to make sure no cell could be determined before trying to guess a number for next cell.

This method increased the solving speed by twice.
