from typing import Callable

from adversarialsearchproblem import (
    Action,
    AdversarialSearchProblem,
    State as GameState,
)


def max_helper(state, asp:AdversarialSearchProblem, player) -> int:
    if asp.is_terminal_state(state):
       return asp.evaluate_terminal(state)
    
    maxEval:int = -9999
    move_2 = 0
    move = 1
    for action in asp.get_available_actions(state):
        new_state = asp.transition(state, action)
        new_player = new_state.player_to_move()

        new_eval, move_2 = min_helper(new_state, asp, new_player)

        if new_eval > maxEval:
            maxEval = new_eval
            move = action
    
    return maxEval, move

def min_helper(state, asp:AdversarialSearchProblem, player) -> int:
    if asp.is_terminal_state(state):
       return asp.evaluate_terminal(state)
     
    minEval:int = +9999
    move_2 = 0
    move = 1
    for action in asp.get_available_actions(state):
        new_state = asp.transition(state, action)
        new_player = new_state.player_to_move()

        new_eval, move_2 = max_helper(new_state, asp, new_player)

        if new_eval < minEval:
            minEval = new_eval
            move = action
        
    return minEval, move


def max_helper_alpha(state, asp:AdversarialSearchProblem, player, alpha, beta) -> int:
    if asp.is_terminal_state(state):
       return asp.evaluate_terminal(state)
    
    maxEval:int = -9999
    move_2 = 0
    move = 1
    for action in asp.get_available_actions(state):
        new_state = asp.transition(state, action)
        new_player = new_state.player_to_move()

        new_eval, move_2 = min_helper_beta(new_state, asp, new_player, alpha, beta)

        if new_eval > maxEval:
            maxEval = new_eval
            move = action
        
        alpha = max(alpha, new_eval)
        if beta<=alpha:
            break
    
    return maxEval, move

    

def min_helper_beta(state, asp:AdversarialSearchProblem, player, alpha, beta) -> int:
    if asp.is_terminal_state(state):
       return asp.evaluate_terminal(state)
     
    minEval:int = +9999
    move_2 = 0
    move = 1
    for action in asp.get_available_actions(state):
        new_state = asp.transition(state, action)
        new_player = new_state.player_to_move()

        new_eval, move_2 = max_helper_alpha(new_state, asp, new_player, alpha, beta)

        if new_eval < minEval:
            minEval = new_eval
            move = action

        beta = min(beta, new_eval)
        if beta<=alpha:
            break
        
    return minEval, move
    
def max_helper_alpha_cutoff(state, asp:AdversarialSearchProblem, player, alpha, beta, depth, heuristic_func) -> int:
    if asp.is_terminal_state(state):
        return asp.evaluate_terminal(state)[player], 0
    
    if depth == 0:
       return heuristic_func(state), 0

    maxEval:int = -9999
    move_2 = 0
    move = None
    for action in asp.get_available_actions(state):
        new_state = asp.transition(state, action)

        new_eval, move_2 = min_helper_beta_cutoff(new_state, asp, player, alpha, beta, (depth-1),heuristic_func)   
        
        if new_eval > maxEval:
            maxEval = new_eval
            move = action
        
        alpha = max(alpha, new_eval)
        if beta<=alpha:
            break
        
        """
        if new_eval > maxEval:
            maxEval = new_eval
            move = action
            alpha = max(alpha, maxEval)
        if maxEval >= beta:
            break
        """    
    return maxEval, move

    

def min_helper_beta_cutoff(state, asp:AdversarialSearchProblem, player, alpha, beta, depth, heuristic_func) -> int:
    if asp.is_terminal_state(state):
        return asp.evaluate_terminal(state)[player], 0
    
    if depth == 0:
       return heuristic_func(state), 0
     
    minEval:int = +9999
    move_2 = 0
    move = None
    for action in asp.get_available_actions(state):
        new_state = asp.transition(state, action)

        new_eval, move_2 = max_helper_alpha_cutoff(new_state, asp, player, alpha, beta, (depth-1), heuristic_func)

        if new_eval < minEval:
            minEval = new_eval
            move = action

        beta = min(beta, new_eval)
        if beta<=alpha:
            break
        """
        if new_eval < minEval:
            minEval = new_eval
            move = action
            beta = min(beta, minEval)
        if minEval <= alpha:
            break
        """
    return minEval, move

