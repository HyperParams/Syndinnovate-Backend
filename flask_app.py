import heapq
import flask
import pickle
import random
import classes
import requests
import psycopg2
import datetime
from twilio.rest import Client

re_entry_threshold=3

# initializing postgresql db
conn = psycopg2.connect("dbname=syndicatebank user=rachit password=12345678")
cur = conn.cursor()

# initializing sms api-twilio
account_sid = 'ACcd8d141a148b8146d9e3d4bcb4ebbee0'
auth_token = '1362785844e526c003c938465a9b7ecf'
client = Client(account_sid, auth_token)

# initializing lines
with open("resources/line1.dat","rb") as file:
    line1 = classes.line()
    try:
        line1 = pickle.load(file)
    except EOFError:
        line1 = classes.line()

with open("resources/line2.dat","rb") as file:
    line2 = classes.line()
    try:
        line2 = pickle.load(file)
    except EOFError:
        line2 = classes.line()

with open("resources/line3.dat","rb") as file:
    line3 = classes.line()
    try:
        line3 = pickle.load(file)
    except EOFError:
        line3 = classes.line()

line_assignment = {
'0':line1,
        '1':line1,
        '2':line1,
        '3':line1,
        '4':line1,
        '5':line2,
        '6':line2,
        '7':line2,
        '8':line2,
        '9':line3,
        '10':line3,
        '11':line3,
        '12':line3
}

otps = {}

try:
    with open("resources/weights.bat","rb") as file:
        weights = pickle.load(file)
except FileNotFoundError:
    weights = {'time':1,
                'D_score':1,
                'is_specially_abled':1,
                'POV':1
    }
if weights == None:
    weights = {'time':1,
                'D_score':1,
                'is_specially_abled':1,
                'POV':1
    }
occupied_customers = []
customers_not_reviewed = []

app = flask.Flask(__name__)

@app.route('/')
def landing():
    return flask.Response(), 200

@app.route('/add/', methods=["GET", "POST"])
def add():
    mobile_number = flask.request.args.get('mobile-number')
    POV = flask.request.args.get('POV')
    otp = flask.request.args.get('OTP')
    if otp!=otps[mobile_number]:
        print(otp, otps[mobile_number])
        return flask.jsonify({'verified':False}), 200
    else:
        # print(mobile_number)
        c = classes.customer(mobile_number, POV, weights)
        line_assignment[POV].add_customer(c)
        c.alert_customer("We have reserved your spot in the line. \n-Team Syndicate Bank")
        response = flask.jsonify({'verified':True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200

@app.route('/verify/', methods=["GET", "POST"])
def verify():
    mobile_number = flask.request.args.get('mobile-number')
    otps[mobile_number] = str(random.randint(100000, 999999))
    to_number = "+91"+str(mobile_number)
    message = client.messages.create(body=str(otps[mobile_number]), from_="+12015089104", to=to_number)
    print(message.sid, datetime.datetime.now())
    response = flask.jsonify({'ok':True})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

# TODO: enter value for https://5e339b7d.ngrok.io
# ================================================================================|COUNTER-1|=============================================================================================================

@app.route('/counter-1/empty/', methods=["GET", "POST"])
def empty1():
    for i in range(len(occupied_customers)):
        if occupied_customers[i][1] == 1:
            occupied_customers[i][0].end_service()
            occupied_customers[i][0].alert_customer("Please review your experience at <URL>!") # TODO: enter value for url
            del occupied_customers[i]
            break
    c = line1.get_next_customer()
    occupied_customers.append((c, 1))
    customers_not_reviewed.append(c)
    r = requests.post(url="https://5e339b7d.ngrok.io/counter-1/next/", data=vars(c))
    print(type(c))
    c.alert_customer("Please reach counter 1")
    c.end_waiting_time()
    c.start_counter_time()
    print(vars(c)) # DEBUGGING
    response = flask.jsonify(vars(c))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

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
    response = flask.jsonify(vars(c))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

# ================================================================================|COUNTER-2|=============================================================================================================

@app.route('/counter-2/empty/', methods=["GET", "POST"])
def empty2():
    for i in range(len(occupied_customers)):
        if occupied_customers[i][1] == 2:
            occupied_customers[i].end_service()
            occupied_customers[i][0].alert_customer("Please review your experience at <URL>!")
            del occupied_customers[i]
            break
    c = line2.get_next_customer()
    occupied_customers.append((c, 2))
    customers_not_reviewed.append(c)
    r = requests.post(url="https://5e339b7d.ngrok.io/counter-2/next/",data=vars(c))
    c.alert_customer("Please reach counter 2")
    c.end_waiting_time()
    c.start_counter_time()
    response = flask.jsonify(vars(c))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

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
    response = flask.jsonify(vars(c))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

# ================================================================================|COUNTER-3|=============================================================================================================

@app.route('/counter-3/empty/', methods=["GET", "POST"])
def empty3():
    for i in range(len(occupied_customers)):
        if occupied_customers[i][1] == 3:
            occupied_customers[i].end_service()
            occupied_customers[i][0].alert_customer("Please review your experience at <URL>!")
            del occupied_customers[i]
            break
    c = line3.get_next_customer()
    occupied_customers.append((c, 3))
    customers_not_reviewed.append(c)
    r = requests.post(url="https://counter 3")
    c.end_waiting_time()
    c.start_counter_time()
    response = flask.jsonify(vars(c))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

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
    response = flask.jsonify(vars(c))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

# ================================================================================|COUNTER-4|=============================================================================================================

@app.route('/counter-4/empty/', methods=["GET", "POST"])
def empty4():
    for i in range(len(occupied_customers)):
        if occupied_customers[i][1] == 4:
            occupied_customers[i].end_service()
            occupied_customers[i][0].alert_customer("Please review your experience at <URL>!")
            del occupied_customers[i]
            break
    c = line1.get_next_customer()
    occupied_customers.append((c, 4))
    customers_not_reviewed.append(c)
    r = requests.post(url="https://5e339b7d.ngrok.io/counter-4/next/",data=vars(c))
    c.alert_customer("Please reach counter 4")
    c.end_waiting_time()
    c.start_counter_time()
    response = flask.jsonify(vars(c))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

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
    response = flask.jsonify(vars(c))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

@app.route('/review/', methods=["GET", "POST"])
def customer_served():
    id = flask.request.args.get('ID')
    review = flask.request.args.get('review')
    rating = flask.request.args.get('rating')
    print(review, rating)
    for i in range(len(customers_not_reviewed)):
        if customers_not_reviewed[i].ID == id:
            c = customers_not_reviewed.pop(i)
            break
    cur.execute("INSERT INTO reviews VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", (c.ID, c.mobile_number, c.D_score, c.is_specially_abled, c.waiting_time, c.on_counter_time, c.re_entries, review, rating))
    return flask.Response(), 200

@app.route('/get-info/', methods=["GET", "POST"])
def get_info():
    with open('resources/params.dat', 'rb') as file:
        try:
            data = pickle.load(file)
        except EOFError:
            data = {'pi':[5, 6.5, 5.5, 6, 7, 7.2, 7.8, 7.5, 8]}
    with open('resources/review stats.dat', 'rb') as file:
        try:
            stats = pickle.load(file)
        except EOFError:
            stats = {"time":5, "employee":4, "ambience":2}
    response = flask.jsonify({"PI":data["pi"], "stats":stats})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

# @app.route('/change-weights/', methods=["GET", "POST"])
# def change_weights
@app.route('/test/', methods=["GET", "POST"])
def test():
    print(flask.request, flask.request.args)
    return flask.Response(), 200

if __name__ == "__main__":
    app.run(port=4000)
