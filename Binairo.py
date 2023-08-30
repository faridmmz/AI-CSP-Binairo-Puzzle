import copy
import sys
import State


def check_Adjancy_Limit(state: State):
    # check rows
    for i in range(0, state.size):
        for j in range(0, state.size - 2):
            if (state.board[i][j].value.upper() == state.board[i][j + 1].value.upper() and
                    state.board[i][j + 1].value.upper() == state.board[i][j + 2].value.upper() and
                    state.board[i][j].value != '_' and
                    state.board[i][j + 1].value != '_' and
                    state.board[i][j + 2].value != '_'):
                return False
    # check cols
    for j in range(0, state.size):  # cols
        for i in range(0, state.size - 2):  # rows
            if (state.board[i][j].value.upper() == state.board[i + 1][j].value.upper()
                    and state.board[i + 1][j].value.upper() == state.board[i + 2][j].value.upper()
                    and state.board[i][j].value != '_'
                    and state.board[i + 1][j].value != '_'
                    and state.board[i + 2][j].value != '_'):
                return False

    return True


def check_circles_limit(state: State):  # returns false if number of white or black circles exceeds board_size/2
    # check in rows
    for i in range(0, state.size):  # rows
        no_white_row = 0
        no_black_row = 0
        for j in range(0, state.size):  # each col
            # if cell is black or white and it is not empty (!= '_')
            if (state.board[i][j].value.upper() == 'W' and state.board[i][j].value != '_'): no_white_row += 1
            if (state.board[i][j].value.upper() == 'B' and state.board[i][j].value != '_'): no_black_row += 1
        if no_white_row > state.size / 2 or no_black_row > state.size / 2:
            return False

    # check in cols
    for j in range(0, state.size):  # cols
        no_white_col = 0
        no_black_col = 0
        for i in range(0, state.size):  # each row
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper() == 'W' and state.board[i][j].value != '_'): no_white_col += 1
            if (state.board[i][j].value.upper() == 'B' and state.board[i][j].value != '_'): no_black_col += 1
        if no_white_col > state.size / 2 or no_black_col > state.size / 2:
            return False

    return True


def is_unique(state: State):  # checks if all rows are unique && checks if all cols are unique
    # check rows
    for i in range(0, state.size - 1):
        for j in range(i + 1, state.size):
            count = 0
            for k in range(0, state.size):
                if (state.board[i][k].value.upper() == state.board[j][k].value.upper()
                        and state.board[i][k].value != '_'
                        and state.board[j][k].value != '_'):
                    count += 1
            if count == state.size:
                return False
            count = 0

    # check cols
    for j in range(0, state.size - 1):
        for k in range(j + 1, state.size):
            count_col = 0
            for i in range(0, state.size):
                if (state.board[i][j].value.upper() == state.board[i][k].value.upper()
                        and state.board[i][j].value != '_'
                        and state.board[i][k].value != '_'):
                    count_col += 1
            if count_col == state.size:
                return False
            count_col = 0

    return True


def is_assignment_complete(state: State):  # check if all variables are assigned or not
    for i in range(0, state.size):
        for j in range(0, state.size):
            if (state.board[i][j].value == '_'):  # exists a variable wich is not assigned (empty '_')

                return False

    return True


def is_consistent(state: State):
    return check_Adjancy_Limit(state) and check_circles_limit(state) and is_unique(state)


def check_termination(state: State):
    return is_consistent(state) and is_assignment_complete(state)

#in this function we first do all the preparations so then we can have a recursive function!
def backTrack(state: State):
    #we need to first run forward check or ac3 for out pre assigned cells
    forwardCheck(0, 0, state, "start")
    #ac3(state,"normal")
    #we increase recursion limit in case of a huge test case!
    sys.setrecursionlimit((10 ** 9))
    #and now we call our recursive backtrack and whether it succeed or not we print the solved puzzle
    return recursiveBackTrack(state)


