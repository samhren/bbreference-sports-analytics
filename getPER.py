import json
import os
import time
from bs4 import BeautifulSoup
import pandas as pd

import requests

START_SEASONS = 2010
END_SEASONS = 2023

URL = (
    "https://www.basketball-reference.com/leagues/NBA_YEAR_advanced.html#advanced_stats"
)


class PlayerDataGrabber:
    def __init__(self):
        self.ready = False

        self.gameData = {}

        for year in range(START_SEASONS, END_SEASONS):
            with open("data/scrapeData/CAVS_" + str(year) + ".json", "r") as f:
                d = json.load(f)
                self.gameData[year] = d

        self.votingData = {}

        for year in range(START_SEASONS, END_SEASONS):
            d = pd.read_csv("data/votingData/ALLSTAR_VOTING_" + str(year) + ".csv")
            self.votingData[year] = d

        # check if per data is available

        for year in range(START_SEASONS, END_SEASONS):
            if not os.path.exists("data/perData/" + str(year) + ".csv"):

                scrape_url = URL.replace("YEAR", str(year))

                request = requests.get(scrape_url)
                if request.status_code != 200:
                    print("Error: " + str(request.status_code) + " " + scrape_url)
                    quit()

                bs4 = BeautifulSoup(request.content, "html.parser")

                tabled = bs4.find("table", {"id": "advanced_stats"})

                for s in tabled.select("tr"):
                    if s.has_attr("class"):
                        if "partial_table" in s["class"]:
                            s.extract()

                table = pd.read_html(str(tabled))[0]

                table = table[~table["Rk"].str.contains("Rk") == True].reset_index(
                    drop=True
                )[["Player", "PER"]]

                table = table.replace("\*", "", regex=True)

                table.to_csv("data/perData/" + str(year) + ".csv", index=True)

                time.sleep(3.5)

        self.perData = {}

        for year in range(START_SEASONS, END_SEASONS):
            d = pd.read_csv("data/perData/" + str(year) + ".csv")
            self.perData[year] = d

        self.ready = True

    def getPER(self, name, year):

        if not self.ready:
            print("Error: Data not ready")
            quit()

        if year not in self.perData:
            print("Error: Year not found")
            quit()

        data = self.perData[year]

        return data.loc[data["Player"] == name].values[0][2]


if __name__ == "__main__":
    pdg = PlayerDataGrabber()
    pdg.getPER("LeBron James", 2010)
