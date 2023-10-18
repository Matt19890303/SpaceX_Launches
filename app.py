# Use Flask to setup a website using python 
from flask import Flask, render_template,request
from datetime import datetime
import requests
from bs4 import BeautifulSoup



########################################################################################################

# from flask import Flask, render_template
# import requests
# from bs4 import BeautifulSoup

# # Specify the URL you want to scrape
# url = 'https://spaceflightnow.com/launch-schedule/'

# # Send an HTTP GET request to the URL
# new_response = requests.get(url)

# doc = BeautifulSoup(new_response.text, "html.parser")

# launche_dates = doc.find_all(class_='launchdate')
# mission_name = doc.find_all(class_='mission')
# launch_text = doc.find_all(class_='missdescrip')

# main_content = doc.find(class_='mh-content')
# name = main_content.find("header", class_="page-header").text.replace(' ','')
# text = main_content.find(class_='entry-content clearfix').text.replace(' ','')

# # Print the content of each element
# # for dates in launche_dates:
# #     print(dates.text)

# # for names in mission_name:
# #     print(names.text)

# # for texts in launch_text:
# #     print(texts.text)

# # print(name)
# # print(text)


# app = Flask(__name__)
# @app.route("/")

# def home():
#     return render_template('index.html', name=name, text=text)


# if __name__ == "__main__":
#     # Anytime we make a change inside of our python file it will automatically update the webserver for us.
#     app.run(debug=True)


########################################################################################################



app = Flask(__name__)
# Web route
# "/" base route of our website
# can route to other pages as well example - "/home" or "/about" etc.
@app.route("/")

def index():
    return render_template("index.html", launches=launches, name=name, text=text)
    # return render_template("index.html", launches=launches, launches_to_come=launches_to_come)


# Create filter to pop off the unnecessary times/details on the date
@app.template_filter('date_only')
# writing a function that we will access to from inside our template
def date_only_filter(date_string):
    # strip the time off date / string
    # format of the strip we want to strip the time off of ("%Y-%m-%dT%H:%M:%S.%fZ")
    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_object.date()

def fetch_spacex_launches():
    # Acces to the upcoming and previous launches
    url = "https://api.spacexdata.com/v4/launches"
    # .get to get some data from the above url
    # you get a response any time to send a request - get request and generates a response for us 
    response = requests.get(url)
    # Checks to see if the response was successful
    if response.status_code == 200:
        # returns a dictionary with allthe keys and values in it
        return response.json()
    # else return empty array
    else:
        return []
    
    
# function to categorise launches as successful, failed or upcoming
def categorise_launches(Launches):
    # looking through launches array and filtering this and adds it to success variable if the keys "success" is in the data and the key "upcoming" is not
    # lambda is an anonomous function
    successful = list(filter(lambda x: x["success"] and not x["upcoming"], Launches))
    failed = list(filter(lambda x: not x["success"] and not x["upcoming"], Launches))
    # upcoming = list(filter(lambda x: x["upcoming"], Launches))

    return {
        "successful": successful,
        "failed": failed,
        # "upcoming": upcoming
    }
####################################################################
# lambda is replacing the below function
# def is_success(Launch):
#     return Launch["success"] and not Launch["upcoming"]
####################################################################

launches = categorise_launches(fetch_spacex_launches())


# https://www.youtube.com/watch?v=F1mkrEfM_ZU
# Upcoming Launches
# Specify the URL you want to scrape
url = 'https://spaceflightnow.com/launch-schedule/'

# Send an HTTP GET request to the URL
new_response = requests.get(url)

doc = BeautifulSoup(new_response.text, "html.parser")

# launche_dates = doc.find_all(class_='launchdate')
# mission_name = doc.find_all(class_='mission')
# launch_text = doc.find_all(class_='missdescrip')

main_content = doc.find(class_='mh-content')
name = main_content.find("header", class_="page-header").text.replace(' ','')
text = main_content.find(class_='entry-content clearfix').text



if __name__ == "__main__":
    # Anytime we make a change inside of our python file it will automatically update the webserver for us.
    app.run(debug=True)




