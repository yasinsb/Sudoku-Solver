import numpy as np
#import numba as nb

def check_rbc(numlist):
    """
    :param numlist: list
        list of number to check
    :return:
        if a number other then zero repeats then false, else true
    """
    poslist = [x for x in numlist if x!=0]
    posset = set(poslist)
    if len(poslist) == len(posset):
        return True
    else:
        return False

def loopcheck(myarr):
    """
    :param myarr:
        9x9 array
    :return:
        if any row or column or block of 3x3 contains duplicates then False else True
    """
    for row in np.vstack((myarr,myarr.T)):
        if not check_rbc(row):
            return False
    for i in range(3):
        for j in range(3):
            mysqlist = myarr[i*3:i*3+3,j*3:j*3+3]
            if not check_rbc(mysqlist.flatten()):
                return False
    return True


def complist(myarr):
    """
    :param myarr:
        9x9 matrix
    :return:
        9x9 list of all possible combinations
    """
    #results = {}
    results_list = [[[] for i in range(9) ] for j in range(9)]
    for i in range(9):
        for j in range(9):
            myarr_copy = myarr.copy()
            for k in range(1,10):
                if myarr[i,j] ==0:
                    myarr_copy[i,j] = k
                    if loopcheck(myarr_copy):
                        results_list[i][j].append(k)
    return results_list


def backward_improve(myarr):
    improve = False
    comb = complist(myarr)
    for i in range(9):
        for j in range(9):
            if len(comb[i][j]) == 1:
                myarr[i,j] = comb[i][j][0]
                improve = True
    return myarr, improve

def find_unique(mylol):
    """
    :param mylol:
        a list of list
    :return:
        list of unique items
    """
    mylist = [j for i in mylol for j in i]
    basket = {}
    for item in set(mylist):
        if mylist.count(item) == 1:
            for i in range(9):
                if item in mylol[i]:
                    ind = i
                    break
            basket[item] = ind
    return basket

def column(matrix, i):
    return [row[i] for row in matrix]

def forward_improve(arr_in):
    myarr = arr_in.copy()
    improve = False
    comb = complist(myarr)
    for i in range(9):
        for item, ind in find_unique(comb[i]).items():
            myarr[i,ind] = item
    for j in range(9):
        for item, ind in find_unique(column(comb, j)).items():
            myarr[ind,j] = item
    for i in range(3):
        for j in range(3):
            mysqlist = []
            for i2 in range(3):
                for j2 in range(3):
                    mysqlist.append(comb[i*3+i2][j*3+j2])
            for item, ind in find_unique(mysqlist).items():
                myarr[i*3+ind//3][j*3+ind%3] = item
    improve = (arr_in != myarr).any()
    return myarr, improve

def improve_it(myarr):
    solsdk = myarr.copy()
    for iter in range(100):
        back_improve = True
        forw_improve = True
        solsdk, back_improve = backward_improve(solsdk)
        solsdk, forw_improve = forward_improve(solsdk)
        if back_improve  == False and forw_improve == False:
            return solsdk

def solve_sudoku(myarr,deep=0, smart=True):
    if deep == 100:
        print('Did not find a solution, something should be wring')
        return False, myarr
    comb = complist(myarr)
    if len(max([j for i in comb for j in i], key=len)) == 0:
        if np.sum(myarr == 0) == 0:
            return True, myarr #already solved
        else:
            return False, myarr #dead end
    else:
        shortest = list(range(1, 10))
        for i, row in enumerate(comb):
            for j, item in enumerate(row):
                if len(item)>0 and len(item)<len(shortest):
                    shortest = item
                    ind = (i,j)
        for item in shortest:
            guess_arr = myarr.copy()
            guess_arr[ind[0],ind[1]] = item
            if smart:
                guess_arr = improve_it(guess_arr)
            if np.sum(guess_arr == 0) == 0:
                return True, guess_arr
            else:
                return solve_sudoku(guess_arr,deep+1,smart=smart)

def main():
    import argparse
    parser = argparse.ArgumentParser(prog='Sudoku Solver 0.1')
    parser.add_argument('-s','--sudoku_array',type=list, help='Input a matrix-shaped list of numbers')
    args = parser.parse_args()
    result, solution = solve_sudoku(args.sudoku_array)
    if result:
        print(solution)

if __name__=='__main__':
    main()
