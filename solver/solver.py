# TUCIL 1 STIMA

# Functions to generate the paths
def generatePath(matrix, i, j, buffer : int, path : list[str], vertical : bool, result) -> None :
    
    result.append(path.copy())
    if buffer == 0 :
        return
    
    else :

        if vertical : 
            for newi in range(len(matrix)) :
                if (newi,j) not in path :
                    path.append((newi,j))
                    generatePath(matrix, newi, j, buffer-1, path, not(vertical), result)
                    path.pop()

        else :
            for newj in range(len(matrix[0])) :
                if (i,newj) not in path :
                    path.append((i,newj))
                    generatePath(matrix, i, newj, buffer-1, path, not(vertical), result)
                    path.pop()

def generateAllPaths(matrix : list[list[str]], buffer : int) -> list[list[str]] :
    result = list()
    for j in range(len(matrix[0])) :
        path = [(0,j)]
        generatePath(matrix, i=0, j=j, buffer=buffer-1, path=path, vertical=True, result = result)

    return result

def pathToString(matrix, path : list[tuple]) -> list[str] :
    return "".join([matrix[i][j] for (i,j) in path])

""""""

# Find the points/value/score/whatever_that_is of a path given an array of sequences and their values
def pathValue(path_str : str, sequenceValues : list[int], sequences : list[str]) :
    
    ans = 0
    for seq,val in zip(sequences, sequenceValues) :
        idx = path_str.find(seq)
        if idx > -1 and idx % 2 == 0 : 
            ans += val
    return ans

def solve(matrix, buffer, sequences, sequenceValues) :

    # Generate all possible paths
    paths = generateAllPaths(matrix, buffer)

    # Convert all paths to token strings, store in second array
    path_strs = [pathToString(matrix, path) for path in paths]
    ans,ansidx = 0,0

    # Each path is evaluated. Find the index of the max/best path as well as its value
    for idx,path in enumerate(path_strs) :
        v = pathValue(path, sequenceValues, sequences)
        if v > ans :
            ans = v
            ansidx = idx
        elif v == ans and len(path_strs[idx]) < len(path_strs[ansidx]) :
            ansidx = idx
    
    bestpathstr = path_strs[ansidx]
    bestpathstr = " ".join([bestpathstr[i:i+2] for i in range(0, len(bestpathstr), 2)])
    bestpath = paths[ansidx]
    
    return ans,bestpathstr,bestpath