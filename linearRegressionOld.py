from sklearn.linear_model import LinearRegression
import numpy as np
import json

year_data = "data/scrapeDataUpdated/CAVS_2022.json"

# Assume you have independent variables X and a dependent variable y

# GET X VALS

# fgs, 3pts, fga,

# x_1 = opponent

teamNames = {
    "ATL": 1,
    "BRK": 2,
    "BOS": 3,
    "CHO": 4,
    "CHI": 5,
    "CLE": 6,
    "DAL": 7,
    "DEN": 8,
    "DET": 9,
    "GSW": 10,
    "HOU": 11,
    "IND": 12,
    "LAC": 13,
    "LAL": 14,
    "MEM": 15,
    "MIA": 16,
    "MIL": 17,
    "MIN": 18,
    "NOP": 19,
    "NYK": 20,
    "OKC": 21,
    "ORL": 22,
    "PHI": 23,
    "PHO": 24,
    "POR": 25,
    "SAC": 26,
    "SAS": 27,
    "TOR": 28,
    "UTA": 29,
    "WAS": 30,
}

with open(year_data, "r") as f:
    data = json.load(f)
    against = []
    for i in data:
        opp_abb = i["against"]
        opp_abb_number = teamNames[opp_abb]
        against.append(opp_abb_number)
    x_1 = np.array(against)

# x_2 = record

with open(year_data, "r") as f:
    data = json.load(f)
    record = []
    for i in data:
        if i["cavs"]["record"] == "N/A" or i["cavs"]["record"] == "0-0":
            record.append(0)
            continue
        wins = int(i["cavs"]["record"].split("-")[0])
        losses = int(i["cavs"]["record"].split("-")[1])
        record.append(wins - losses)
    x_2 = np.array(record)

# x_25 opponent record
with open(year_data, "r") as f:
    data = json.load(f)
    record = []
    for i in data:
        if i["opponent"]["record"] == "N/A" or i["opponent"]["record"] == "0-0":
            record.append(0)
            continue
        wins = int(i["opponent"]["record"].split("-")[0])
        losses = int(i["opponent"]["record"].split("-")[1])
        record.append(wins - losses)
    x_3 = np.array(record)

# x_3-22 = starter stats

