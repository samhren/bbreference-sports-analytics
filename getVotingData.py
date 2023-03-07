import json
from pprint import pprint
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests

TEAM = "CLE"
TEAM_NAME = "Cleveland Cavaliers"
START_SEASONS = 2010
END_SEASONS = 2023


def getLinks():
    links = []
    for year in range(START_SEASONS, END_SEASONS + 1):
        if year >= 2017:
            links.append(
                {
                    "year": year,
                    "links": [
                        "https://www.basketball-reference.com/allstar/NBA_"
                        + str(year)
                        + "_voting-backcourt-western-conference.html",
                        "https://www.basketball-reference.com/allstar/NBA_"
                        + str(year)
                        + "_voting-backcourt-eastern-conference.html",
                        "https://www.basketball-reference.com/allstar/NBA_"
                        + str(year)
                        + "_voting-frontcourt-western-conference.html",
                        "https://www.basketball-reference.com/allstar/NBA_"
                        + str(year)
                        + "_voting-frontcourt-eastern-conference.html",
                    ],
                }
            )
        else:
            links.append(
                {
                    "year": year,
                    "links": "https://www.basketball-reference.com/allstar/NBA_"
                    + str(year)
                    + "_voting.html",
                }
            )
    return links


def getNewData(link, year):
    request = requests.get(link)
    if request.status_code != 200:
        print("Error: " + str(request.status_code) + " " + link)
        quit()

    soup = BeautifulSoup(request.content, "html5lib")

    table = soup.find("table", {"class": "stats_table"})

    if table is None:
        print("Error: " + link)
        quit()

    pdTable = pd.read_html(str(table))[0].iloc[:, :3].iloc[:, 1:]

    pdTable.columns = ["Player", "Votes"]

    pdTable = pdTable.sort_values("Votes", ascending=False)

    return pdTable


def getOldData(link, year):
    request = requests.get(link)
    if request.status_code != 200:
        print("Error: " + str(request.status_code) + " " + link)
        quit()

    soup = BeautifulSoup(request.content, "html5lib")

    eastern = soup.find("div", {"id": "voting-results-E_1"}).parent
    western = soup.find("div", {"id": "voting-results-W_1"}).parent

    easternTable = eastern.find_all("table")
    westernTable = western.find_all("table")

    eastData = []

    if year <= 2012:
        eastData.append(
            pd.read_html(str(easternTable))[2]
            .iloc[1:, 1:]
            .rename(columns={1: "Player", 2: "Votes"})
        )

    eastData.append(
        pd.read_html(str(easternTable))[0]
        .iloc[1:, 1:]
        .rename(columns={1: "Player", 2: "Votes"})
    )
    eastData.append(
        pd.read_html(str(easternTable))[1]
        .iloc[1:, 1:]
        .rename(columns={1: "Player", 2: "Votes"})
    )

    westData = []

    if year <= 2012:
        westData.append(
            pd.read_html(str(westernTable))[2]
            .iloc[1:, 1:]
            .rename(columns={1: "Player", 2: "Votes"})
        )

    westData.append(
        pd.read_html(str(westernTable))[0]
        .iloc[1:, 1:]
        .rename(columns={1: "Player", 2: "Votes"})
    )

    westData.append(
        pd.read_html(str(westernTable))[1]
        .iloc[1:, 1:]
        .rename(columns={1: "Player", 2: "Votes"})
    )

    allData = westData + eastData

    table = (
        pd.concat(allData)
        .sort_values("Votes", ascending=False)
        .reset_index()
        .drop(columns=["index"])
    )

    return table


def main():

    api_call_delay = 3.5

    links = getLinks()
    for link in links:
        year = link["year"]

        if type(link["links"]) == list:
            # After 2016
            data = []
            for l in link["links"]:
                data.append(getNewData(l, year))
                time.sleep(api_call_delay)
            data = (
                pd.concat(data)
                .sort_values("Votes", ascending=False)
                .reset_index()
                .drop(columns=["index"])
            )
            data.to_csv(
                f"data/votingData/ALLSTAR_VOTING_{year}.csv", sep=",", index=False
            )

        else:
            # Before 2017
            getOldData(link["links"], year).to_csv(
                f"data/votingData/ALLSTAR_VOTING_{year}.csv", sep=",", index=False
            )
            time.sleep(api_call_delay)

        print(f"Finished {year}")


if __name__ == "__main__":
    main()
