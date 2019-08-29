import datetime
import pickle

#test

def sql_query(mobile_number):
    # TODO: implement SQL query
    pass

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
        details = sql_query(self.mobile_number)
        self.D_score = details["D_score"]
        self.name = details["Name"]
        self.is_specially_abled = details["is_specially_abled"]
        # details generated
        self.ID = instances # TODO: rethink how to create unique ids on a daily basis
        self.in_time = datetime.datetime.now()
        self.score = self.calculate_score(weights)
        # increasing instances
        instances += 1

    def __del__(self):
        instances -= 1

    def __lt__(self, other):
        return self.score > other.score

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

    def alert_customer(self):
        # TODO: alert_customer
        pass

    def update_details(self):
        # TODO: update_details
        pass
