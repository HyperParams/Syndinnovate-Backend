import classes
import heapq
import flask
import pickle
import requests

with open("resources/queue1.bat","rb") as file:
    queue1 = pickle.load(file)

with open("resources/weights.bat","rb") as file:
    weights = pickle.load(file)
    # TODO: detect for changes in weights

app = flask.Flask(__name__)

@app.route('/')
def landing():
    return flask.Response(), 200

@app.route('/add/', methods=["GET", "POST"])
def add():
    mobile_number = flask.request.args.get('mobile-number')
    POV = flask.request.args.get('POV')
    heapq.heappush(queue1, customer(mobile_number, POV, weights))
    return flask.Response(), 200

@app.route('/counter-1/empty/', methods=["GET", "POST"]) # TODO: check if multiple slashes work for app route in flask
def empty1():
    c = queue1.heappop()
    r = requests.post(url="<URL>/counter-1/next/",data=vars(c))
    # TODO: send sms to customer

#just test
