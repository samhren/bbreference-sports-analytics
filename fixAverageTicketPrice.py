import pandas as pd


data = pd.read_csv("data/previousData/cavs_avg_ticket_price_by_section.csv")

newDataframe = pd.DataFrame(
    columns=[
        "Season",
        "EventName",
        "EventDate",
        "Club",
        "Floor",
        "Lower Bowl",
        "Mezzanine",
        "Upper Bowl",
    ]
)


for index, row in data.iterrows():
    if (
        (newDataframe["EventName"] == row["EventName"])
        & (newDataframe["EventDate"] == row["EventDate"])
    ).any():

        newDfIndex = newDataframe[
            (newDataframe["EventName"] == row["EventName"])
            & (newDataframe["EventDate"] == row["EventDate"])
        ].index.tolist()

        if len(newDfIndex) > 1:
            print("Error")
            quit()

        newDfIndex = newDfIndex[0]

        newDataframe.at[newDfIndex, row["Section"]] = row["AverageTicketPrice"]

    else:
        typea = row["Section"]

        if typea == "Club":
            newDataframe = newDataframe.append(
                {
                    "Season": row["Season"],
                    "EventName": row["EventName"],
                    "EventDate": row["EventDate"],
                    "Club": row["AverageTicketPrice"],
                    "Floor": -1,
                    "Lower Bowl": -1,
                    "Mezzanine": -1,
                    "Upper Bowl": -1,
                },
                ignore_index=True,
            )
        elif typea == "Floor":
            newDataframe = newDataframe.append(
                {
                    "Season": row["Season"],
                    "EventName": row["EventName"],
                    "EventDate": row["EventDate"],
                    "Club": -1,
                    "Floor": row["AverageTicketPrice"],
                    "Lower Bowl": -1,
                    "Mezzanine": -1,
                    "Upper Bowl": -1,
                },
                ignore_index=True,
            )
        elif typea == "Lower Bowl":
            newDataframe = newDataframe.append(
                {
                    "Season": row["Season"],
                    "EventName": row["EventName"],
                    "EventDate": row["EventDate"],
                    "Club": -1,
                    "Floor": -1,
                    "Lower Bowl": row["AverageTicketPrice"],
                    "Mezzanine": -1,
                    "Upper Bowl": -1,
                },
                ignore_index=True,
            )
        elif typea == "Mezzanine":
            newDataframe = newDataframe.append(
                {
                    "Season": row["Season"],
                    "EventName": row["EventName"],
                    "EventDate": row["EventDate"],
                    "Club": -1,
                    "Floor": -1,
                    "Lower Bowl": -1,
                    "Mezzanine": row["AverageTicketPrice"],
                    "Upper Bowl": -1,
                },
                ignore_index=True,
            )
        elif typea == "Upper Bowl":
            newDataframe = newDataframe.append(
                {
                    "Season": row["Season"],
                    "EventName": row["EventName"],
                    "EventDate": row["EventDate"],
                    "Club": -1,
                    "Floor": -1,
                    "Lower Bowl": -1,
                    "Mezzanine": -1,
                    "Upper Bowl": row["AverageTicketPrice"],
                },
                ignore_index=True,
            )
        else:
            print("Error")

newDataframe.to_csv("data/previousData/cavs_avg_ticket_price_by_section_fixed.csv")
