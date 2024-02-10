# The tedious input output stuff. If you're reading this, there's absolutely nothing interesting here.

def printMatrix(matrix) :
    for row in matrix :
        print(" ".join(row))

def printSequences(seqs, seqvals) :
    for i,(seq,val) in enumerate(zip(seqs,seqvals)) :
        print(f"Sequence {i+1}: {' '.join([seq[i:i+2] for i in range(0, len(seq), 2)])} ({val} points)")

def txtInput(filename : str) :

    # init
    # m_width is not used, hence the underscore
    buffersize = 0 ; _m_width, m_height = 0, 0 ; seq_length = 0 
    matrix = [] ; seqs = [] ; seqvals = []

    # readfile
    lineidx = 0
    seqidx = 0

    try :

        with open(filename) as f :
            while True :
                line = f.readline().strip().split()

                if not line or line[0][0] == "#" :
                    # line == whitespace or comments
                    pass
                else : 

                    if lineidx == 0 :
                        buffersize = int(line[0])

                    elif lineidx == 1 :
                        _m_width, m_height = tuple(map(int, line))

                    elif lineidx == 2 :
                        matrix.append(line)
                        for _ in range(m_height - 1) :
                            line = f.readline().strip().split()
                            matrix.append(line)

                    elif lineidx == 3 :
                        seq_length = int(line[0])
                        while seqidx < seq_length :
                            line1 = f.readline().strip().split()
                            if not line1 or line1[0][0] == "#" :
                                # line == whitespace or comments
                                continue
                            else :
                                line2 = f.readline().strip().split()
                                seqs.append("".join(line1))
                                seqvals.append(int(line2[0]))
                                seqidx += 1
                        break

                    lineidx += 1
    
    except : 

        return [],-1,[],[]
        
    return matrix,buffersize,seqs,seqvals

from random import randint,choice
def generateRandom(seqs_length : int, maxseqlength : int,  tokens : set[str], m_width : int, m_height : int) :
    
    tokens = list(tokens)
    matrix = [[choice(tokens) for i in range(m_width)] for j in range(m_height)]
    seqs = ["".join([choice(tokens) for k in range(randint(1,maxseqlength))]) for i in range(seqs_length)]
    seqvals = [randint(-100, 100) for i in range(seqs_length)]

    return matrix, seqs, seqvals

def cliInput() :

    token_length = 0 ; buffersize = 0 ; m_width, m_height = 0, 0 ; seqs_length = 0 ; maxseqlength = 0 
    tokens = [] ; errormsg = "Please make sure your inputs are correctly formatted."
    try :

        token_length = int(input("Input amount of unique tokens: "))
        if token_length < 1 :
            errormsg = "Amount of tokens must be a positive integer."
            raise ValueError
        
        inputmsg = "Input unique 2 character tokens seperated by a space:\n(e.g. BD 1C 7A 55 E9)\n\n"
        tokens = set([token for token in input(inputmsg).split()])
        if len(tokens) != token_length :
            errormsg = "Tokens must be unique. Also, make sure you've inputted the correct amount of tokens!"
            raise ValueError
        for i in tokens :
            if len(i) != 2 or not str.isalnum(i[0]) or not str.isalnum(i[1]):
                errormsg = "Tokens must be two alphanumeric characters."
                raise ValueError

        buffersize = int(input("Input buffer size: "))
        if buffersize < 1 :
            errormsg = "Buffer size must be a positive integer."
            raise ValueError
        
        inputmsg = "Input matrix sizes seperated by a space (width heigth): "
        m_width, m_height = tuple([int(n) for n in input(inputmsg).split()])
        if m_width <= 0 or m_height <= 0 :
            errormsg = "Matrix sizes must be positive integers."
            raise ValueError

        seqs_length = int(input("Input amount of sequences: "))
        if seqs_length <= 0 :
            errormsg = "Amount of sequences must be a positive integer."
            raise ValueError
        
        maxseqlength = int(input("Input maximum sequence length: "))
        if maxseqlength <= 0 :
            errormsg = "Maximum sequence length must be a positive integer."
            raise ValueError

    except ValueError :
        return [],-1,[],errormsg
    
    matrix, seqs, seqvals = generateRandom(seqs_length, maxseqlength, tokens, m_width, m_height)

    return matrix,buffersize,seqs,seqvals

def outputSolution(matrix, score, path_str, path, exec_time) :
    print(f"Best score: {score}")
    print(f"Buffer: {path_str}")
    print("Path:")
    for i,j in path :
        print(f"{i}, {j}")
    for i in range(len(matrix)) :
        for j in range(len(matrix[0])) :
            print(matrix[i][j] if (i,j) in path else "--", end = " ")
        print()
    print(f"Done in {exec_time:.2f} ms!")
    print()

    if input("Output to txt file? (y/n): ") == 'y' :
        with open("output.txt", mode = "w") as f :
            f.write(f"Best score: {score}\n")
            f.write(f"Buffer: {path_str}\n")
            f.write("Path:\n")
            for i,j in path :
                f.write(f"{i}, {j}\n")
            matrixStr = ""
            for i in range(len(matrix)) :
                for j in range(len(matrix[0])) :
                    matrixStr += (matrix[i][j] if (i,j) in path else "--") + " "
                matrixStr += "\n"
            f.write(matrixStr)
            f.write(f"Done in {exec_time:.2f} ms!")


def ui() :
    print("Welcome to my Cyberpunk 2077 Breach Protocol solver!")
    print("Go ahead and choose your method of input:")
    print("1. Command Line (direct) input.")
    print("2. Txt file input.\n")
    choice = int(input("1/2: "))
    
    return choice