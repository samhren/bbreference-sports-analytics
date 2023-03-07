from sklearn.linear_model import LinearRegression
import numpy as np
import json
import csv

START_SEASONS = 2010
END_SEASONS = 2023


class LinearRegression:
    def __init__(self, targetYear):
        if not targetYear >= 2010 or not targetYear <= 2022:
            raise ValueError("Target year is invalid")

        self.targetYear = targetYear
        self.prevYear = targetYear - 1

        self.trainModel()

    def trainModel(self):
        for year in range(START_SEASONS, END_SEASONS - 1):
            with open("data/perData/" + str(year) + ".csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    print(row)
