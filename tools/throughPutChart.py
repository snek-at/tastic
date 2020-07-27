# IMPORTS
import requests
import json
from datetime import *
import numpy as np
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# VARIABLES
#Environment
project_folder = os.path.expanduser("./")
load_dotenv(os.path.join(project_folder, ".env"))
#Global
api_url = "https://api.github.com" 
labels = ["Feature", "Opportunity", "Requirement", "bug", "enchancement"]
repos = []
issues = []
text = ""
project_start = datetime(2020, 7, 15)
today = datetime.today()
calendar = {}

# EXECUTION
#Get all repository names from snek-at organization
with requests.get(f"{api_url}/users/snek-at/repos?access_token={os.getenv('ACCESS_TOKEN')}") as repo_req:
    #Convert html response to json
    repo_json = json.loads(repo_req.text)

    for repo in repo_json:
        repos.append(repo["name"])

#Loop through each found repository
for repo in repos:
    #Get all issues from the repository
    with requests.get(f"{api_url}/repos/snek-at/{repo}/issues?state=all&access_token={os.getenv('ACCESS_TOKEN')}") as issue_req:
        #Convert html response to json
        issue_json = json.loads(issue_req.text)

        #Loop through each issue
        for issue in issue_json:
            #Loop through each label
            for label in issue["labels"]:
                #Check if the label is in the defined labels
                if label["name"] in labels:
                    #Get datetime when the issue was created
                    created_at = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")

                    #Check if issue was created after project start
                    if created_at > project_start:
                        issues.append(issue)

#Create calendar
while today > project_start:
    calendar[today] = []
    today -= timedelta(days=1)

#Loop through each date of the calendar
for date in calendar:
    issues_closed_per_date = {
        "Requirement" : 0,
        "Feature": 0,
        "Opportunity": 0,
        "bug": 0,
        "enchancement": 0,
    }

    #Loop through each issue
    for issue in issues:
        #Check if issue was closed
        closed_at = issue["closed_at"]
        if closed_at:
            closed_at = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
            #Check if GitHub closed at equals calendar date
            if closed_at.year == date.year and closed_at.month == date.month and closed_at.day == date.day:
                #Loop through each label
                for label in labels:
                    #Loop through each issue label
                    for issue_label in issue["labels"]:
                        if label == issue_label["name"]:
                            issues_closed_per_date[label] += 1

    calendar[date] = issues_closed_per_date

# CHART
#Set x axis values
ind = np.arange(len(calendar))
#Set bar width
width = 0.35

# VARIABLES
requirements_count = []
features_count = []
opportunities_count = []
enchancements_count = []
bugs_count = []

#Loop through each day of the calendar
for date in calendar:
    #Get day of calendar
    date = calendar[date]

    #Get issues count of the day
    requirements_count.append(date["Requirement"])
    opportunities_count.append(date["Opportunity"])
    features_count.append(date["Feature"])
    enchancements_count.append(date["enchancement"])
    bugs_count.append(date["bug"])

#Set bars
bar_requirements = plt.bar(ind, requirements_count, width, color="#90f9a2")
bar_features = plt.bar(ind, features_count, width, color="#ba056b")
bar_opportunities = plt.bar(ind, opportunities_count, width, color="#593ba5")
bar_enchancements = plt.bar(ind, enchancements_count, width, color="#a2eeef")
bar_bugs = plt.bar(ind, bugs_count, width, color="#d73a4a")

#Set y label
plt.ylabel("Solved issues")
#Set char title
plt.title("Issues by date and tag")
#Set x axis ticks
xticks_label = []
for date in calendar:
    xticks_label.append(f"{date.month}/{date.day}")

plt.xticks(ind, xticks_label)
#Set y axis ticks
plt.yticks(np.arange(0, 21, 2))
#Set legend for chart
plt.legend((bar_requirements[0], bar_features[0], bar_opportunities[0], bar_enchancements[0], bar_bugs[0]), ("Requirements", "Features", "Opportunities", "Enchancements", "Bugs"))

#Display the chart
plt.show()

"""
SPDX-License-Identifier: (EUPL-1.2)
Copyright © Simon Prast
"""