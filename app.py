# My tic-tac-toe game
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# My game board
game_board = [None, None, None, None, None, None, None, None, None]
current_player = "X"

@app.route('/')
def index():
    return render_template('index.html')

def check_winner():
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns  
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for combo in winning_combinations:
        if (game_board[combo[0]] == game_board[combo[1]] == game_board[combo[2]] and 
            game_board[combo[0]] is not None):
            return game_board[combo[0]]
    
    return None

def is_board_full():
    return None not in game_board

@app.route('/make_move', methods=['POST'])
def make_move():
    global current_player
    
    position = int(request.json['position'])
    
    if game_board[position] is not None:
        return jsonify({'error': 'Position already taken'})
    
    game_board[position] = current_player
    winner = check_winner()
    tie = is_board_full() and winner is None
    
    # switch players
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"
    
    return jsonify({
        'board': game_board,
        'current_player': current_player,
        'winner': winner,
        'tie': tie
    })

@app.route('/reset', methods=['POST'])
def reset_game():
    global game_board, current_player
    
    game_board = [None, None, None, None, None, None, None, None, None]
    current_player = "X"
    
    return jsonify({
        'board': game_board,
        'current_player': current_player,
        'winner': None,
        'tie': False
    })

@app.route('/game_state', methods=['GET'])
def get_game_state():
    return jsonify({
        'board': game_board,
        'current_player': current_player,
        'winner': check_winner(),
        'tie': is_board_full() and check_winner() is None
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080) 