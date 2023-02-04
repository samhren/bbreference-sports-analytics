import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime

TEAM = "CLE"
TEAM_NAME = "Cleveland Cavaliers"
TEAM_UTL = "https://www.basketball-reference.com/teams/" + TEAM
END_SEASONS = 2023
START_SEASONS = 2023

SEASON_URL = "https://www.basketball-reference.com/teams/" + TEAM + "/SEASON_games.html"

# Get list of season urls
def get_seasons():
    seasons = []
    for i in range(START_SEASONS, END_SEASONS):
        SEASON_URL = (
            "https://www.basketball-reference.com/teams/"
            + TEAM
            + "/"
            + i
            + "_games.html"
        )
        seasons.append(SEASON_URL)
    return seasons


# Get list of game urls using BeautifulSoup
def get_game_urls(season_url):
    request = requests.get(season_url)
    soup = BeautifulSoup(request.content, "html5lib")
    game_links = soup.findAll("a", href=True, text="Box Score")
    links = []
    for game in game_links:
        links.append("https://www.basketball-reference.com/" + game["href"])
    print(links)


# Get game stats using BeautifulSoup
def get_game_stats(game_url):
    request = requests.get(game_url)
    soup = BeautifulSoup(request.content, "html5lib")

    gameStats = {}

    ###### Cavs Record
    ###### Opponent Record
    scores = soup.find_all("div", {"class": "scores"})
    for score in scores:
        if score is not None:
            teamName = score.parent.find("strong").text.strip()
            teamAbr = (
                score.parent.find("strong").find("a")["href"].split("/")[2].strip()
            )
            record = score.parent.find("div", text=re.compile("-")).text.strip()
            if teamName != TEAM_NAME:
                gameStats["opponent"] = {
                    "name": teamName,
                    "record": record,
                    "teamAbr": teamAbr,
                }
            else:
                gameStats["cavs"] = {
                    "name": teamName,
                    "record": record,
                    "teamAbr": teamAbr,
                }
    # Cavs Roster
    # Opponent Roster
    # Cavs Stats
    # Opponent Stats
    table = soup.find(
        "table",
        {"id": "box-" + gameStats["opponent"]["teamAbr"] + "-game-advanced"},
    )

    stats = pd.read_html(str(table))[0]
    stats_dict = stats.to_dict()
    # print(stats_dict)

    # print(stats)

    # Inactive Players

    gameStats["cavs"]["inactive"] = []
    gameStats["opponent"]["inactive"] = []

    inactiveString = soup.find("strong", text=re.compile("Inactive:")).parent.text
    cavsInactive = inactiveString.split("CLE")[1]
    opponentInactive = inactiveString.split(gameStats["opponent"]["teamAbr"])[1]
    if gameStats["opponent"]["teamAbr"] in cavsInactive:
        cavsInactive = cavsInactive.split(gameStats["opponent"]["teamAbr"])[0].split(
            ","
        )
        opponentInactive = cavsInactive.split(gameStats["opponent"]["teamAbr"])[
            1
        ].split(",")
    else:
        cavsInactive = inactiveString.split("CLE")[1].split(",")
        opponentInactive = opponentInactive.split("CLE")[0].split(",")

    for inactive in cavsInactive:
        inactive = inactive.strip().replace("\xa0", "")
        if inactive != "":
            gameStats["cavs"]["inactive"].append(inactive)
    for inactive in opponentInactive:
        inactive = inactive.strip().replace("\xa0", "")
        if inactive != "":
            gameStats["opponent"]["inactive"].append(inactive)

    # Attendance
    inactiveString = soup.find("strong", text=re.compile("Attendance:")).parent.text
    gameStats["attendance"] = inactiveString.split("Attendance:")[1].strip()
    # Length of Game
    inactiveString = soup.find("strong", text=re.compile("Time of Game:")).parent.text
    gameStats["length"] = inactiveString.split("Time of Game:")[1].strip()

    box = soup.find("div", {"class": "scorebox_meta"})
    #Time of Game 
    gameStats["time"] = box.text.strip().split(",")[0]
    #Date of Game
    gameStats["date"] = box.text.strip().split(",")[1]
    #NEED ADD REGEX FIX HERE TO GET YEAR FROM SCOREBOX
    date = gameStats["date"].strip() + ", " + str(2020) 
    gameStats["date"] = date
    #Day of week
    gameStats["dotw"] = datetime.datetime.strptime(date, '%B %d, %Y').strftime('%A')

    print(gameStats)


get_game_stats("https://www.basketball-reference.com/boxscores/202002290CLE.html")


# Scrape seasons get list of urls

# For each season
# Save List of Games URL

# For each season
### For each game:
###### Cavs Record
###### Opponent Record
###### Cavs Roster
###### Opponent Roster
###### Cavs Stats
###### Opponent Stats
