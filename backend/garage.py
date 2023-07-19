from flask import Flask, redirect, url_for,request,jsonify,json
# from flask_classful import FlaskView, route

 

app = Flask(__name__)


@app.route('/')
def hello():
    print(redirect(url_for('test')))
    return "<p>Hi</p>"


@app.route('/test', methods=['POST', 'GET'])
def test():
    # default = {'poop': 2}

    if request.method == 'POST':
        default = request.get_json()
        
        return jsonify({'Done' : 201})
    
    else:
        # print(default)
        try:
            copy = default 
            del default
            return copy 
        except:
            return {'poop':2}

#===============================================================



# @app.route('/')
# def hello():
    
#     var = redirect(url_for('get')) #input game.py here. figure out how to call a route from a route 
#     print(var.get_json())
#     return "<p>hi</p>"


# @app.route('/post', methods=['POST'])
# def post():
    
#     req = request.get_json()
#     cache.set('row', req['row'])
#     cache.set('col', req['col'])

#     return jsonify({
#         'row' : cache.get('row'),
#         'col' : cache.get('col'),
#     })


# @app.route('/get', methods=['GET'])
# def get():
#     copy = {
#         'row' : cache.get('row'), 
#         'col' : cache.get('col'),
#     }
    
#     cache.set('row', None)
#     cache.set('col', None)  

#     return jsonify(copy)

#==================================================