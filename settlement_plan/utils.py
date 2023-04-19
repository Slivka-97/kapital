from datetime import datetime


def get_year_achievement_goal(data: dict):
    current_year = datetime.now().year
    res = None
    if data['age_goal_achievement']:
        res = current_year + (data['age_goal_achievement'] - data['age'])
    return res


class Calculate:

    @staticmethod
    def calculate_investment_sum(data):
        period_monthly_invest = data['period_monthly_invest']
        age_goal_achievement = data['age_goal_achievement']
        average_sum = data['average_sum']
        sum_rent_month = data['sum_rent_month']

        # monthly_return = (1 + average_sum) ** (1 / 12) - 1  # ежемесячная доходность
        # months = (age_goal_achievement - period_monthly_invest) * 12  # количество месяцев, в течение которых необходимо инвестировать
        # investment_amount = (sum_rent_month / 0.05) * ((1 + 0.05) ** months - 1) / (
        #             (1 + monthly_return) ** months - 1)  # расчет суммы инвестиций
        # return round(investment_amount, 2)  # возвращаем результат с округлением до 2 знаков после запятой

    @staticmethod
    def calculate_sum_rent(data):
        sum_rent_month = data['sum_rent_month']
        period_monthly_invest = data['period_monthly_invest']
        age_goal_achievement = data['age_goal_achievement']
        average_sum = data['average_sum']
        # переводим годовую доходность и процентную ставку в месячные
        monthly_return = ((1 + average_sum) ** (1 / 12)) - 1
        monthly_interest_rate = 0.5 / 12

        # рассчитываем сумму капитала, который мы накопим к возрасту age
        num_months = (age_goal_achievement - (period_monthly_invest * 12))
        total_capital = 0

        for i in range(period_monthly_invest * 12):
            total_capital += sum_rent_month
        total_capital *= (1 + monthly_return)
        if i % 12 == 0:
            total_capital *= (1 + monthly_interest_rate)

        return round(total_capital, 2)

    @staticmethod
    def calculate_age_rent(data: dict):
        return 3

    @staticmethod
    def calculate_invest_year(data: dict):
        return 4


