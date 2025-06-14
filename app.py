# Simple Tic-Tac-Toe Game - Educational Version
# This is a basic web-based tic-tac-toe game using Flask

from flask import Flask, render_template, request, jsonify

# Create our Flask app - this is the main application
app = Flask(__name__)

# This is our game board - a list of 9 empty spaces
# We use None to represent empty spaces
# Index 0 = top-left, 1 = top-middle, 2 = top-right
# Index 3 = middle-left, 4 = center, 5 = middle-right  
# Index 6 = bottom-left, 7 = bottom-middle, 8 = bottom-right
game_board = [None, None, None, None, None, None, None, None, None]
current_player = "X"  # X always goes first (Chrome)

# Main page route - this shows our game
@app.route('/')
def index():
    return render_template('index.html')

# This function checks if someone won the game
def check_winner():
    # All possible winning combinations (rows, columns, diagonals)
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    # Check each winning combination
    for combo in winning_combinations:
        if (game_board[combo[0]] == game_board[combo[1]] == game_board[combo[2]] and 
            game_board[combo[0]] is not None):
            return game_board[combo[0]]  # Return the winner (X or O)
    
    return None  # No winner yet

# This function checks if the board is full (tie game)
def is_board_full():
    return None not in game_board

# Handle player moves
@app.route('/make_move', methods=['POST'])
def make_move():
    global current_player
    
    # Get the position where the player clicked (0-8)
    position = int(request.json['position'])
    
    # Check if the position is already taken
    if game_board[position] is not None:
        return jsonify({'error': 'Position already taken'})
    
    # Place the current player's mark on the board
    game_board[position] = current_player
    
    # Check if current player won
    winner = check_winner()
    
    # Check if it's a tie
    tie = is_board_full() and winner is None
    
    # Switch to the other player for next turn
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"
    
    # Send back the game state
    return jsonify({
        'board': game_board,
        'current_player': current_player,
        'winner': winner,
        'tie': tie
    })

# Reset the game
@app.route('/reset', methods=['POST'])
def reset_game():
    global game_board, current_player
    
    # Clear the board and reset to X's turn
    game_board = [None, None, None, None, None, None, None, None, None]
    current_player = "X"
    
    return jsonify({
        'board': game_board,
        'current_player': current_player,
        'winner': None,
        'tie': False
    })

# Get current game state
@app.route('/game_state', methods=['GET'])
def get_game_state():
    return jsonify({
        'board': game_board,
        'current_player': current_player,
        'winner': check_winner(),
        'tie': is_board_full() and check_winner() is None
    })

# Run the app - this starts our web server
if __name__ == '__main__':
    app.run(debug=True, port=8080) 