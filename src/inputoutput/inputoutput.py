# The tedious input output stuff. If you're reading this, there's absolutely nothing interesting here.

def printMatrix(matrix) :
    for row in matrix :
        print(" ".join(row))

def printSequences(seqs, seqvals) :
    for i,(seq,val) in enumerate(zip(seqs,seqvals)) :
        print(' '.join([seq[i:i+2] for i in range(0, len(seq), 2)]))
        print(val)

def txtInput(filename : str) :

    # init
    buffersize = 0 ; m_width, m_height = 0, 0 ; seq_length = 0 
    matrix = [] ; seqs = [] ; seqvals = []

    # readfile
    lineidx = 0
    seqidx = 0

    try :

        with open(filename) as f :
            while True :
                line = f.readline()

                if not line :
                    raise ValueError
                else :
                    line = line.strip().split()

                if not line or line[0][0] == "#" :
                    # line == whitespace or comments
                    pass
                else : 

                    if lineidx == 0 :
                        buffersize = int(line[0])

                    elif lineidx == 1 :
                        m_width, m_height = tuple(map(int, line))

                    elif lineidx == 2 :
                        matrix.append(line)
                        for _ in range(m_height - 1) :
                            line = f.readline().strip().split()
                            if len(line) != m_width:
                                raise ValueError
                            matrix.append(line)

                    elif lineidx == 3 :
                        seq_length = int(line[0])
                        while seqidx < seq_length :
                            line1 = f.readline()
                            if not line1 :
                                raise ValueError
                            else :
                                line1 = line1.strip().split()
                            
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

from random import randint,choice,sample
from itertools import product
def generateRandom(seqs_length : int, maxseqlength : int,  tokens : set[str], m_width : int, m_height : int) :
    
    tokens = list(tokens)
    matrix = [[choice(tokens) for i in range(m_width)] for j in range(m_height)]
    possibleseqs = []
    for l in range(2, maxseqlength + 1) :
        possibleseqs += product(tokens, repeat=l)
    seqs = sample(possibleseqs, seqs_length)
    seqs = list(map("".join, seqs))
    seqvals = [randint(-100, 100) for i in range(seqs_length)]

    return matrix, seqs, seqvals

def possibleAmountOfSequences(maxseqlength : int, tokens : set[str]) :
    ans = 0
    l = len(tokens)
    for i in range(2, maxseqlength+1) :
        ans += l ** i
    return ans

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

        maxseqlength = int(input("Input maximum sequence length: "))
        if maxseqlength <= 0 :
            errormsg = "Maximum sequence length must be a positive integer."
            raise ValueError
        
        seqs_length = int(input("Input amount of sequences: "))
        if seqs_length <= 0 :
            errormsg = "Amount of sequences must be a positive integer."
            raise ValueError
        
        if possibleAmountOfSequences(maxseqlength, tokens) < seqs_length :
            errormsg = "The amount of possible sequences that can be generated is smaller than the number you provided. Try putting in more unique tokens or increase the maximum sequence length."
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
        print(f"{j+1}, {i+1}")
    print()
    for i in range(len(matrix)) :
        for j in range(len(matrix[0])) :
            print(matrix[i][j] if (i,j) in path else "--", end = " ")
        print()
    print()
    print(f"Done in {exec_time:.2f} ms!")
    print()

    if input("Output to txt file? (y/n): ") == 'y' :
        filename = input("Input filename (if you don't enter anything, output.txt will be used): ")
        filename = filename if filename else "output.txt"
        with open(filename, mode = "w") as f :
            f.write(f"{score}\n")
            f.write(f"{path_str}\n")
            for i,j in path :
                f.write(f"{j+1}, {i+1}\n")
            f.write(f"\n{exec_time:.2f} ms")
        print("Done!")
    else :
        print("Goodbye!")

def ui() :

    try :
        print("Welcome to my Cyberpunk 2077 Breach Protocol solver!")
        print("Go ahead and choose your method of input:")
        print("1. Command Line (direct) input.")
        print("2. Txt file input.\n")
        choice = int(input("1/2: "))
        if choice not in [1,2] : choice = 3
        return choice

    except ValueError : return 3

if __name__ == "__main__" :
    matrix, seqs, seqvals = generateRandom(27, 5, {"AA", "BB", "CC"}, 6, 6)
    print(seqs)