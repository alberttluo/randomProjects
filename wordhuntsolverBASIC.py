# For GamePigeon Word Hunt, going to implement custom sizing soon.

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('letters', metavar='lets', type=str)
args = parser.parse_args()
string_input = args.letters
file_path = '/Users/albertluo/wordhuntbot/scrabDictionary.txt'

NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1),(0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def load_dict(file_path):
    with open(file_path, 'r') as file:
        dictionary = set(word.strip().lower() for word in file)
    return dictionary

dictionary = load_dict(file_path)

def solve(grid):
    results = []
    words = set(word for word in dictionary if len(word) >= 3)
    prefix_set = set(word[:i] for word in words for i in range(1, len(word) + 1))
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            results += get_possible_words(grid, words, prefix_set, grid[y][x], y, x, set([(y, x)]))

    return set(results)



def generate_grid(string):
    if len(string) != 16:
        print("Invalid string length. Please provide a string of exactly 16 characters.")
        return None

    array_4x4 = [[0] * 4 for _ in range(4)]
    index = 0

    for i in range(4):
        for j in range(4):
            array_4x4[i][j] = string[index]
            index += 1

    return array_4x4

grid = generate_grid(string_input)

def in_grid(grid, y, x):
    return y >= 0 and x >= 0 and y < len(grid) and x < len(grid[y])

def get_possible_words(grid, words, prefix_set, current, y, x, used):
    found = []
    if current not in prefix_set:
        return found
    if current in words:
        found.append(current)
    for dy, dx in NEIGHBORS:
        ny, nx = y + dy, x + dx
        if in_grid(grid, ny, nx) and (ny, nx) not in used:
            used.add((ny, nx))
            found.extend(get_possible_words(grid, words, prefix_set, current+grid[ny][nx], ny, nx, used))
            used.remove((ny, nx))
    return list(set(found))


# Example usage:
string_input = args.letters
sorted_array = sorted(solve(grid), key=len, reverse=True)
print(sorted_array)
