import re
from bs4 import BeautifulSoup
import numpy as np
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


def dataframe_to_list_of_dicts(df):
    data = []
    for index, row in df.iterrows():
        dict = {}
        for col in df.columns:
            if col == "('Unnamed: 0_level_0', 'Starters')":
                dict["name"] = row[col]
            else:
                colName = col.replace("('Advanced Box Score Stats', '", "").replace(
                    "')", ""
                )
                dict[colName] = row[col]

        data.append(dict)
    return data


# Get game stats using BeautifulSoup
def get_game_stats(game_url):
    request = requests.get(game_url)
    soup = BeautifulSoup(request.content, "html5lib")

    gameStats = {}

    # Cavs Record
    # Opponent Record
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

    # Opponent Roster
    # Opponent Stats
    opponentsAdvancedStats = pd.read_html(
        str(
            soup.find(
                "table",
                {"id": "box-" + gameStats["opponent"]["teamAbr"] + "-game-advanced"},
            )
        )
    )[0]
    opponentsAdvancedStats.columns = [str(s) for s in opponentsAdvancedStats.columns]

    # Get index of reserve row and split table
    opponentsReservesIndex = opponentsAdvancedStats.index[
        opponentsAdvancedStats["('Unnamed: 0_level_0', 'Starters')"] == "Reserves"
    ].tolist()[0]

    opponentsReserves = np.split(opponentsAdvancedStats, [opponentsReservesIndex])[1]
    opponentsReserves.drop(opponentsReserves.tail(1).index, inplace=True)
    opponentsReserves.drop(opponentsReserves.head(1).index, inplace=True)

    opponentsStarters = np.split(opponentsAdvancedStats, [opponentsReservesIndex])[0]

    # Convert to list of dicts and add to gameStats
    gameStats["opponent"]["reserves"] = dataframe_to_list_of_dicts(opponentsReserves)
    gameStats["opponent"]["starters"] = dataframe_to_list_of_dicts(opponentsStarters)

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

    # DateTime of Game
    box = soup.find("div", {"class": "scorebox_meta"})
    dateTime = [i.text.strip() for i in box.select("div:first-child")][0]
    time = dateTime.split(",")[0]
    date = dateTime.split(",")[1] + "," + dateTime.split(",")[2]
    dateTime = (date + " " + time).strip()
    gameStats["time"] = datetime.datetime.strptime(dateTime, "%B %d, %Y %I:%M %p")

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