def minimax(asp: AdversarialSearchProblem[GameState, Action]) -> Action:
    """
    Implement the minimax algorithm on ASPs, assuming that the given game is
    both 2-player and constant-sum.

    Input:
        asp - an AdversarialSearchProblem
    Output:
        an action (an element of asp.get_available_actions(asp.get_start_state()))
    """
    state = asp.get_start_state()
    minEval = +9999
    maxEval = -9999

    player = state.player_to_move()

    if asp.is_terminal_state(state):
        return asp.evaluate_terminal(state)

    if player == 0: #maximising player
        new_eval, move = max_helper(state, asp, player)
        maxEval = max(maxEval, new_eval)
        return move
    else: #minimising player
        new_eval, move = min_helper(state, asp, player)
        minEval= min(minEval, new_eval)
        return move

def alpha_beta(asp: AdversarialSearchProblem[GameState, Action]) -> Action:
    """
    Implement the alpha-beta pruning algorithm on ASPs,
    assuming that the given game is both 2-player and constant-sum.

    Input:
        asp - an AdversarialSearchProblem
    Output:
        an action(an element of asp.get_available_actions(asp.get_start_state()))
    """
    state = asp.get_start_state()
    minEval = +9999
    maxEval = -9999
    alpha = -9999
    beta = +9999

    player = state.player_to_move()

    if asp.is_terminal_state(state):
        return asp.evaluate_terminal(state)

    if player == 0: #maximising player
        new_eval, move = max_helper_alpha(state, asp, player, alpha, beta)
        maxEval = max(maxEval, new_eval)
        return move
    else: #minimising player
        new_eval, move = min_helper_beta(state, asp, player, alpha, beta)
        minEval= min(minEval, new_eval)
        return move


    ...


def alpha_beta_cutoff(
    asp: AdversarialSearchProblem[GameState, Action],
    cutoff_ply: int,
    # See AdversarialSearchProblem:heuristic_func
    heuristic_func: Callable[[GameState], float],
) -> Action:
    """
    This function should:
    - search through the asp using alpha-beta pruning
    - cut off the search after cutoff_ply moves have been made.

    Input:
        asp - an AdversarialSearchProblem
        cutoff_ply - an Integer that determines when to cutoff the search and
            use heuristic_func. For example, when cutoff_ply = 1, use
            heuristic_func to evaluate states that result from your first move.
            When cutoff_ply = 2, use heuristic_func to evaluate states that
            result from your opponent's first move. When cutoff_ply = 3 use
            heuristic_func to evaluate the states that result from your second
            move. You may assume that cutoff_ply > 0.
        heuristic_func - a function that takes in a GameState and outputs a
            real number indicating how good that state is for the player who is
            using alpha_beta_cutoff to choose their action. You do not need to
            implement this function, as it should be provided by whomever is
            calling alpha_beta_cutoff, however you are welcome to write
            evaluation functions to test your implemention. The heuristic_func
            we provide does not handle terminal states, so evaluate terminal
            states the same way you evaluated them in the previous algorithms.
    Output:
        an action(an element of asp.get_available_actions(asp.get_start_state()))
    """
    state = asp.get_start_state()
    minEval = +9999
    maxEval = -9999
    alpha = -9999
    beta = +9999

    player = state.player_to_move()

    if asp.is_terminal_state(state):
        return heuristic_func(state)

    if player == 0: #maximising player
        new_eval, move = max_helper_alpha_cutoff(state, asp, player, alpha, beta, cutoff_ply, heuristic_func)
        maxEval = max(maxEval, new_eval)
        return move
    else: #minimising player
        new_eval, move = min_helper_beta_cutoff(state, asp, player, alpha, beta, cutoff_ply,heuristic_func)
        minEval= min(minEval, new_eval)
        return move


    ...
