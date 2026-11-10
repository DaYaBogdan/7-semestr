from Lab_2_scrapped import XSolver

A1 = [
    [0, 0, 0, 0, 0, 0, 0],   # x1
    [1, 0, 1, 0, 0, 0, 0],   # x2
    [0, 0, 0, 1, 0, 0, 1],   # x3
    [0, 1, 0, 0, 1, 1, 0],   # x4
    [0, 1, 0, 0, 0, 0, 0],   # x5
    [1, 0, 0, 1, 0, 0, 0],   # x6
    [0, 0, 1, 0, 0, 1, 0],   # x7
]

solver = XSolver(A1=A1)

solver.makeXmaps()
solver.printSolution()