with open(year_data, "r") as f:
    data = json.load(f)
    # Threeps = [[1, 1, 1, 1, 1], [2, 4, 5, 6, 7], [], [], []] THE GOAL
    Threeps = [[], [], [], [], []]
    Threepps = [[], [], [], [], []]
    Fgs = [[], [], [], [], []]
    Fgps = [[], [], [], [], []]
    Ptss = [[], [], [], [], []]
    Votess = [[], [], [], [], []]
    for game in data:
        StarterThreeps = []
        StarterThreepps = []
        StarterFgs = []
        StarterFgps = []
        StarterPtss = []
        StarterVotess = []
        for starter in game["cavs"]["starters"]:
            Threepp = float(starter["3P%"])
            StarterThreepps.append(Threepp)
            Threep = int(starter["3P"])
            StarterThreeps.append(Threep)
            Fg = int(starter["FG"])
            StarterFgs.append(Fg)
            Fgp = float(starter["FG%"])
            StarterFgps.append(Fgp)
            Pts = int(starter["PTS"])
            StarterPtss.append(Pts)
            Votes = int(starter["ASV"])
            StarterVotess.append(Votes)
        Threeps[0].append(StarterThreeps[0])
        Threeps[1].append(StarterThreeps[1])
        Threeps[2].append(StarterThreeps[2])
        Threeps[3].append(StarterThreeps[3])
        Threeps[4].append(StarterThreeps[4])
        Threepps[0].append(StarterThreepps[0])
        Threepps[1].append(StarterThreepps[1])
        Threepps[2].append(StarterThreepps[2])
        Threepps[3].append(StarterThreepps[3])
        Threepps[4].append(StarterThreepps[4])
        Fgs[0].append(StarterFgs[0])
        Fgs[1].append(StarterFgs[1])
        Fgs[2].append(StarterFgs[2])
        Fgs[3].append(StarterFgs[3])
        Fgs[4].append(StarterFgs[4])
        Fgps[0].append(StarterFgps[0])
        Fgps[1].append(StarterFgps[1])
        Fgps[2].append(StarterFgps[2])
        Fgps[3].append(StarterFgps[3])
        Fgps[4].append(StarterFgps[4])
        Ptss[0].append(StarterPtss[0])
        Ptss[1].append(StarterPtss[1])
        Ptss[2].append(StarterPtss[2])
        Ptss[3].append(StarterPtss[3])
        Ptss[4].append(StarterPtss[4])
        Votess[0].append(StarterVotess[0])
        Votess[1].append(StarterVotess[1])
        Votess[2].append(StarterVotess[2])
        Votess[3].append(StarterVotess[3])
        Votess[4].append(StarterVotess[4])

    x_4 = np.nan_to_num(np.array(Threeps[0]))
    x_5 = np.nan_to_num(np.array(Fgs[0]))
    x_6 = np.nan_to_num(np.array(Fgps[0]))
    x_7 = np.nan_to_num(np.array(Ptss[0]))
    x_8 = np.nan_to_num(np.array(Threeps[1]))
    x_9 = np.nan_to_num(np.array(Fgs[1]))
    x_10 = np.nan_to_num(np.array(Fgps[1]))
    x_11 = np.nan_to_num(np.array(Ptss[1]))
    x_12 = np.nan_to_num(np.array(Threeps[2]))
    x_13 = np.nan_to_num(np.array(Fgs[2]))
    x_14 = np.nan_to_num(np.array(Fgps[2]))
    x_15 = np.nan_to_num(np.array(Ptss[2]))
    x_16 = np.nan_to_num(np.array(Threeps[3]))
    x_17 = np.nan_to_num(np.array(Fgs[3]))
    x_18 = np.nan_to_num(np.array(Fgps[3]))
    x_19 = np.nan_to_num(np.array(Ptss[3]))
    x_20 = np.nan_to_num(np.array(Threeps[4]))
    x_21 = np.nan_to_num(np.array(Fgs[4]))
    x_22 = np.nan_to_num(np.array(Fgps[4]))
    x_23 = np.nan_to_num(np.array(Ptss[4]))
    x_24 = np.nan_to_num(np.array(Votess[0]))
    x_25 = np.nan_to_num(np.array(Votess[1]))
    x_26 = np.nan_to_num(np.array(Votess[2]))
    x_27 = np.nan_to_num(np.array(Votess[3]))
    x_28 = np.nan_to_num(np.array(Votess[4]))
    x_29 = np.nan_to_num(np.array(Threepps[0]))
    x_30 = np.nan_to_num(np.array(Threepps[1]))
    x_31 = np.nan_to_num(np.array(Threepps[2]))
    x_32 = np.nan_to_num(np.array(Threepps[3]))
    x_33 = np.nan_to_num(np.array(Threepps[4]))

# x_23 Day of the week

with open(year_data, "r") as f:
    data = json.load(f)
    days = []
    for i in data:
        day = i["dayOfWeek"]
        if day == "Monday":
            days.append(0)
        elif day == "Tuesday":
            days.append(1)
        elif day == "Wednesday":
            days.append(2)
        elif day == "Thursday":
            days.append(3)
        elif day == "Friday":
            days.append(4)
        elif day == "Saturday":
            days.append(5)
        elif day == "Sunday":
            days.append(6)
    x_34 = np.array(days)

# x_24 Time of day
with open(year_data, "r") as f:
    data = json.load(f)
    times = []
    for i in data:
        time = i["dateTime"].split(" ")[1].split(":")[0]
        times.append(int(time))
    x_35 = np.array(times)


