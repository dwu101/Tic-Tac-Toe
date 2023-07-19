import sys
sys.path.insert(0, 'c:\python310\lib\site-packages')
from flask.views import MethodView 
from flask import Flask, request, jsonify, redirect, url_for, json, render_template
from flask_caching import Cache
import requests 
import time
import numpy as np
import pickle
import requests
import time
import jinja2
# import game


app = Flask(__name__,template_folder='templates')
app.jinja_loader = jinja2.FileSystemLoader('templates')


config = {
    "DEBUG": True,         
    "CACHE_TYPE": "simple",  
}
app.config.from_mapping(config)

cache = Cache(app)

cache.set('row', None)
cache.set('col', None) 
cache.set('rowToFrontend', None)
cache.set('colToFrontend', None)


@app.route('/')
def hello():
   
#    return "<p>hi</p>"

    BOARD_ROWS = 3
    BOARD_COLS = 3


    class State:
        def __init__(self, p1, p2):
            self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
            self.p1 = p1
            self.p2 = p2
            self.isEnd = False
            self.boardHash = None
            # init p1 plays first
            self.playerSymbol = 1

        # get unique hash of current board state
        def getHash(self):
            self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
            return self.boardHash

        def winner(self):
            # row
            for i in range(BOARD_ROWS):
                if sum(self.board[i, :]) == 3:
                    self.isEnd = True
                    return 1
                if sum(self.board[i, :]) == -3:
                    self.isEnd = True
                    return -1
            # col
            for i in range(BOARD_COLS):
                if sum(self.board[:, i]) == 3:
                    self.isEnd = True
                    return 1
                if sum(self.board[:, i]) == -3:
                    self.isEnd = True
                    return -1
            # diagonal
            diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
            diag_sum2 = sum([self.board[i, BOARD_COLS - i - 1] for i in range(BOARD_COLS)])
            diag_sum = max(abs(diag_sum1), abs(diag_sum2))
            if diag_sum == 3:
                self.isEnd = True
                if diag_sum1 == 3 or diag_sum2 == 3:
                    return 1
                else:
                    return -1

            # tie
            # no available positions
            if len(self.availablePositions()) == 0:
                self.isEnd = True
                return 0
            # not end
            self.isEnd = False
            return None

        def availablePositions(self):
            positions = []
            for i in range(BOARD_ROWS):
                for j in range(BOARD_COLS):
                    if self.board[i, j] == 0:
                        positions.append((i, j))  # need to be tuple
            return positions

        def updateState(self, position):
            self.board[position] = self.playerSymbol
            # switch to another player
            self.playerSymbol = -1 if self.playerSymbol == 1 else 1

        # only when game ends
        def giveReward(self):
            result = self.winner()
            # backpropagate reward
            if result == 1:
                self.p1.feedReward(1)
                self.p2.feedReward(0)
            elif result == -1:
                self.p1.feedReward(0)
                self.p2.feedReward(1)
            else:
                self.p1.feedReward(0.1)
                self.p2.feedReward(0.5)

        # board reset
        def reset(self):
            self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
            self.boardHash = None
            self.isEnd = False
            self.playerSymbol = 1

        def play(self, rounds=100):
            for i in range(rounds):
                if i % 1000 == 0:
                    print("Rounds {}".format(i))
                while not self.isEnd:
                    # Player 1
                    positions = self.availablePositions()
                    p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                    # take action and upate board state
                    self.updateState(p1_action)
                    board_hash = self.getHash()
                    self.p1.addState(board_hash)
                    # check board status if it is end

                    win = self.winner()
                    if win is not None:
                        # self.showBoard()
                        # ended with p1 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

                    else:
                        
                        # Player 2
                        positions = self.availablePositions()
                        p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                        self.updateState(p2_action)
                        board_hash = self.getHash()
                        self.p2.addState(board_hash)

                        win = self.winner()
                        if win is not None:
                            # self.showBoard()
                            # ended with p2 either win or draw
                            self.giveReward()
                            self.p1.reset()
                            self.p2.reset()
                            self.reset()
                            break

        # play with human
        def play2(self):
            turns = 0
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)

                body = {
                    "rowToFrontend": p1_action[0],
                    "colToFrontend": p1_action[1],
                }
                headers = {
                    'Content-Type' : 'application/json'
                }
                print(body)
                # if turns ==0:
                #     cache.set('rowToFrontend', None)
                #     cache.set('colToFrontend', None)
                # else:
                cache.set('rowToFrontend', p1_action[0])
                cache.set('colToFrontend', p1_action[1]) #response is 1 behind
                turns +=1
                # response = requests.post("http://127.0.0.1:5000/postToFrontend", data=body, headers=headers)
                # print(response.status_code)
                

                # take action and upate board state
                self.updateState(p1_action)
                self.showBoard()
                # check board status if it is end
                win = self.winner()
                if win is not None:
                    copy_name = self.p1.name
                    self.reset()
                    if win == 1:
                        return jsonify({'winner': copy_name})
                        # print(self.p1.name, "wins!")
                    else:
                        
                        return jsonify({'winner': 'tie'})
                        # print("tie!")
                    
                

                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions)

                    self.updateState(p2_action)
                    self.showBoard()
                    win = self.winner()
                    if win is not None:
                        copy_name = self.p2.name
                        self.reset()
                        if win == 1:
                            return jsonify({'winner': copy_name})
                            # print(self.p2.name, "wins!")
                        else:
                            
                            return jsonify({'winner': 'tie'})
                            # print("tie!")

        def showBoard(self):
            # p1: x  p2: o
            for i in range(0, BOARD_ROWS):
                print('-------------')
                out = '| '
                for j in range(0, BOARD_COLS):
                    if self.board[i, j] == 1:
                        token = 'x'
                    if self.board[i, j] == -1:
                        token = 'o'
                    if self.board[i, j] == 0:
                        token = ' '
                    out += token + ' | '
                print(out)
            print('-------------')


    class Player:
        def __init__(self, name, exp_rate=0.3):
            self.name = name
            self.states = []  # record all positions taken
            self.lr = 0.2
            self.exp_rate = exp_rate
            self.decay_gamma = 0.9
            self.states_value = {}  # state -> value

        def getHash(self, board):
            boardHash = str(board.reshape(BOARD_COLS * BOARD_ROWS))
            return boardHash

        def chooseAction(self, positions, current_board, symbol):
            if np.random.uniform(0, 1) <= self.exp_rate:
                # take random action
                idx = np.random.choice(len(positions))
                action = positions[idx]
            else:
                value_max = -999
                for p in positions:
                    next_board = current_board.copy()
                    next_board[p] = symbol
                    next_boardHash = self.getHash(next_board)
                    value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                    # print("value", value)
                    if value >= value_max:
                        value_max = value
                        action = p
            # print("{} takes action {}".format(self.name, action))
            # print("ASDNOEGNWOIEG0:", action) #row, col
            return action

        # append a hash state
        def addState(self, state):
            self.states.append(state)

        # at the end of game, backpropagate and update states value
        def feedReward(self, reward):
            for st in reversed(self.states):
                if self.states_value.get(st) is None:
                    self.states_value[st] = 0
                self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
                reward = self.states_value[st]

        def reset(self):
            self.states = []

        def savePolicy(self):
            fw = open('policy_' + str(self.name), 'wb')
            pickle.dump(self.states_value, fw)
            fw.close()

        def loadPolicy(self, file):
            fr = open(file, 'rb')
            self.states_value = pickle.load(fr)
            fr.close()


    class HumanPlayer:
        def __init__(self, name):
            self.name = name

        def chooseAction(self, positions):
            while True:
                # print("x")
                response = requests.get("http://127.0.0.1:5000/get").json()
                # print(response['row'])

                while response['row'] == None:
                    print("waiting...")
                    response = requests.get("http://127.0.0.1:5000/get").json()
                    time.sleep(0.5)
                    
                row = response['row']
                col = response['col']
                action = (row, col)
                if action in positions:
                    return action

        # append a hash state
        def addState(self, state):
            pass

        # at the end of game, backpropagate and update states value
        def feedReward(self, reward):
            pass

        def reset(self):
            pass


    
    p1 = Player("p1")
    p2 = Player("p2")

    p1 = Player("computer", exp_rate=0)
    p1.loadPolicy("policy_p1")

    p2 = HumanPlayer("human")

    st = State(p1, p2)
    ret = st.play2().get_json()
    return render_template(r"index.html", title=ret)

    



