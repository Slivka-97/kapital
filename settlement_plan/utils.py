from datetime import datetime


def get_year_achievement_goal(data: dict):
    current_year = datetime.now().year
    res = None
    if data['investment_purpose']['age_goal_achievement']:
        res = current_year + (data['investment_purpose']['age_goal_achievement'] - data['age'])
    return res


class Calculate:

    @staticmethod
    def calculate_investment_sum(data: dict):
        return 1

    @staticmethod
    def calculate_sum_rent(data: dict):
        return 2

    @staticmethod
    def calculate_age_rent(data: dict):
        return 3

    @staticmethod
    def calculate_invest_year(data: dict):
        return 4


