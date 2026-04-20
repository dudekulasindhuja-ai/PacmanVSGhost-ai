# ai.py

def evaluate(game, pacman, ghost):
    # Manhattan distance
    distance = abs(pacman[0] - ghost[0]) + abs(pacman[1] - ghost[1])

    # Mobility (number of moves)
    ghost_moves = len(game.get_moves(ghost))
    pacman_moves = len(game.get_moves(pacman))

    # Goal awareness
    goal_dist = abs(pacman[0] - game.goal[0]) + abs(pacman[1] - game.goal[1])

    # Final score
    return -distance + 2 * ghost_moves - pacman_moves + goal_dist


def minimax(game, pacman, ghost, depth, alpha, beta, maximizing):

    # 🔹 Terminal conditions
    if pacman == ghost:
        return 100   # ghost wins

    if pacman == game.goal:
        return -100  # pacman wins

    if depth == 0:
        return evaluate(game, pacman, ghost)

    # 🔹 Ghost (MAX player)
    if maximizing:
        max_eval = -float('inf')

        for move in game.get_moves(ghost):
            eval = minimax(game, pacman, move, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)

            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Alpha-Beta pruning

        return max_eval

    # 🔹 Pacman (MIN player)
    else:
        min_eval = float('inf')

        for move in game.get_moves(pacman):
            eval = minimax(game, move, ghost, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)

            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha-Beta pruning

        return min_eval


def best_move(game, pacman, ghost, depth):
    best_score = -float('inf')
    best_move_choice = ghost

    for move in game.get_moves(ghost):
        score = minimax(game, pacman, move, depth - 1, -float('inf'), float('inf'), False)

        if score > best_score:
            best_score = score
            best_move_choice = move

    return best_move_choice