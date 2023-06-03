
import queue
import sys
# Sean O'Sullivan
# Date: 09/07/2022
# Filename: words.py
#
# Description: Implementation of a BFS algorithm to find a
# shortest path of words from a given start word to a given
# goal word. At each step, any single letter in the word
# can be changed to any other letter, provided
# that the resulting word is also in the dictionary.
# 
# A dictionary of English words a text file, a start word,
# and a goal word are passed as command line arguments.
# 
# Usage: python3 words.py dictionaryFile startWord endWord

# Python queue implementation (https://docs.python.org/3.5/library/collections.html?highlight=deque#collections.deque)
from collections import deque
from tracemalloc import start


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent

    # Nodes with the same state are viewed as equal
    def __eq__(self, other_node):
        return isinstance(other_node, Node) and self.state == other_node.state
    
    # Nodes with the same state hash to the same value
    # (e.g., when storing them in a set or dictionary)
    def __hash__(self):
        return hash(self.state)

def read_file(filename):
    """Read in each word from a dictionary where each
    word is listed on a single line."""
    print("Reading dictionary: " +filename)
    word_dict = set()

    dictionary = open(filename)

    # Read each word from the dictionary
    for word in dictionary:
        # Remove the trailing newline character
        word = word.rstrip('\n')

        # Convert to lowercase
        word = word.lower()

        word_dict.add(word)

    dictionary.close()

    return word_dict

def find_path(startWord, goalWord, word_dict):
    alphabet = "abcdefghijklmnopqrstuvwxyz" #All possible letters to change
    frontier = deque() #Words that will be explored
    explored = set() 
    ans = deque() #Deque will contain a shortest path solution
    visited = set() #Set to keep track of words that have already been used

    # Declare start and goal nodes
    goal = Node(goalWord, None) 
    s = Node(startWord, None)

    # If the start word and goal word are the same; add the word to ans deque and return it
    if s.__eq__(goal):
        ans.appendleft(goal.state)
        return ans

    # Append starting word node to the frontier
    frontier.append(s)

    while frontier: #While frontier is not empty
        x = frontier.popleft() 
        explored.add(x.state) #add node state from the left of the frontier to the explored set

        for i in range(len(startWord)): # Nested for loop that changes one character at a time of the current word
            for j in alphabet:
                newWord = x.state[:i] + j + x.state[i+1:] # New possible word
                valid = newWord in word_dict # Check if the new word is a valid word from the dictionary
                if valid:
                    child = Node(newWord, x) # If it is a valid word, create a new child node where child.state = newWord and 
                                             # child.parent = x (the previous node)

                    # Check to see if the word has already been explored, and not in the frontier, or ever been seen before
                    if child.state not in explored and child.state not in frontier and child.state not in visited:
                        visited.add(child.state) # add the new word to the visited set
                        if child.__eq__(goal): # If the new word is the goal word, trace through the path and add it to ans
                                               # then return ans
                            while child != None:
                                ans.appendleft(child.state)
                                child = child.parent
                            return ans
                        frontier.append(child) # If new word doesn't equal the goal word, append to frontier
                    
    return None # Return none if no path exists.

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 words.py dictionaryFile startWord goalWord")
    else:
        dictionaryFile = sys.argv[1]
        startWord = sys.argv[2]
        goalWord = sys.argv[3]

        word_dict = set()
        word_dict = read_file(dictionaryFile)

        if startWord not in word_dict:
            print(startWord + " is not in the given dictionary.")
        else:
            print("-- Shortest path from " + startWord + " to " + goalWord + " --")
            
            solution = find_path(startWord, goalWord, word_dict)

            if(solution is None):
                print("None exists!")
            else:
                for word in solution:
                    print(word)

if __name__ == "__main__":
    main()
