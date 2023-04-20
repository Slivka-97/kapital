from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

from settlement_plan.models.investment import Compare


class TestInvestmentPortfolio(APITestCase):

    def setUp(self) -> None:
        """TEST POST PORTFOLIO"""
        user = User.objects.create(username='user', password='1234', is_staff=True)
        user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        data = {
            "currency": "RUB",
            "fact_price": 1000,
            "plan_price": 35
        }
        response = self.client.post(reverse('investment_portfolio_api'), data=data, format='json')
        self.assertEquals(response.status_code, 201)
        data['plan_price'] = 100
        response = self.client.post(reverse('investment_portfolio_api'), data=data, format='json')
        self.assertEquals(response.status_code, 201)

    def test_list_portfolio_api(self):
        response = self.client.get(reverse('investment_portfolio_api'))
        data = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 2)


class TestInvestmentPurposeRecord(APITestCase):

    def setUp(self) -> None:
        """TEST POST Investment Purpose"""
        user = User.objects.create(username='user', password='1234', is_staff=True)
        user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        data = {
            "currency": "RUB",
            "fact_price": 1000,
            "plan_price": 35
        }
        self.investment_sum = 20_000
        response = self.client.post(reverse('investment_portfolio_api'), data=data, format='json')
        self.assertEquals(response.status_code, 201)
        self.data = response.json()

    def _test_post_investment_purpose_investment_sum(self):
        data = {
            "age": 30,
            "period_monthly_invest": 1,
            "start_data_invest": "2023-05-18",
            "age_goal_achievement": 60,
            "average_sum": 21,
            "sum_rent_month": 4,
            'investment_sum': self.investment_sum,
            "investment_portfolio": self.data['id'],
            "other_info": "3eedd"
        }

        response = self.client.post(reverse('investment_purpose_type_invest_record', args=['investment_sum']),
                                    data=data, format='json')
        self.assertEquals(response.status_code, 201)

        response = self.client.get(reverse('compare_api'))
        data = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 12)

    def test_investment_purpose_api_list(self):
        self._test_post_investment_purpose_investment_sum()
        response = self.client.get(reverse('investment_purpose_api'))
        data = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 1)

    def test_compare_api_update_for_id(self):
        self._test_post_investment_purpose_investment_sum()
        data = {
            'monthly_payment_fact': 18_000,
            'data': '2023-06-18',
        }
        response = self.client.put(reverse('compare_update_for_pk_api', kwargs={'pk': 1}), data=data, format='json')
        self.assertEquals(response.status_code, 200)

    def test_compare_api_update(self):
        self._test_post_investment_purpose_investment_sum()
        data = {
            'monthly_payment_fact': 18_000,
            'data': '2023-06-18',
            'purpose': 1
        }
        response = self.client.put(reverse('compare_update_api'), data=data, format='json')
        data = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['invested_funds_fact'], 18_000)

    def test_compare_api_update_with_monthly_payment_fact(self):
        self._test_post_investment_purpose_investment_sum()
        data = {
            'monthly_payment_fact': 18_000,
            'data': '2023-06-18',
            'purpose': 1
        }
        c = Compare.objects.get(id=1)
        c.monthly_payment_fact = 10_000
        c.save()
        response = self.client.put(reverse('compare_update_api'), data=data, format='json')
        data = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['invested_funds_fact'], 28_000) #10+18
