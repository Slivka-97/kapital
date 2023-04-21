from datetime import datetime

from .serializer import CalculateSerializer


class Calculate:

    @staticmethod
    def calculate_investment_sum(data):
        return 1

    @staticmethod
    def calculate_sum_rent(data):
        """difficult percent"""
        serializer = CalculateSerializer(data=data)
        if not serializer.is_valid():
            return {'error': data.errors}
        data = serializer.data
        mount_intensity_invest = data['period_intensity_invest'] * 12

        rever_sum_invest_mount = ((data['initial_sum'] / 100) * (data['annual_return_investment'] / 12))
        balance = data['initial_sum'] + rever_sum_invest_mount
        balance_with_invest = balance + data['investment_sum']

        for _ in range(1, mount_intensity_invest):
            rever_sum_invest_mount = ((balance_with_invest / 100) * (data['annual_return_investment'] / 12))
            balance_with_invest += data['investment_sum'] + rever_sum_invest_mount

        rest_year = (data['year_achievement_goal'] - data['age'] - data['period_intensity_invest']) * 12
        for _ in range(rest_year):
            rever_sum_invest_mount = ((balance_with_invest / 100) * (data['annual_return_investment'] / 12))
            balance_with_invest += rever_sum_invest_mount

        sum_rent_month = ((balance_with_invest / 100) * (data['percent_rent_month'] / 12))

        """eazy percent"""
        # for _ in range(data['period_intensity_invest']):
        #     rever_sum_invest_mount = ((data['initial_sum'] / 100) * data['annual_return_investment'])
        #     balance = data['initial_sum'] + rever_sum_invest_mount
        #     balance_with_invest = balance + (data['investment_sum'] * 12)
        #
        # rest_year = (data['year_achievement_goal'] - data['age'] - data['period_intensity_invest'])
        # for _ in range(rest_year):
        #     rever_sum_invest_mount = ((balance_with_invest / 100) * data['annual_return_investment'])
        #     balance_with_invest += rever_sum_invest_mount
        #
        # sum_rent_month = ((balance_with_invest / 100) * (data['percent_rent_month'] / 12))

        return {'result': round(sum_rent_month, 2)}

    @staticmethod
    def calculate_age_rent(data: dict):
        return 3

    @staticmethod
    def calculate_invest_year(data: dict):
        return 4


