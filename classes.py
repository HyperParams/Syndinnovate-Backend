import datetime
import pickle
import heapq
import psycopg2
from twilio.rest import Client

# initializing sms api-twilio
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
client = Client(account_sid, auth_token)

# initializing postgresql db
conn = psycopg2.connect("dbname=syndicatebank user=rachit")
cur = conn.cursor()

def sql_query(mobile_number):
    # RAMANSH PSYCOPG2 IS SQL INJECTION PROOF!!!!!
    cur.execute("SELECT * FROM customerdetials WHERE mobilenumber=%s;", (mobile_number))
    customers = cur.fetchall()
    if len(customers)>1:
        print("Multiple customers with same mobile numbers!")
        return None
    elif len(customers)==0:
        print("No entry found!")
        return -1
    else:
        return customer

with open("resources/weights.bat","rb") as file:
    weights = pickle.load(file)

def get_POV():
    with open("resources/POV.bat","rb") as file:
        POV = pickle.load(file)
        return POV

class customer():

    instances = 0

    def __init__(self, mobile_number, POV, weights):
        # details to be entered by user
        self.mobile_number = mobile_number
        self.POV_code = ""
        # details to get from sql using mobile_number
        # TODO: change i in details[i] according to table structure
        details = sql_query(self.mobile_number)
        self.D_score = details[1]
        self.name = details[0]
        self.is_specially_abled = details[2]
        # details generated
        self.ID = str(datetime.datetime.now().microsecond)+mobile_number[6:]
        self.in_time = datetime.datetime.now()
        self.score = self.calculate_score(weights)
        # increasing instances
        instances += 1
        # variables for internal use
        self.re_entries = 0

    def __del__(self):
        instances -= 1

    def __lt__(self, other):
        return self.score > other.score

    def __eq__(self, other):
        return self.id == other.id

    def calculate_score(self, weights):
        POV = get_POV()
        score = 0
        score += weights["time"]*(datetime.datetime.now()-self.in_time)
        score += weights["D_score"]*self.D_score
        score += weigths["is_specially_abled"]*self.is_specially_abled
        score += weigths["POV"]*POV[self.POV_code]
        return score

    def update_digital_score(self, value):
        # TODO: update_digital_score
        pass

    def alert_customer(self, text):
        to_number = "+91"+self.mobile_number
        message = client.messages.create(body=text, from="+12015089104", to=to_number)
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
                l = [i+1:]
                break
        self.queue = heapq._heapify_max(self.queue[:i+1])

        for i in range(len(l)):
            l[i].calculate_score(weights)
            self.__push(l[i])

    def get_next_customer(self):
        return heapq._heappop_max
