import os
import heapq
import flask
import pickle
import random
import classes
import requests
import psycopg2
from twilio.rest import Client

re_entry_threshold=3

# initializing sms api-twilio
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
client = Client(account_sid, auth_token)

# initializing lines
with open("resources/line1.dat","rb") as file:
    line1 = classes.line()
    try:
        line1 = pickle.load(file)
    except EOFError:
        line1 = []

with open("resources/line2.dat","rb") as file:
    line2 = classes.line()
    try:
        line2 = pickle.load(file)
    except EOFError:
        line2 = []

with open("resources/line3.dat","rb") as file:
    line3 = classes.line()
    try:
        line3 = pickle.load(file)
    except EOFError:
        line3 = []

line_assignment = {
        1:line1,
        2:line1,
        3:line1,
        4:line1,
        5:line2,
        6:line2,
        7:line2,
        8:line2,
        9:line3,
        10:line3,
        11:line3,
        12:line3
}

otps = {}

with open("resources/weights.dat","rb") as file:
    weights = pickle.load(file)

occupied_customers = []

app = flask.Flask(__name__)

@app.route('/')
def landing():
    return flask.Response(), 200

@app.route('/add/', methods=["GET", "POST"])
def add():
    mobile_number = flask.request.args.get('mobile-number')
    POV = flask.request.args.get('POV')
    otp = flask.request.args.get('OTP')
    if otp!=otps["mobile_number"]:
        return flask.jsonify({'verified':False}), 200
    else:
        c = customer(mobile_number, POV, weights)
        line_assignment[POV].add_customer(c)
        c.alert_customer("We have reserved your spot in the line. \n-Team Syndicate Bank")
        return flask.jsonify({'verified':True}), 200

@app.route('/verify/', methods=["GET", "POST"])
def verify():
    mobile_number = flask.request.args.get('mobile-number')
    otps[mobile_number] = random.randint(100000, 999999)
    return flask.Response(), 200

# TODO: enter value for <URL>
# ================================================================================|COUNTER-1|=============================================================================================================

@app.route('/counter-1/empty/', methods=["GET", "POST"])
def empty1():
    for i in range(len(occupied_customers)):
        if occupied_customers[i][1] == 1:
            del occupied_customers[i]
            break
    c = line1.get_next_customer()
    occupied_customers.append((c, 1))
    r = requests.post(url="<URL>/counter-1/next/", data=vars(c))
    c.alert_customer("Please reach counter 1")
    return flask.Response(), 200

@app.route('/counter-1/customer-not-there/', methods=["GET", "POST"])
def cusomer_didnt_show_up1():
    id = flask.request.args.get('ID')
    for i in range(len(occupied_customers)):
        if occupied_customers[i][0].ID == id:
            c = (occupied_customers.pop(i))[0]
            break
    if c.re_entries > re_entry_threshold:
        del c
    else:
        c.re_entries+=1
        line1.add_customer(c)
    empty1()

# ================================================================================|COUNTER-2|=============================================================================================================

@app.route('/counter-2/empty/', methods=["GET", "POST"])
def empty2():
    for i in range(len(occupied_customers)):
        if occupied_customers[i][1] == 2:
            del occupied_customers[i]
            break
    c = line2.get_next_customer()
    occupied_customers.append((c, 2))
    r = requests.post(url="<URL>/counter-2/next/",data=vars(c))
    c.alert_customer("Please reach counter 2")
    return flask.Response(), 200

@app.route('/counter-2/customer-not-there/', methods=["GET", "POST"])
def cusomer_didnt_show_up2():
    id = flask.request.args.get('ID')
    for i in range(len(occupied_customers)):
        if occupied_customers[i][0].ID == id:
            c = (occupied_customers.pop(i))[0]
            break
    if c.re_entries > re_entry_threshold:
        del c
    else:
        c.re_entries+=1
        line2.add_customer(c)
    empty2()

# ================================================================================|COUNTER-3|=============================================================================================================

@app.route('/counter-3/empty/', methods=["GET", "POST"])
def empty3():
    for i in range(len(occupied_customers)):
        if occupied_customers[i][1] == 3:
            del occupied_customers[i]
            break
    c = line3.get_next_customer()
    occupied_customers.append((c, 3))
    r = requests.post(url="<URL>/counter-3/next/",data=vars(c))
    c.alert_customer("Please reach counter 3")
    return flask.Response(), 200

@app.route('/counter-3/customer-not-there/', methods=["GET", "POST"])
def cusomer_didnt_show_up3():
    id = flask.request.args.get('ID')
    for i in range(len(occupied_customers)):
        if occupied_customers[i][0].ID == id:
            c = (occupied_customers.pop(i))[0]
            break
    if c.re_entries > re_entry_threshold:
        del c
    else:
        c.re_entries+=1
        line3.add_customer(c)
    empty3()

# ================================================================================|COUNTER-4|=============================================================================================================

@app.route('/counter-4/empty/', methods=["GET", "POST"])
def empty4():
    for i in range(len(occupied_customers)):
        if occupied_customers[i][1] == 4:
            del occupied_customers[i]
            break
    c = line1.get_next_customer()
    occupied_customers.append((c, 4))
    r = requests.post(url="<URL>/counter-4/next/",data=vars(c))
    c.alert_customer("Please reach counter 4")
    return flask.Response(), 200

@app.route('/counter-4/customer-not-there/', methods=["GET", "POST"])
def cusomer_didnt_show_up4():
    id = flask.request.args.get('ID')
    for i in range(len(occupied_customers)):
        if occupied_customers[i][0].ID == id:
            c = (occupied_customers.pop(i))[0]
            break
    if c.re_entries > re_entry_threshold:
        del c
    else:
        c.re_entries+=1
        line1.add_customer(c)
    empty4()

@app.route('/customer-served/', methods=["GET", "POST"])
def customer_served():
    # TODO: enter data into customer table according to the need of data analytics
    pass
