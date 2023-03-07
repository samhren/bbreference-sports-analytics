from pytrends.request import TrendReq

pytrends = TrendReq(hl="en-US", tz=300)


def getNumberOfDaysInMonth(month, year):
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month == 2:
        if year % 4 == 0:
            return 29
        else:
            return 28
    else:
        return 30


def getPlayerPopularity(player_name, team_name, month, year):
    timeString = (
        year
        + "-"
        + month
        + "-01"
        + " "
        + year
        + "-"
        + month
        + "-"
        + str(getNumberOfDaysInMonth(int(month), int(year)))
    )
    kw_list = [player_name, team_name]
    pytrends.build_payload(kw_list, timeframe=timeString, geo="US")
    print(pytrends.interest_over_time())


if __name__ == "__main__":
    getPlayerPopularity("Darius Garland", "Cleveland Cavaliers", "04", "2022")
