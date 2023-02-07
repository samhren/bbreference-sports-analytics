import simplejson as json
import re
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import datetime

TEAM = "CLE"
TEAM_NAME = "Cleveland Cavaliers"
START_SEASONS = 2010
END_SEASONS = 2023

# Get list of season urls
def get_seasons():
    seasons = []
    for i in range(START_SEASONS, END_SEASONS):
        SEASON_URL = (
            "https://www.basketball-reference.com/teams/"
            + TEAM
            + "/"
            + str(i)
            + "_games.html"
        )
        seasons.append({"url": SEASON_URL, "year": str(i)})
    return seasons


# Remove all non-ascii characters
def remove_non_ascii(text):
    return str(text).encode("ascii", "ignore").decode()


# Convert dataframe to list of dicts
def dataframe_to_list_of_dicts(df):

    data = []
    for index, row in df.iterrows():
        dict = {}
        for col in df.columns:
            if col == "('Unnamed: 0_level_0', 'Starters')":
                # Removes all non-ascii characters
                dict["name"] = remove_non_ascii(row[col])
            else:
                colName = col.replace("('Advanced Box Score Stats', '", "").replace(
                    "')", ""
                )
                # Removes all non-ascii characters
                dict[colName] = remove_non_ascii(row[col])

        data.append(dict)
    return data


# Get list of game urls using BeautifulSoup
# USES 1 API CALL
def get_game_urls(season_url):
    request = requests.get(season_url)
    if request.status_code != 200:
        print("Error: " + str(request.status_code), "Season URL: " + season_url)
        quit()
    soup = BeautifulSoup(request.content, "html5lib")
    game_links = soup.findAll("a", href=True, text="Box Score")
    links = []
    for game in game_links:
        links.append("https://www.basketball-reference.com" + game["href"])
    return links