def recursiveBackTrack(state: State):
    #our base rule to end recursion
    if check_termination(state):
        return True
    cellChosed = False
    #calling mrv
    x, y, hasMrv = mrv(state)

    if hasMrv:
        cellChosed = True
    #in case of not having mrv we use normal back track!
    while not  cellChosed:
        for i in range(state.size):
            for j in range(state.size):
                if state.board[i][j].value == '_':
                    x = state.board[i][j].x
                    y = state.board[i][j].y
                    cellChosed = True
    #calling lcv to find the best domain!
    state.board[x][y].domain = lcv(x,y,state)
    #now we try recursion on our backtrack and solve it!
    for choice in state.board[x][y].domain:
        state.board[x][y].value = choice
        if is_consistent(state):
            forwardCheck(x, y, state, "normal")
            result = recursiveBackTrack(state)
            if result:
                return result
        #in case of backtrack we call the reverse mood of forwardcheck or ac3
        state.board[x][y].value = '_'
        forwardCheck(x, y, state, "reverse")
        #ac3(state,"reverse")

    return False

#forward checking has 3 moods for start, normal check and reverse for back tracking
def forwardCheck(x: int, y: int, state: State, mood: str):
    if mood == 'start':
        domainList = copy.deepcopy(state.board)
        for i in range(state.size):
            for j in range(state.size):
                if state.board[i][j].value != '_':
                    continue
                else:
                    tempCellValue = state.board[i][j].value
                    for choice in domainList[i][j].domain:
                        state.board[i][j].value = choice
                        if is_consistent(state):
                            continue
                        else:
                            if choice in state.board[i][j].domain:
                                tempStr = copy.deepcopy(state.board[i][j].domain)
                                tempStr.remove(choice)
                                state.board[i][j].domain = tempStr
                    state.board[i][j].value = tempCellValue

    if mood == 'normal':
        for i in range(state.size):
            if state.board[i][y].value != '_':
                continue
            if i == x:
                continue
            tempCellValue = state.board[i][y].value
            for choice in state.board[i][y].domain:
                state.board[i][y].value = choice
                if is_consistent(state):
                    continue
                else:
                    # print("current cell:",x,y,state.board[x][y].value)
                    # print("problem cell:",i,y,state.board[i][y].value)
                    if choice in state.board[i][y].domain:
                        tempStr = copy.deepcopy(state.board[i][y].domain)
                        tempStr.remove(choice)
                        state.board[i][y].domain = tempStr
            state.board[i][y].value = tempCellValue

        for i in range(state.size):
            if state.board[x][i].value != '_':
                continue
            if i == y:
                continue
            tempCellValue = state.board[x][i].value
            for choice in state.board[x][i].domain:
                state.board[x][i].value = choice
                if is_consistent(state):
                    continue
                else:
                    # print("current cell:", x, y,state.board[x][y].value)
                    # print("problem cell:", x, i,state.board[x][i].value)
                    if choice in state.board[x][i].domain:
                        tempStr = copy.deepcopy(state.board[x][i].domain)
                        tempStr.remove(choice)
                        state.board[x][i].domain = tempStr
            state.board[x][i].value = tempCellValue

    if mood == "reverse":
        for i in range(state.size):
            tempStrlist = []
            if state.board[i][y].value != '_':
                continue
            if (i == x):
                continue
            state.board[i][y].value = 'w'
            if is_consistent(state):
                tempStrlist.append('w')
            state.board[i][y].value = 'b'
            if is_consistent(state):
                tempStrlist.append('b')
            state.board[i][y].value = '_'
            state.board[i][y].domain = tempStrlist
        for i in range(state.size):
            tempStrlist = []
            if state.board[x][i].value != '_':
                continue
            if (i == y):
                continue
            state.board[x][i].value = 'w'
            if is_consistent(state):
                tempStrlist.append('w')
            state.board[x][i].value = 'b'
            if is_consistent(state):
                tempStrlist.append('b')
            state.board[x][i].value = '_'
            state.board[x][i].domain = tempStrlist
    return

