from window import Window
from algorithms import a_star, dijkstras, depth_first_search, breadth_first_search, greedy_best_first_search, prims
import pygame


def start_visualizer():
    win = Window()
    grid = win.make_grid()
    start = None
    end = None

    running = True
    while running:
        win.draw(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Left click will place nodes
            if pygame.mouse.get_pressed(3)[0]:
                pos = pygame.mouse.get_pos()
                row, col = win.get_mouse_position(pos)

                # Clicking within the grid
                if 0 <= row <= 40 and 0 <= col <= 40:
                    node = grid[row][col]

                    # If there is no start node and you are not clicking on end node
                    if not start and node != end:
                        start = node
                        start.place_start()
                    
                    # If there is no end node and you are not clicking on start node
                    elif not end and node != start:
                        end = node
                        end.place_end()

                    # If start and end nodes are defined and you are not clicking on them
                    elif node != start and node != end:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_w] and not node.is_wall():
                            node.reset_color()
                            node.place_weight()
                        else:
                            if node.weight == 1:
                                node.place_wall()
                
                # Selecting Algorithms / Heuristic
                elif 625 <= pos[1] <= 655:
                    if 15 <= pos[0] <= 135:
                        win.selected_algorithm = "a_star"
                
                    elif 150 <= pos[0] <= 270:
                        win.selected_algorithm = "dijkstras"
                    
                    elif 285 <= pos[0] <= 405:
                        win.selected_algorithm = "depth_first_search"
                
                elif 660 <= pos[1] <= 690:
                    if 15 <= pos[0] <= 135:
                        win.selected_algorithm = "greedy_best_first_search"
                    
                    elif 150 <= pos[0] <= 270:
                        if win.speed == "Fast":
                            win.speed = "Medium"
                        elif win.speed == "Medium":
                            win.speed = "Slow"
                        else:
                            win.speed = "Fast"
                    
                    elif 285 <= pos[0] <= 405:
                        win.selected_algorithm = "breadth_first_search"
            
            # Right click will remove (reset) nodes
            elif pygame.mouse.get_pressed(3)[2]:
                row, col = win.get_mouse_position(pygame.mouse.get_pos())
                if 0 <= row <= 40 and 0 <= col <= 40:
                    node = grid[row][col]
                    if node == start:
                        start = None
                    elif node == end:
                        end = None
                    node.reset_color()
                    node.reset_weight()
            
            if event.type == pygame.KEYDOWN:

                # If start and end are defined and an algorithm is selected, run the algorithm
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            if node != start and node != end and not node.is_wall():
                                node.reset_color()

                            node.add_neighbours(grid)
                    
                    if win.selected_algorithm:
                        if win.selected_algorithm == "a_star":
                            a_star.algorithm(start, end, grid, lambda: win.draw(grid), win)
                        
                        elif win.selected_algorithm == "greedy_best_first_search":
                            greedy_best_first_search.algorithm(start, end, grid, lambda: win.draw(grid), win)
                        
                        elif win.selected_algorithm == "dijkstras":
                            dijkstras.algorithm(start, end, grid, lambda: win.draw(grid), win)

                        elif win.selected_algorithm == "depth_first_search":
                            depth_first_search.algorithm(start, end, lambda: win.draw(grid), win)
                        
                        elif win.selected_algorithm == "breadth_first_search":
                            breadth_first_search.algorithm(start, end, grid, lambda: win.draw(grid), win)
                
                # Clear the board
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    for row in grid:
                        for node in row:
                            node.reset_color()
                            node.reset_weight()
                
                # Generate a maze
                if event.key == pygame.K_g:
                    start, end, grid = prims.algorithm(grid, lambda: win.draw(grid), win)

    pygame.quit()


if __name__ == "__main__":
    start_visualizer()
