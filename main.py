# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import myfitnesspal
from MFPCreds import name, pw
import datetime as dt


class MFP:

    def __init__(self):
        self.NAME = name
        self.PW = pw
        self.Client = myfitnesspal.Client(self.NAME, password=self.PW)
        self.T = dt.date.today() - dt.timedelta(days=1)
        self.Tminus7 = self.T - dt.timedelta(days=7)

    def getNutritionDictwkAvg(self):
        """ returns an avg/week dict of nutrition like {'calories': 2100, 'carbs': 30, ...}"""
        stat_dict = {}
        for stat in ["calories", "carbs", "fat", "protein"]:
            weekrange = self.Client.get_report(stat, "Nutrition", self.T, self.Tminus7)
            lizt = list(weekrange.values())
            avgWk = round(sum(lizt) / len(lizt))
            stat_dict[stat] = avgWk
        return stat_dict

    def getCardioWkAvg( self ):
        """ returns avg/week kcal from exercise """
        weekrange = self.Client.get_report("Calories Burned", "Fitness", self.T, self.Tminus7)
        lizt = list(weekrange.values())
        avgWk = round(sum(lizt) / len(lizt))
        return avgWk

    def getWeightWkAvg( self ):
        """ returns avg/week kcal from exercise """
        weekrange = self.Client.get_report("Weight", "Progress", self.T, self.Tminus7)
        lizt = list(weekrange.values())
        avgWk = round(sum(lizt) / len(lizt))
        return avgWk

    def cardioToSteps(self):
        """ returns avg/week step count estimate """
        return self.getCardioWkAvg()/0.03
    # def get_measurements(
    #         self,
    #         measurement="Weight",
    #         lower_bound: Optional[datetime.date] = None,
    #         upper_bound: Optional[datetime.date] = None,
    # )

    # def get_date(self, *args, **kwargs) -> Day:
    #     """Returns your meal diary for a particular date"""

if __name__ == '__main__':
    print(MFP().getCardioWkAvg()) # 0.03kcal/step

