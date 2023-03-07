import simplejson as json
import pandas as pd


TEAM = "CLE"
TEAM_NAME = "Cleveland Cavaliers"
START_SEASONS = 2010
END_SEASONS = 2023


def main():
    for year in range(START_SEASONS, END_SEASONS + 1):
        # grab the data from json then grab the csv data and update the json

        # get the data from the json file
        with open("data/scrapeData/CAVS_" + str(year) + ".json", "r") as f:
            data = json.load(f)

        # get the data from the csv file
        csv_data = pd.read_csv("data/votingData/ALLSTAR_VOTING_" + str(year) + ".csv")

        # update the json file with the csv data
        for game in data:
            cavsStarters = game["cavs"]["starters"]
            opponentStarters = game["opponent"]["starters"]

            for starter in cavsStarters:
                # find the player in the csv data
                nameMatch = csv_data[csv_data["Player"].str.contains(starter["name"])]
                if nameMatch.shape[0] == 0:
                    starter["ASV"] = str(0)
                elif nameMatch.shape[0] == 1:
                    starter["ASV"] = str(int(nameMatch["Votes"].values[0]))
                else:
                    print("Error: " + str(nameMatch.shape[0]))

            for starter in opponentStarters:
                # find the player in the csv data
                nameMatch = csv_data[csv_data["Player"].str.contains(starter["name"])]
                if nameMatch.shape[0] == 0:
                    starter["ASV"] = str(0)
                elif nameMatch.shape[0] == 1:
                    starter["ASV"] = str(int(nameMatch["Votes"].values[0]))
                else:
                    print("Error: " + str(nameMatch.shape[0]))

        # write the updated json file
        with open("data/scrapeDataUpdated/CAVS_" + str(year) + ".json", "w") as f:
            json.dump(
                data,
                f,
                sort_keys=True,
                default=str,
                ignore_nan=True,
            )


if __name__ == "__main__":
    main()
