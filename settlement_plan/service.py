from datetime import datetime

from .serializer import CalculateSerializer


class Calculate:
    MONTHS = 12
    FULL_PERCENT = 100
    INITIAL_SUM = 500_000
    INVEST_SUM = 20_000
    DEFAULT_PERCENT = 5

    @staticmethod
    def calculate_investment_sum(data):
        return 1

    def calculate_sum_rent(self, data):
        """difficult percent"""
        serializer = CalculateSerializer(data=data)
        if not serializer.is_valid():
            return {'error': data.errors}
        data = serializer.data
        mount_intensity_invest = data.get('period_intensity_invest', self.MONTHS) * self.MONTHS

        rever_sum_invest_mount = ((data.get('initial_sum', self.INITIAL_SUM) / self.FULL_PERCENT) * (data.get('annual_return_investment', self.DEFAULT_PERCENT) / self.MONTHS))
        balance = data.get('initial_sum', self.INITIAL_SUM) + rever_sum_invest_mount
        balance_with_invest = balance + data.get('investment_sum', self.INVEST_SUM)

        for _ in range(1, mount_intensity_invest):
            rever_sum_invest_mount = ((balance_with_invest / self.FULL_PERCENT) * (data.get('annual_return_investment', self.DEFAULT_PERCENT) / self.MONTHS))
            balance_with_invest += data.get('investment_sum', self.INVEST_SUM) + rever_sum_invest_mount

        rest_year = (data.get('year_achievement_goal', 50) - data.get('age', 0) - data.get('period_intensity_invest', self.MONTHS)) * self.MONTHS
        for _ in range(rest_year):
            rever_sum_invest_mount = ((balance_with_invest / self.FULL_PERCENT) * (data.get('annual_return_investment', self.DEFAULT_PERCENT) / self.MONTHS))
            balance_with_invest += rever_sum_invest_mount

        sum_rent_month = ((balance_with_invest / self.FULL_PERCENT) * (data.get('percent_rent_month', self.DEFAULT_PERCENT) / self.MONTHS))

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