# x_26+ opponent starter stats
with open(year_data, "r") as f:
    data = json.load(f)
    Threeps = [[], [], [], [], []]
    Threepps = [[], [], [], [], []]
    Fgs = [[], [], [], [], []]
    Fgps = [[], [], [], [], []]
    Ptss = [[], [], [], [], []]
    Votess = [[], [], [], [], []]
    for game in data:
        StarterThreeps = []
        StarterThreepps = []
        StarterFgs = []
        StarterFgps = []
        StarterPtss = []
        StarterVotess = []
        for starter in game["opponent"]["starters"]:
            Threepp = float(starter["3P%"])
            StarterThreepps.append(Threepp)
            Threep = int(starter["3P"])
            StarterThreeps.append(Threep)
            Fg = int(starter["FG"])
            StarterFgs.append(Fg)
            Fgp = float(starter["FG%"])
            StarterFgps.append(Fgp)
            Pts = int(starter["PTS"])
            StarterPtss.append(Pts)
            Votes = int(starter["ASV"])
            StarterVotess.append(Votes)
        Threeps[0].append(StarterThreeps[0])
        Threeps[1].append(StarterThreeps[1])
        Threeps[2].append(StarterThreeps[2])
        Threeps[3].append(StarterThreeps[3])
        Threeps[4].append(StarterThreeps[4])
        Threepps[0].append(StarterThreepps[0])
        Threepps[1].append(StarterThreepps[1])
        Threepps[2].append(StarterThreepps[2])
        Threepps[3].append(StarterThreepps[3])
        Threepps[4].append(StarterThreepps[4])
        Fgs[0].append(StarterFgs[0])
        Fgs[1].append(StarterFgs[1])
        Fgs[2].append(StarterFgs[2])
        Fgs[3].append(StarterFgs[3])
        Fgs[4].append(StarterFgs[4])
        Fgps[0].append(StarterFgps[0])
        Fgps[1].append(StarterFgps[1])
        Fgps[2].append(StarterFgps[2])
        Fgps[3].append(StarterFgps[3])
        Fgps[4].append(StarterFgps[4])
        Ptss[0].append(StarterPtss[0])
        Ptss[1].append(StarterPtss[1])
        Ptss[2].append(StarterPtss[2])
        Ptss[3].append(StarterPtss[3])
        Ptss[4].append(StarterPtss[4])
        Votess[0].append(StarterVotess[0])
        Votess[1].append(StarterVotess[1])
        Votess[2].append(StarterVotess[2])
        Votess[3].append(StarterVotess[3])
        Votess[4].append(StarterVotess[4])

    x_36 = np.nan_to_num(np.array(Threeps[0]))
    x_37 = np.nan_to_num(np.array(Fgs[0]))
    x_38 = np.nan_to_num(np.array(Fgps[0]))
    x_39 = np.nan_to_num(np.array(Ptss[0]))
    x_40 = np.nan_to_num(np.array(Threeps[1]))
    x_41 = np.nan_to_num(np.array(Fgs[1]))
    x_42 = np.nan_to_num(np.array(Fgps[1]))
    x_43 = np.nan_to_num(np.array(Ptss[1]))
    x_44 = np.nan_to_num(np.array(Threeps[2]))
    x_45 = np.nan_to_num(np.array(Fgs[2]))
    x_46 = np.nan_to_num(np.array(Fgps[2]))
    x_47 = np.nan_to_num(np.array(Ptss[2]))
    x_48 = np.nan_to_num(np.array(Threeps[3]))
    x_49 = np.nan_to_num(np.array(Fgs[3]))
    x_50 = np.nan_to_num(np.array(Fgps[3]))
    x_51 = np.nan_to_num(np.array(Ptss[3]))
    x_52 = np.nan_to_num(np.array(Threeps[4]))
    x_53 = np.nan_to_num(np.array(Fgs[4]))
    x_54 = np.nan_to_num(np.array(Fgps[4]))
    x_55 = np.nan_to_num(np.array(Ptss[4]))
    x_56 = np.nan_to_num(np.array(Votess[0]))
    x_57 = np.nan_to_num(np.array(Votess[1]))
    x_58 = np.nan_to_num(np.array(Votess[2]))
    x_59 = np.nan_to_num(np.array(Votess[3]))
    x_60 = np.nan_to_num(np.array(Votess[4]))
    x_61 = np.nan_to_num(np.array(Threepps[0]))
    x_62 = np.nan_to_num(np.array(Threepps[1]))
    x_63 = np.nan_to_num(np.array(Threepps[2]))
    x_64 = np.nan_to_num(np.array(Threepps[3]))
    x_65 = np.nan_to_num(np.array(Threepps[4]))