@app.route('/post', methods=['POST'])
def post():
    print("x")
    req = request.get_json()
    print(req)
    cache.set('row', req['row'])
    cache.set('col', req['col'])

    time.sleep(1)
    
    copy = {
        'rowToFrontend' : cache.get('rowToFrontend'), 
        'colToFrontend' : cache.get('colToFrontend'),
    }
    
    cache.set('rowToFrontend', None)
    cache.set('colToFrontend', None) 
    print("POOP")

    return jsonify(copy)

    


@app.route('/get', methods=['GET'])
def get():
    copy = {
        'row' : cache.get('row'), 
        'col' : cache.get('col'),
    }
    
    cache.set('row', None)
    cache.set('col', None) 
    
    return jsonify(copy)


# @app.route('/postToFrontend', methods=['POST']) #computer moves get sent here which then get sent to the frontend through getToFrontend. POSTMAN is simulating this 
# def postToFrontend():

#     req = request.get_json()
#     cache.set('rowToFrontend', req['rowToFrontend'])
#     cache.set('colToFrontend', req['colToFrontend'])

#     print(cache.get('row'))
#     return jsonify({
#         'rowToFrontend' : cache.get('rowToFrontend'),
#         'colToFrontend' : cache.get('colToFrontend'),
#     })


# @app.route('/getToFrontend', methods=['GET'])
# def getToFrontend():

#     copy = {
#         'rowToFrontend' : cache.get('rowToFrontend'), 
#         'colToFrontend' : cache.get('colToFrontend'),
#     }
    
#     cache.set('rowToFrontend', None)
#     cache.set('colToFrontend', None) 

#     return jsonify(copy)




# class ListView(MethodView):

#     def __init__(self):
#         print(exec(open('test.py').read()))

#     def post(self):

#         req = request.get_json()
#         cache.set('row', req['row'])
#         cache.set('col', req['col'])

#         return jsonify({
#             'row' : cache.get('row'),
#             'col' : cache.get('col'),
#         })
    
#     def get(self):
#         copy = {
#             'row' : cache.get('row'), 
#             'col' : cache.get('col'),
#         }
       
#         cache.set('row', None)
#         cache.set('col', None)  
  
#         return jsonify(copy)
    

# app.add_url_rule('/handleData', view_func=ListView.as_view('handleData'),)
