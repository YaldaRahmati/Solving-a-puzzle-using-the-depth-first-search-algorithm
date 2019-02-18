import numpy as np

# Define the shape of the pieces

P1= np.ones((2, 1), dtype=np.int)
P2= np.ones((5, 1), dtype=np.int)

P3= np.ones((3, 4), dtype=np.int)
P3[0,0]= 0
P3[2,0]= 0
P3[0,3]= 0
P3[1,3]= 0

P4= np.ones((3, 3), dtype=np.int)
P4[0,2]= 0
P4[1,0]= 0
P4[2,0]= 0
P4[2,1]= 0

P5= np.ones((3, 3), dtype=np.int)
P5[0,2]= 0
P5[2,2]= 0

P6= np.ones((4, 2), dtype=np.int)
P6[0,0]= 0
P6[3,0]= 0

P7= np.ones((3, 3), dtype=np.int)
P7[0,1]= 0
P7[0,2]= 0
P7[1,2]= 0

P8= np.ones((2, 3), dtype=np.int)
P8[0,0]= 0
P8[0,2]= 0

P9= np.ones((2, 4), dtype=np.int)
P9[1,0]= 0
P9[1,1]= 0
P9[1,3]= 0


def valid_board(board, value):
    return (board < value).all()


def embed_piece(piece, x, y):                                                   # Returns a blank board with the "piece"
    board_with_piece = np.zeros((7, 7), dtype=np.int)                           # embedded at location x, y
    board_with_piece[x:x + piece.shape[0], y:y + piece.shape[1]] = piece
    return board_with_piece


def find_available_locations(board):
    k = 0
    avaliable_locations_list= []
    avaliable_locations_list.append([])
    for i in range(7):
        for j in range(7):
            if board[i, j] == 0:
                avaliable_locations_list[k].append(i)
                avaliable_locations_list[k].append(j)
                avaliable_locations_list.append([])
                k += 1
    return avaliable_locations_list


def depth_search(available_pieces, board, x, y, counter, row):
    count = 0
    while available_pieces is not None:
        P = available_pieces[count]
        if y + P.shape[1] < 8 and x + P.shape[0] < 8:                 # Create a new board by adding piece P
            new_board = board + embed_piece(P, x, y)                  # if it is inside the 7*7 block

            if valid_board(new_board, 2):                             # Piece P will be placed on the board if it
                                                                      # doesn't overlap with other existing pieces
                counter += 1
                Solution.append([])
                Solution[counter].append(P)                           # Update the solution list by adding piece P
                Solution[counter].append((x, y))

                board = new_board                                     # Update the board

                Locations = find_available_locations(board)           # Find next available location on the new board
                x, y = Locations[row][0], Locations[row][1]

                available_pieces.pop(count)                           # Remove P from the list of available pieces
                count = 0

                if available_pieces is None:
                    print ("A solution is found for this branch.")
                    print (Solution)
                    return

            else:
                if len(available_pieces) == count + 1:                 # If all of the pieces are tested at location x, y
                    count = 0                                          # Start testing form the first remaining piece

                    Locations = find_available_locations(board)        # Update the list of available locations
                    if row == len(Locations)-2:
                        print ("No solution for this branch!")
                    else:
                        row += 1
                        x, y = Locations[row][0], Locations[row][1]    # Move to the next available location if there is one
                else:
                    count += 1

        else:
            if len(available_pieces) == count + 1:                     # If all of the pieces are tested at location x, y
                count = 0                                              # Start testing form the first remaining piece

                Locations = find_available_locations(board)            # Update the list of available locations
                if row == len(Locations)-2:
                    print ("No solution for this branch!")
                    print ("Final board:")
                    print (board)
                    print ("Remaining pieces:")
                    print (available_pieces)
                    return
                else:
                    row += 1
                    x, y = Locations[row][0], Locations[row][1]        # Move to the next available location if there is one
            else:
                count += 1

    if available_pieces is None:
        Locations = find_available_locations(board)
        if len(Locations) < 2:
            print ("A solution is found for this branch.")
        elif len(Locations) >= 2:
            print ("All pieces are placed on the board, but there is more than one hole. "
                   "Thus, there's no solution for this branch.")

    return


# DEPTH-FIRST SEARCH (DFS):

p_num = 0

for first_piece in [P1, P2, P3, P4, P5, P6, P7, P8, P9]:
    print ("First piece of the present branch: ")
    print (first_piece)

    Solution = []
    Solution.append([])

    # Initials
    x = 0
    y = 0
    row = 0
    counter = 0

    board = np.zeros((7, 7), dtype=np.int)                     # Define the board

    available_pieces = [P1, P2, P3, P4, P5, P6, P7, P8, P9]    # Define the available puzzle pieces

    board = board + embed_piece(first_piece, x, y)             # Place the first piece on the board (initial branches of tree)

    if valid_board(board, 2):
        Solution[0].append(first_piece)
        Solution[0].append((x,y))

        Locations = find_available_locations(board)            # Find the list of available locations
        x, y = Locations[row][0], Locations[row][1]

        available_pieces.pop(p_num)                            # Remove the first piece form the list of available pieces

    depth_search(available_pieces, board, x, y, counter, row)  # Find solution for the this first piece (branch)

    p_num += 1




