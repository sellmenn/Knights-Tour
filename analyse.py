from search import find_KT
from game import *
from time import time, sleep
import sys
import os
from pyfiglet import Figlet

MAX = 500000 # Cycle limit for search algorithm
H_PROB = 1 # Probability that Warnsdorff’s Rule is conformed to when adding Node objects to Frontier

def main():
    print("\nA personal project by Ariq Koh -- Github ID: sellmenn\n")
    f = Figlet(font='slant')
    print(f.renderText("Knight's Tour"))
    try:
        var, length = str(sys.argv[1]).upper(), int(sys.argv[2])
        sleep(3)
    except:
        print("\nCommand line argument usage: python3 analyse.py open/closed length\n")
        print("Configuration menu:")
        var = input("Search 'open' or 'closed' variants: ").upper()
        length = input("Length of board: ")
    try:
        analyse_KT(length=int(length), limit=MAX, h_prob=H_PROB, var=var.upper(), csv_file=f"{var.capitalize()}_KT.csv")
    except:
        print("\nInvalid input.\nCommand line argument usage: python3 analyse.py open/closed length\n")

def analyse_KT(length=8, limit=500000, h_prob=1, var="OPEN", csv_file="OpenTour.csv"):
    # Create directory 'Results' if it does not already exist
    if not os.path.exists("Results"): 
        os.makedirs("Results") 
    print(f"\nSearch for solutions to {var.capitalize()} Knight's Tour.\nBoard size: {length}*{length}\nH_PROB: {h_prob}\nSearch limit: {limit} / start coordinate")
    # Initialise count and start time
    start_time = time()
    total_count = 0
    # Write csv file headers
    with open(f"Results/{csv_file}", "w") as file:
        file.write("iterations, start coordinate, number of solutions\n")
    # For each coordinate on the board
    for i in range(length):
        for j in range(length):
            print(f"\nStart coordinate ({i}, {j}):")
            # Obtain number of solutions while writing them into txt files
            solution_count = find_KT(piece=Knight(position=(i,j), board=Board(length=length)), start=(i, j), h_prob=h_prob, var=var, limit=limit, file_name=f"Results/{var.capitalize()}_{i}{j}.txt")
            # Add to solution count
            total_count += solution_count
            print(f"{solution_count} tours found. Refer to Results/{var.capitalize()}_{i}{j}.txt.")
            # Append count to csv file
            with open(f"Results/{csv_file}", "a") as file:
                file.write(f'{limit}, "{(i, j)}", {solution_count}\n')
    elapsed_time = time()- start_time
    print(f"\nSearch completed for {var.capitalize()} Knight's Tour in {elapsed_time:.2f} seconds.\nBoard size: {length}*{length}\nH_PROB: {h_prob}\nSearch limit: {limit} / start coordinate\n{total_count} tours found.")
    
if __name__ == "__main__":
    main()