#mrv return if it succeed and the targeted cell
def mrv(state: State):
    #print("finding mrv")
    hasMrv = False
    min = 2
    for i in range(state.size):
        for j in range(state.size):
            if len(state.board[i][j].domain) < min and state.board[i][j].domain != ['n'] and state.board[i][j].value == '_':
                #print("mrv found", i , j , state.board[i][j].domain)
                hasMrv = True
                return i, j, hasMrv

    return 0, 0, hasMrv

#lcv change the domain as the choice with better chances for other cells has advantage of being choosed
def lcv(x : int, y : int, state : State):
    lcv = copy.deepcopy(state)
    if len(lcv.board[x][y].domain) <= 1:
        return lcv.board[x][y].domain
    else:
        x1 = 0
        x2 = 0
        lcv.board[x][y].value = lcv.board[x][y].domain[0]
        for i in range(lcv.size):
            if lcv.board[i][y].value != '_':
                continue
            if i == x:
                continue
            tempCellValue = lcv.board[i][y].value
            for choice in lcv.board[i][y].domain:
                lcv.board[i][y].value = choice
                if is_consistent(lcv):
                    continue
                else:
                    # print("current cell:",x,y,state.board[x][y].value)
                    # print("problem cell:",i,y,state.board[i][y].value)
                    if choice in lcv.board[i][y].domain:
                        x1 += 1
            lcv.board[i][y].value = tempCellValue

        for i in range(lcv.size):
            if lcv.board[x][i].value != '_':
                continue
            if i == y:
                continue
            tempCellValue = lcv.board[x][i].value
            for choice in lcv.board[x][i].domain:
                lcv.board[x][i].value = choice
                if is_consistent(lcv):
                    continue
                else:
                    # print("current cell:", x, y,state.board[x][y].value)
                    # print("problem cell:", x, i,state.board[x][i].value)
                    if choice in lcv.board[x][i].domain:
                        x1 += 1
            lcv.board[x][i].value = tempCellValue

        lcv.board[x][y].value = lcv.board[x][y].domain[1]
        for i in range(lcv.size):
            if lcv.board[i][y].value != '_':
                continue
            if i == x:
                continue
            tempCellValue = lcv.board[i][y].value
            for choice in lcv.board[i][y].domain:
                lcv.board[i][y].value = choice
                if is_consistent(lcv):
                    continue
                else:
                    # print("current cell:",x,y,state.board[x][y].value)
                    # print("problem cell:",i,y,state.board[i][y].value)
                    if choice in lcv.board[i][y].domain:
                        x2 += 1
            lcv.board[i][y].value = tempCellValue

        for i in range(lcv.size):
            if lcv.board[x][i].value != '_':
                continue
            if i == y:
                continue
            tempCellValue = lcv.board[x][i].value
            for choice in lcv.board[x][i].domain:
                lcv.board[x][i].value = choice
                if is_consistent(lcv):
                    continue
                else:
                    # print("current cell:", x, y,state.board[x][y].value)
                    # print("problem cell:", x, i,state.board[x][i].value)
                    if choice in lcv.board[x][i].domain:
                        x2 += 1
            lcv.board[x][i].value = tempCellValue

        str = []
        if x1 <= x2:
            str.append(lcv.board[x][y].domain[0])
            str.append(lcv.board[x][y].domain[1])
        else:
            str.append(lcv.board[x][y].domain[1])
            str.append(lcv.board[x][y].domain[0])

        return str

