# Sprites for my game. All had to be made by hand because I wanted the cool scrolling effect.

player_cursor = [[2, 2], [0, 2], [1, 2], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, 2], [4, 2]]

warning_zombie = [[5, 5], # Center px
                  [5, 0], 
                  [4, 1], [6, 1], [4, 2], [6, 2], #Triangle sides
                  [3, 3], [7, 3], [3, 4], [7, 4],
                  [2, 5], [8, 5], [2, 6], [8, 6],
                  [1, 7], [9, 7], [1, 8], [9, 8],
                  [0, 9], [10, 9],
                  [1, 10], [2, 10], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10], # Triangle base
                  [5, 4], [5, 5], [5, 6], [5, 8]] # Exclamation point 

error_brute = [[5, 5], # Center px
               [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], # Top side
               [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], # Left side
               [10, 1], [10, 2], [10, 3], [10, 4], [10, 5], [10, 6], [10, 7], [10, 8], [10, 9], # Right side
               [0, 10], [1, 10], [2, 10], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10], [10, 10], # Bottom side
               [2, 2], [3, 3], [4, 4], [6, 6], [7, 7], [8, 8], # NW -> SE diagonal
               [8, 2], [7, 3], [6, 4], [4, 6], [3, 7], [2, 8]  # NE -> SW diagonal
                ]

projectile_check = [[2, 2], [0, 2], [1, 3], [3, 1], [4, 0]] # Projectile that player shoots