# for each value of everything we ne
# coolList = [[x1, x2, ..., x65], for each game...]

with open(year_data, "r") as f:
    data = json.load(f)
    coolList = []

    for index, game in enumerate(data):
        coolList.append(
            [
                x_1[index],
                x_2[index],
                x_3[index],
                x_4[index],
                x_5[index],
                x_6[index],
                x_7[index],
                x_8[index],
                x_9[index],
                x_10[index],
                x_11[index],
                x_12[index],
                x_13[index],
                x_14[index],
                x_15[index],
                x_16[index],
                x_17[index],
                x_18[index],
                x_19[index],
                x_20[index],
                x_21[index],
                x_22[index],
                x_23[index],
                x_24[index],
                x_25[index],
                x_26[index],
                x_27[index],
                x_28[index],
                x_29[index],
                x_30[index],
                x_31[index],
                x_32[index],
                x_33[index],
                x_34[index],
                x_35[index],
                x_36[index],
                x_37[index],
                x_38[index],
                x_39[index],
                x_40[index],
                x_41[index],
                x_42[index],
                x_43[index],
                x_44[index],
                x_45[index],
                x_46[index],
                x_47[index],
                x_48[index],
                x_49[index],
                x_50[index],
                x_51[index],
                x_52[index],
                x_53[index],
                x_54[index],
                x_55[index],
                x_56[index],
                x_57[index],
                x_58[index],
                x_59[index],
                x_60[index],
                x_61[index],
                x_62[index],
                x_63[index],
                x_64[index],
                x_65[index],
            ]
        )


# GET Y VAL

# get attendance vals for season
with open(year_data, "r") as f:
    data = json.load(f)
    attendance = []
    for i in data:
        attendance.append(int(i["attendance"].replace(",", "")))
    y = np.array(attendance)

# Create an instance of the LinearRegression class
reg = LinearRegression()

print(coolList)
# # Fit the model to the data
x = coolList
reg.fit(x, y)

# # Print the coefficients of the model
print(reg.coef_)

# [0.33333333 0.33333333 0.33333333]


# [ 9.83145705e+00  1.31044790e+02  9.09547889e+01 -3.38571634e+02
#  -2.79066760e+02 -2.53317901e+02  7.57512902e+01 -2.92131148e+02
#   7.18397323e+02 -1.09057716e+03 -2.28460693e+02  9.97112200e+01
#  -3.64407602e+01 -1.97111678e+03  1.58658048e+01  3.91223774e+02
#  -2.27480511e+02  4.33261498e+03  9.37152298e-01  4.94205422e+01
#  -6.04115456e+02  1.65472514e+03  1.14251043e+02  1.70379234e-03
#  -1.30005327e-03 -1.77320944e-03 -2.28287970e-03  1.11506368e-03
#   3.14617578e+03  2.13630363e+03  1.45501891e+03 -2.15922480e+03
#   2.47508339e+02  1.19689003e+02 -4.31328750e+02 -1.90584753e+02
#   3.54549681e+02 -2.15801111e+03 -1.51983485e+02  7.82400319e+01
#   7.15600928e+02 -8.51222694e+02 -2.90674539e+02  4.57386073e+00
#   8.88117864e+01 -2.00395780e+03  6.59581359e+01 -8.85854966e+02
#   2.79846740e+02  2.55389370e+03 -1.24008200e+02  1.29726365e+02
#   4.53578007e+02  2.22815523e+03 -2.81796966e+02 -6.51809219e-05
#   3.16680607e-04  4.52456628e-04  9.15500966e-05  1.99051269e-04
#   4.49678491e+03  2.61413175e+02 -3.22412244e+03  1.78914505e+03
#   1.82171767e+03]
