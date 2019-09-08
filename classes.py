import os
import pickle
import heapq
import psycopg2
import datetime
from twilio.rest import Client

# initializing sms api-twilio
account_sid = os.environ['SID']
auth_token = os.environ['AUTH_TOKEN']
print(auth_token)
client = Client(account_sid, auth_token)

# initializing postgresql db
conn = psycopg2.connect("dbname=syndicatebank user=postgres password='postgres'")
cur = conn.cursor()

def sql_query(mobile_number):
    # RAMANSH PSYCOPG2 IS SQL INJECTION PROOF!!!!!
    cur.execute("SELECT * FROM customerdetails WHERE mobilenumber=%s;", (mobile_number,))
    customers = cur.fetchall()
    if len(customers)>1:
        print("Multiple customers with same mobile numbers!")
        return None
    elif len(customers)==0:
        print("No entry found!")
        return -1
    else:
        return (customers[0])
try:
    with open("resources/weights.bat","rb") as file:
        weights = pickle.load(file)
except FileNotFoundError:
    weights = {'time':1,
                'D_score':1,
                'is_specially_abled':1,
                'POV':1
    }

def get_POV():
    try:
        with open("resources/POV.dat","rb") as file:
            POV = pickle.load(file)
            return POV
    except FileNotFoundError:
        POV={'1':4}

class customer():

    instances = 0

    def __init__(self, mobile_number, POV, weights):
        # details to be entered by user
        self.mobile_number = str(mobile_number)
        self.POV_code = str(POV)
        # details to get from sql using mobile_number
        details = sql_query(self.mobile_number)
        self.D_score = details[2]
        self.name = details[1]
        self.is_specially_abled = details[3]
        # details generated
        self.ID = str(datetime.datetime.now().microsecond)+mobile_number[6:]
        self.in_time = datetime.datetime.now()
        self.score = self.calculate_score(weights)
        # increasing instances
        customer.instances += 1
        # variables for internal use
        self.re_entries = 0
        self.waiting_time = 0
        self.service_start = datetime.datetime.now()
        self.on_counter_time = 0

    def __del__(self):
        customer.instances -= 1

    def __lt__(self, other):
        return self.score > other.score

    def __eq__(self, other):
        return self.ID == other.ID

    def calculate_score(self, weights):
        POV = get_POV()
        score = 0
        print(weights)
        score += weights["time"]*(datetime.datetime.now()-self.in_time).total_seconds()
        score += weights["D_score"]*self.D_score
        score += weights["is_specially_abled"]*self.is_specially_abled
        score += weights["POV"]*POV[self.POV_code]
        return score

    def end_waiting_time(self):
        self.waiting_time = (datetime.datetime.now() - self.in_time).total_seconds()

    def start_counter_time(self):
        self.service_start = datetime.datetime.now()

    def end_service(self):
        self.on_counter_time = (datetime.datetime.now() - self.service_start).total_seconds()

    def update_digital_score(self, value):
        # TODO: update_digital_score
        pass

    def alert_customer(self, text):
        to_number = "+91"+self.mobile_number
        print(to_number)
        message = client.messages.create(body=text, from_="+12015089104", to=to_number)
        print(message.sid)

    def update_details(self):
        # TODO: update_details
        pass

class line():

    def __init__(self):
        self.queue = []

    def __push(self, customer):
        heapq.heappush(self.queue, customer)
        heapq._heapify_max(self.queue)

    def add_customer(self, customer):
        self.__push(customer)
        for i in range(len(self.queue)):
            if self.queue[i] == customer:
                l = self.queue[i+1:]
                self.queue = self.queue[:i+1]
                break
        heapq._heapify_max(self.queue)
        for i in l:
            self.__push(i)

        for i in range(len(l)):
            l[i].calculate_score(weights)
            self.__push(l[i])

    def get_next_customer(self):
        print(type(self.queue))
        return heapq._heappop_max(self.queue)