# Get game stats using BeautifulSoup
# USES 1 API CALL
def get_game_stats(game_url):
    request = requests.get(game_url)
    if request.status_code != 200:
        print("Error: " + str(request.status_code), "Game URL: " + game_url)
        quit()
    soup = BeautifulSoup(request.content, "html5lib")

    gameStats = {}

    # Cavs Record
    # Opponent Record
    scores = soup.find_all("div", {"class": "scores"})
    for score in scores:
        if score is not None:
            try:
                teamName = score.parent.find("strong").text.strip()
            except:
                teamName = "N/A"
            try:
                teamAbr = (
                    score.parent.find("strong").find("a")["href"].split("/")[2].strip()
                )
            except:
                teamAbr = "N/A"
            try:
                record = score.parent.find("div", text=re.compile("-")).text.strip()
            except:
                record = "N/A"
            if teamName != TEAM_NAME:
                gameStats["opponent"] = {
                    "name": remove_non_ascii(teamName),
                    "record": remove_non_ascii(record),
                    "teamAbr": remove_non_ascii(teamAbr),
                }
            else:
                gameStats["cavs"] = {
                    "name": remove_non_ascii(teamName),
                    "record": remove_non_ascii(record),
                    "teamAbr": remove_non_ascii(teamAbr),
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

    try:
        inactiveString = soup.find("strong", text=re.compile("Inactive:")).parent.text
        cavsInactive = inactiveString.split("CLE")[1]
        opponentInactive = inactiveString.split(gameStats["opponent"]["teamAbr"])[1]
        if gameStats["opponent"]["teamAbr"] in cavsInactive:
            opponentInactive = cavsInactive.split(gameStats["opponent"]["teamAbr"])[
                1
            ].split(",")
            cavsInactive = cavsInactive.split(gameStats["opponent"]["teamAbr"])[
                0
            ].split(",")
        else:
            cavsInactive = inactiveString.split("CLE")[1].split(",")
            opponentInactive = opponentInactive.split("CLE")[0].split(",")

        for inactive in cavsInactive:
            inactive = inactive.strip().replace("\xa0", "")
            if inactive != "":
                gameStats["cavs"]["inactive"].append(remove_non_ascii(inactive))
        for inactive in opponentInactive:
            inactive = inactive.strip().replace("\xa0", "")
            if inactive != "":
                gameStats["opponent"]["inactive"].append(remove_non_ascii(inactive))
    except:
        gameStats["cavs"]["inactive"] = []
        gameStats["opponent"]["inactive"] = []

    # Attendance
    try:
        inactiveString = soup.find("strong", text=re.compile("Attendance:")).parent.text
        gameStats["attendance"] = remove_non_ascii(
            inactiveString.split("Attendance:")[1].strip()
        )
    except:
        gameStats["attendance"] = "N/A"

    # Length of Game
    try:
        inactiveString = soup.find(
            "strong", text=re.compile("Time of Game:")
        ).parent.text
        gameStats["length"] = remove_non_ascii(
            inactiveString.split("Time of Game:")[1].strip()
        )
    except:
        gameStats["length"] = "N/A"

    # DateTime of Game
    try:
        box = soup.find("div", {"class": "scorebox_meta"})
        dateTime = [i.text.strip() for i in box.select("div:first-child")][0]
        time = dateTime.split(",")[0]
        date = dateTime.split(",")[1] + "," + dateTime.split(",")[2]
        dateTime = (date + " " + time).strip()
        gameStats["dateTime"] = datetime.datetime.strptime(
            dateTime, "%B %d, %Y %I:%M %p"
        )
        gameStats["dayOfWeek"] = gameStats["dateTime"].strftime("%A")
    except:
        gameStats["dateTime"] = "N/A"
        gameStats["dayOfWeek"] = "N/A"

    # Location of Game
    try:
        location = [i.text.strip() for i in box.select("div:nth-child(2)")][0]
        gameStats["location"] = remove_non_ascii(location)
    except:
        gameStats["location"] = "N/A"

    # Game ID
    try:
        gameStats["gameID"] = remove_non_ascii(game_url.split("/")[4].split(".")[0])
    except:
        gameStats["gameID"] = "N/A"

    # Game URL
    gameStats["gameURL"] = game_url

    # Add against to gameStats
    gameStats["against"] = gameStats["opponent"]["teamAbr"]

    # Game Result
    try:
        scores = soup.find_all("div", {"class": "score"})
        for score in scores:
            if score is not None:
                teamName = score.parent.parent.find("strong").text.strip()
                if teamName != TEAM_NAME:
                    gameStats["opponent"]["score"] = remove_non_ascii(
                        score.text.strip()
                    )
                else:
                    gameStats["cavs"]["score"] = remove_non_ascii(score.text.strip())
    except:
        gameStats["cavs"]["score"] = "N/A"
        gameStats["opponent"]["score"] = "N/A"

    return gameStats


# MAIN MUST USE LESS THAN 20 API CALLS PER MINUTE
# 60 / 20 = 3 seconds between calls
# 3.5 seconds for safety
# Sleep 1 minute before starting
def main():
    api_call_delay = 3.5
    api_call_count = 0

    time.sleep(60)

    seasons = get_seasons()
    for season in seasons:
        currSeasonGames = []

        # 1 API Call
        games = get_game_urls(season["url"])
        api_call_count += 1
        time.sleep(api_call_delay)
        for game in games:

            # 1 API Call
            try:
                gameStats = get_game_stats(game)
            except Exception as e:
                print(e)
                print(game)
                quit()
            currSeasonGames.append(gameStats)
            api_call_count += 1
            time.sleep(api_call_delay)

        # Save to file
        with open(f"data/scrapeData/CAVS_{season['year']}.json", "w+") as f:
            json.dump(
                currSeasonGames,
                f,
                indent=4,
                sort_keys=True,
                default=str,
                ignore_nan=True,
            )

        print(f"Finished {season['year']}")


# with open("gameStats.json", "w") as f:
#     json.dump(
#         get_game_stats(
#             "https://www.basketball-reference.com/boxscores/201002210ORL.html"
#         ),
#         f,
#         indent=4,
#         sort_keys=True,
#         default=str,
#         ignore_nan=True,
#     )

if __name__ == "__main__":
    main()
