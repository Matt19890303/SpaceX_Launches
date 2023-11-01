
# Use Flask to setup a website using python 
from flask import Flask, render_template, request
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re


app = Flask(__name__)
# Web route
# "/" base route of our website
# can route to other pages as well example - "/home" or "/about" etc.
@app.route("/")

def index():
    # Calculate the number of entries
    data_length = len(dates)
    # return render_template("index.html", launches=launches, name=name, text=text, content=content)
    return render_template("index.html", launches=launches, header=header, header_text=header_text, data_length=data_length, dates=dates, mission_name=mission_name, launch_times=launch_times, launch_sites=launch_sites, descriptions=descriptions)

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



# # https://www.youtube.com/watch?v=F1mkrEfM_ZU
# # Upcoming Launches
# # Specify the URL you want to scrape
url = 'https://spaceflightnow.com/launch-schedule/'

# Send an HTTP GET request to the URL
new_response = requests.get(url)

doc = BeautifulSoup(new_response.text, "html.parser")

header = doc.find(class_='page-header').text
header_text = doc.find(class_='entry-content clearfix').text

main_content = doc.find(class_='mh-content').text
data = ''
data += main_content
# Split the string at the delimiter '\n\n\n\n\n\n'
data = data.split('\n\n\n\n\n\n')

# Initialize lists to store extracted data
dates = []
mission_name = []
launch_sites = []
launch_times = []
descriptions = []


# Lauch Date
# Find all elements with the desired class name and extract their text
launch_date_name = doc.find_all(class_='launchdate')

# Extract text from each element and add it to the list
for date_name in launch_date_name:
    text = date_name.get_text()
    dates.append(text)


# Mission name
# Find all elements with the desired class name and extract their text
launch_name = doc.find_all(class_='mission')

# Extract text from each element and add it to the list
for launch_name in launch_name:
    text = launch_name.get_text()
    mission_name.append(text)


# Launch times and sites
# Find all elements with the desired class name and extract their text
mission_time = doc.find_all(class_='missiondata')
mission_data_list = []

# Extract text from each element and add it to the list
for time in mission_time:
    text = time.get_text()
    mission_data_list.append(text)

# Launch times
# Iterate through the launch_info list
for info in mission_data_list:
    # Use a regular expression to extract the launch time
    launch_time_match = re.search(r'Launch time: \n\n(.*?)\n', info)

    if launch_time_match:
        launch_time = launch_time_match.group(1).strip()
        launch_times.append(launch_time)

# Launch sites
# Iterate through the launch_info list
for info in mission_data_list:
    # Use regular expressions to extract launch time and launch site
    launch_site_match = re.search(r'Launch site: (.*?)$', info)

    if launch_site_match:
        launch_site = launch_site_match.group(1).strip()
        launch_sites.append(launch_site)


# Mission Description
# Find all elements with the desired class name and extract their text
launch_description = doc.find_all(class_='missdescrip')

# Initialize a list to store the first <p> tags from each <div>
# Loop through the <div> elements
for div in launch_description:
    # Find the first <p> tag within the current <div>
    first_p = div.find('p')
    # Get the text content of the first <p> tag
    if first_p:
        first_p_text = first_p.get_text(strip=True)
        descriptions.append(first_p_text)


if __name__ == "__main__":
    # Anytime we make a change inside of our python file it will automatically update the webserver for us.
    app.run(debug=True)

