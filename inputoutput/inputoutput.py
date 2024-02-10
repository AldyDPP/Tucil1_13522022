# The tedious input output stuff. If you're reading this, there's absolutely nothing interesting here.

def txtInput(filename : str) :

    # init
    # m_width is not used, hence the underscore
    buffersize = 0 ; _m_width, m_height = 0, 0 ; seq_length = 0 
    matrix = [] ; seqs = [] ; seqvals = []

    # readfile
    lineidx = 0
    seqidx = 0
    with open(filename) as f :
        while True :
            line = f.readline().strip().split()

            if line[0] == "#" or not line :
                # line == whitespace or comments
                pass
            else : 

                if lineidx == 0 :
                    buffersize = line[0]

                elif lineidx == 1 :
                    _m_width, m_height = tuple(line)

                elif lineidx == 2 :
                    matrix.append(line)
                    for _ in range(m_height - 1) :
                        line = f.readline().strip().split()
                        matrix.append(line)

                elif lineidx == 3 :
                    seq_length = line[0]

                elif lineidx > 3 :
                    while seqidx < seq_length :
                        line1 = f.readline().strip().split()
                        if line1[0] == "#" or not line1 :
                            # line == whitespace or comments
                            continue
                        else :
                            line2 = f.readline().strip().split()
                            seqs.append("".join(line1))
                            seqvals.append(int(line2[0]))
                            seqidx += 1
                    break
        
    return matrix,buffersize,seqs,seqvals

from random import randint,choice
def generateRandom(seqs_length : int, maxseqlength : int,  tokens : set[str], m_width : int, m_height : int) :
    
    matrix = [[choice(tokens) for i in range(m_width)] for j in range(m_height)]
    seqs = [choice(tokens) for i in range(seqs_length)]
    seqvals = [randint(-100, 100) for i in range(seqs_length)]
    return matrix, seqs, seqvals

def cliInput() :

    _token_length = int(input("Input amount of unique tokens: "))
    inputmsg = "Input unique 2 character tokens seperated by a space:\n(e.g. BD 1C 7A 55 E9)"
    tokens = set([token for token in input(inputmsg).split()])
    buffersize = int(input("Input buffer size: "))
    inputmsg = "Input matrix sizes seperated by a space (width heigth): "
    m_width, m_height = tuple([int(n) for n in input(inputmsg)])
    seqs_length = int(input("Input minimum sequence length: "))
    maxseqlength = int(input("Input maximum sequence length: "))

    matrix, seqs, seqvals = generateRandom(seqs_length, maxseqlength, tokens, m_width, m_height)

    return matrix,buffersize,seqs,seqvals

def outputSolution(matrix, score, path_str, path) :
    print(f"Best score: {score}")
    print(f"Buffer: {path_str}")
    print("Path:")
    for i,j in path :
        print(f"{i}, {j}")
    for i in range(len(matrix)) :
        for j in range(len(matrix[0])) :
            print(matrix[i][j] if (i,j) in path else "--", end = " ")
        print()