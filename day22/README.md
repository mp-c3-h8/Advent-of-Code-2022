# Advent of Code 2022 - Day 22

Problem: https://www.adventofcode.com/2022/day/22

## Part 1

- simulate the walk
- use complex numbers for the board, position and direction
- y-axis points downwards: all rotations are multiplied by -1
- wrap around the edge via modulo of the width/height of the bounding box
- create a teleport map to cross "bodies of water"

## Part 2

- cut out a cube net (handicraft)
- note down corresponding edges and changes in direction (arrows)
- translate change in direction to complex multiplication
    - i = left turn
    - -i = right turn
    - script uses y-axis pointing down, so all rotations are inverted
- create function to translate movement from one egde of a face to the corresponding face and edge
- since i didnt do proper 3d rotations, correction terms for every crossing had to be manually calculated
- there are eleven nets of a cube. this is not a general solution

### cube net for my input

                              -----------------------------------------------------
                              |            E            |            E            |
                              |            ►            |            ▲            |
                              |          (-i)           |           (1)           |
                              |                         |                         |
                              |                         |                         |
                              | D ► (-1)   A    (1) ► B | A ◄ (1)    B   (-1) ◄ C |
                              |                         |                         |
                              |                         |                         |
                              |           (1)           |          (-i)           |
                              |            ▼            |            ◄            |
                              |            F            |            F            |
                              -----------------------------------------------------
                              |            A            |
                              |            ▲            |
                              |           (1)           |
                              |                         |
                              |                         |
                              | D ▼ (i)    F    (i) ▲ B |
                              |                         |
                              |                         |
                              |           (1)           |
                              |            ▼            |
                              |            C            |
    -----------------------------------------------------
    |            F            |            F            |
    |            ►            |            ▲            |
    |          (-i)           |           (1)           |
    |                         |                         |
    |                         |                         |
    | A ► (-1)   D    (1) ► C | D ◄ (1)    C   (-1) ◄ B |
    |                         |                         |
    |                         |                         |
    |           (1)           |          (-i)           |
    |            ▼            |            ◄            |
    |            E            |            E            |
    -----------------------------------------------------
    |            D            |
    |            ▲            |
    |           (1)           |
    |                         |
    |                         |
    | A ▼ (i)    E    (i) ▲ C |
    |                         |
    |                         |
    |           (1)           |
    |            ▼            |
    |            B            |
    ---------------------------