#ac3 works like forward check but it only has 2 moods for normal and reverse cause there is no difference when we call it.
def ac3(state : State, mood: str):
    if mood == 'normal':
        queue = []
        for x in range(state.size):
            for y in range(state.size):
                for i in range(state.size):
                    if state.board[x][y].value != '_' or state.board[i][y].value != '_':
                        continue
                    if i == x:
                        continue
                    for choice1 in state.board[x][y].domain:
                        consistent = False
                        for choice2 in state.board[i][y].domain:
                            state.board[x][y].value = choice1
                            state.board[i][y].value = choice2
                            if is_consistent(state):
                                consistent = True
                        if not consistent:
                            if choice1 in state.board[x][y].domain:
                                tempStr = copy.deepcopy(state.board[x][y].domain)
                                tempStr.remove(choice1)
                                state.board[x][y].domain = tempStr
                                queue.append(state.board[x][y])
                    state.board[x][y].value = '_'
                    state.board[i][y].value = '_'

                for i in range(state.size):
                    if state.board[x][y].value != '_' or state.board[x][i].value != '_':
                        continue
                    if i == y:
                        continue
                    for choice1 in state.board[x][y].domain:
                        consistent = False
                        for choice2 in state.board[x][i].domain:
                            state.board[x][y].value = choice1
                            state.board[x][i].value = choice2
                            if is_consistent(state):
                                consistent = True
                        if not consistent:
                            if choice1 in state.board[x][y].domain:
                                tempStr = copy.deepcopy(state.board[x][y].domain)
                                tempStr.remove(choice1)
                                state.board[x][y].domain = tempStr
                                queue.append(state.board[x][y])
                    state.board[x][y].value = '_'
                    state.board[x][i].value = '_'
        while queue:
            cell = queue.pop()
            for i in range(state.size):
                if state.board[cell.x][cell.y].value != '_' or state.board[i][cell.y].value != '_':
                    continue
                if i == cell.x:
                    continue
                for choice1 in state.board[cell.x][cell.y].domain:
                    consistent = False
                    for choice2 in state.board[i][cell.y].domain:
                        state.board[cell.x][cell.y].value = choice1
                        state.board[i][cell.y].value = choice2
                        if is_consistent(state):
                            consistent = True
                    if not consistent:
                        if choice1 in state.board[cell.x][cell.y].domain:
                            tempStr = copy.deepcopy(state.board[cell.x][cell.y].domain)
                            tempStr.remove(choice1)
                            state.board[cell.x][cell.y].domain = tempStr
                            queue.append(state.board[cell.x][cell.y])
                state.board[cell.x][cell.y].value = '_'
                state.board[i][cell.y].value = '_'

            for i in range(state.size):
                if state.board[cell.x][cell.y].value != '_' or state.board[cell.x][i].value != '_':
                    continue
                if i == cell.y:
                    continue
                for choice1 in state.board[cell.x][cell.y].domain:
                    consistent = False
                    for choice2 in state.board[cell.x][i].domain:
                        state.board[cell.x][cell.y].value = choice1
                        state.board[cell.x][i].value = choice2
                        if is_consistent(state):
                            consistent = True
                    if not consistent:
                        if choice1 in state.board[cell.x][cell.y].domain:
                            tempStr = copy.deepcopy(state.board[cell.x][cell.y].domain)
                            tempStr.remove(choice1)
                            state.board[cell.x][cell.y].domain = tempStr
                            queue.append(state.board[cell.x][cell.y])
                state.board[x][y].value = '_'
                state.board[x][i].value = '_'
    if mood == "reverse":
        for x in range(state.size):
            for y in range(state.size):
                tempStrlist = []
                state.board[x][y].value = 'w'
                consistent = True
                for i in range(state.size):
                    for domain in state.board[i][y].domain:
                        if not is_consistent(state):
                            consistent =False
                for i in range(state.size):
                    for domain in state.board[x][i].domain:
                        if not is_consistent(state):
                            consistent =False
                if consistent == True:
                    tempStrlist.append('w')
                state.board[x][y].value = 'b'
                consistent = True
                for i in range(state.size):
                    for domain in state.board[i][y].domain:
                        if not is_consistent(state):
                            consistent = False
                for i in range(state.size):
                    for domain in state.board[x][i].domain:
                        if not is_consistent(state):
                            consistent = False
                if consistent == True:
                    tempStrlist.append('b')

                state.board[x][y].domain = tempStrlist
                state.board[x][y].value = '_'