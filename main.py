# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import myfitnesspal
from MFPCreds import name, pw, email, emailpw
import datetime as dt
import smtplib, ssl
import bs4,webbrowser
import requests
import time


class MFP:

    def __init__(self):
        self.Client = myfitnesspal.Client(name, password=pw)
        self.T = dt.date.today() - dt.timedelta(days=1)
        self.Tminus7 = self.T - dt.timedelta(days=7)

    def getNutritionDictwkAvg(self):
        """ returns an avg/week dict of nutrition like {'calories': 2100, 'carbs': 30, ...}"""
        stat_dict = {}
        for stat in ["calories", "carbs", "fat", "protein"]:
            weekrange = self.Client.get_report(stat, "Nutrition", self.T, self.Tminus7)
            lizt = list(weekrange.values())
            avgWk = round(sum(lizt) / len(lizt))
            stat_dict[stat] = avgWk
        return stat_dict

    def getCardioWkAvg( self ):
        """ returns avg/week kcal from exercise """
        weekrange = self.Client.get_report("Calories Burned", "Fitness", self.T, self.Tminus7)
        lizt = list(weekrange.values())
        avgWk = round(sum(lizt) / len(lizt))
        return avgWk

    def getWeightWkAvg( self, diff=False ):
        """ returns avg/week weight """
        weekRange = self.Client.get_report("Weight", "Progress", self.T, self.Tminus7)
        lizt = list(weekRange.values())
        avgWk = round(sum(lizt) / len(lizt))
        if diff:
            Tminus14 = self.Tminus7 - dt.timedelta(days=7)
            lastWeekRange = self.Client.get_report("Weight", "Progress",self.Tminus7, Tminus14)
            lizt2 = list(lastWeekRange.values())
            avgLastWk = round(sum(lizt2) / len(lizt2))
            return avgWk - avgLastWk
        return avgWk

    def cardioToSteps(self):
        """ returns avg/week step count estimate """
        return self.getCardioWkAvg()/0.03


#autocoachpython@gmail.com
#PassWork90!
def sendMail():
    smtp_server = "smtp.gmail.com"
    port = 587                                    # For starttls
    sender_email = email               #sender's mail id
    receiver_email  = ['alangrenfell@gmail.com']        #list of reciever's mail ids
    password = emailpw

    subject="Auto Coach"
    text = get_data()
    message = 'Subject: {}\n\n{}'.format(subject, text)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo()                               # Can be omitted
        server.starttls(context=context)            # Secure the connection
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        print(e)

def get_data():
    client = MFP()
    weight_change = client.getWeightWkAvg( diff=True )
    nutrition_dict = client.getNutritionDictwkAvg()
    cardio = client.getCardioWkAvg()
    stri = ''
    for k, v in nutrition_dict.items():
        stri += (str(k) + ': ' + str(v) + ', ')

    email_string = 'macros: {}, kcal: {}, weight change: {}, steps: {}, cardio kcal: {}'.format(stri, nutrition_dict['calories'], weight_change, cardio)
    return email_string

