
# Use Flask to setup a website using python 
from flask import Flask, render_template, request
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re


# app = Flask(__name__)
# # Web route
# # "/" base route of our website
# # can route to other pages as well example - "/home" or "/about" etc.
# @app.route("/")

# def index():
#     data_length = len(dates)  # Calculate the number of entries
#     # return render_template("index.html", launches=launches, name=name, text=text, content=content)
#     return render_template("index.html", launches=launches, data_length=data_length, dates=dates, mission_name=mission_name, mission_data_list=mission_data_list, descriptions=descriptions)



# # Create filter to pop off the unnecessary times/details on the date
# @app.template_filter('date_only')
# # writing a function that we will access to from inside our template
# def date_only_filter(date_string):
#     # strip the time off date / string
#     # format of the strip we want to strip the time off of ("%Y-%m-%dT%H:%M:%S.%fZ")
#     date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
#     return date_object.date()

# def fetch_spacex_launches():
#     # Acces to the upcoming and previous launches
#     url = "https://api.spacexdata.com/v4/launches"
#     # .get to get some data from the above url
#     # you get a response any time to send a request - get request and generates a response for us 
#     response = requests.get(url)
#     # Checks to see if the response was successful
#     if response.status_code == 200:
#         # returns a dictionary with allthe keys and values in it
#         return response.json()
#     # else return empty array
#     else:
#         return []
    
    
# # function to categorise launches as successful, failed or upcoming
# def categorise_launches(Launches):
#     # looking through launches array and filtering this and adds it to success variable if the keys "success" is in the data and the key "upcoming" is not
#     # lambda is an anonomous function
#     successful = list(filter(lambda x: x["success"] and not x["upcoming"], Launches))
#     failed = list(filter(lambda x: not x["success"] and not x["upcoming"], Launches))
#     # upcoming = list(filter(lambda x: x["upcoming"], Launches))

#     return {
#         "successful": successful,
#         "failed": failed,
#         # "upcoming": upcoming
#     }
# ####################################################################
# # lambda is replacing the below function
# # def is_success(Launch):
# #     return Launch["success"] and not Launch["upcoming"]
# ####################################################################

# launches = categorise_launches(fetch_spacex_launches())



# # https://www.youtube.com/watch?v=F1mkrEfM_ZU
# # Upcoming Launches
# # Specify the URL you want to scrape
url = 'https://spaceflightnow.com/launch-schedule/'

# Send an HTTP GET request to the URL
new_response = requests.get(url)

doc = BeautifulSoup(new_response.text, "html.parser")

main_content = doc.find(class_='mh-content').text
data = ''
data += main_content
# Split the string at the delimiter '\n\n\n\n\n\n'
data = data.split('\n\n\n\n\n\n')
# print(data)


# # Initialize lists to store extracted data
# dates = []
# mission_name = []
# mission_data_list = []
# descriptions = []



################################################################################################
# for item in data[1:]:  # Skip the first item which is not a mission entry
#     # Extract date and mission name
#     date_and_mission = re.split(r'\n', item, maxsplit=1)
#     date, mission = date_and_mission[0], date_and_mission[1]

#     # Extract mission details and description
#     mission_details = re.split(r'\nUpdated:', mission, maxsplit=1)
#     mission_detail = mission_details[0].strip()
#     description = mission_details[1].strip() if len(mission_details) > 1 else ""

#     # Append the extracted data to their respective lists
#     dates.append(date)
#     mission_name.append(mission_detail)
#     # mission_data_list.append(mission_time)
#     descriptions.append(description)
#####################################################################################################



# # Find all elements with the desired class name and extract their text
# launch_date_name = doc.find_all(class_='launchdate')

# # Extract text from each element and add it to the list
# for date_name in launch_date_name:
#     text = date_name.get_text()
#     dates.append(text)

# # Find all elements with the desired class name and extract their text
# launch_name = doc.find_all(class_='mission')

# # Extract text from each element and add it to the list
# for launch_name in launch_name:
#     text = launch_name.get_text()
#     mission_name.append(text)


# # Find all elements with the desired class name and extract their text
# mission_time = doc.find_all(class_='missiondata')

# # Extract text from each element and add it to the list
# for time in mission_time:
#     text = time.get_text()
#     mission_data_list.append(text)

# # Find all elements with the desired class name and extract their text
# launch_description = doc.find_all(class_='missdescrip')

# # Initialize a list to store the first <p> tags from each <div>
# # Loop through the <div> elements
# for div in launch_description:
#     # Find the first <p> tag within the current <div>
#     first_p = div.find('p')
#     # Get the text content of the first <p> tag
#     if first_p:
#         first_p_text = first_p.get_text(strip=True)
#         descriptions.append(first_p_text)


# if __name__ == "__main__":
#     # Anytime we make a change inside of our python file it will automatically update the webserver for us.
#     app.run(debug=True)


# Find all the first <span> tags and the text before the <br>
first_span_tags = doc.select('.missiondata span.strong:first-child')
data_before_br = [span.get_text(strip=True) for span in first_span_tags]

print("Data Before <br> for First Span Tags:")
print(data_before_br)