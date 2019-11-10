import yaml
import numpy as np
from sudoku_solver import solve_sudoku

example = yaml.safe_load(open('example.yml','r'))['example1']

result, solution = solve_sudoku(np.array(example))
if result:
    print(solution)