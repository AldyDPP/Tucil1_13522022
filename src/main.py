from inputoutput.inputoutput import *
from solver.solver import *
from time import perf_counter
import os

def main() :
    # Initialize
    os.system("cls" if os.name == "nt" else "clear")
    matrix, buffersize, seqs, seqvals = [],0,[],[]
    
    # Input
    choice = ui()
    if choice == 1 :
        matrix, buffersize, seqs, seqvals = cliInput()
        if not matrix :
            errormsg = seqvals # errormsg is returned through seqvals in cliInput() if an error is raised
            print(f"Error. {errormsg}")
            return
    elif choice == 2 :
        filename = input("Input filename (input.txt will be chosen by default if you input nothing): ")
        filename = filename if filename else "input.txt"
        matrix, buffersize, seqs, seqvals = txtInput(filename)
        if not matrix :
            print("Failed to read file. Please make sure the filename is correct and the file is correctly formatted!")
            return
    else :
        print("Please input correctly.")
        return

    # Solve
    os.system("cls" if os.name == "nt" else "clear")
    print("Solving...")
    print("Hang on! This may take a while if the buffer size and/or matrix is large...")
    start = perf_counter()
    ans, pathstr, path = solve(matrix, buffersize, seqs, seqvals)
    end = perf_counter()
    os.system("cls" if os.name == "nt" else "clear")
    exec_time = (end - start) * 1000 # in ms

    # Output
    if choice == 1 :
        print(f"{'*':-^20}")
        print("Generated matrix: ")
        printMatrix(matrix)
        print()
        print("Generated sequences:")
        printSequences(seqs, seqvals)
        print()
    outputSolution(matrix, ans, pathstr, path, exec_time)

if __name__ == "__main__" :
    main()