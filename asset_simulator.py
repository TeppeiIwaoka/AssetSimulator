import numpy as np
import matplotlib.pyplot as plt

def calculate_net_salary(salary, tax_rate):
    """ Calculate the net salary after applying the effective tax rate. """
    return salary * (1 - tax_rate / 100)


def calculate_remaining_income(net_salary, cost_of_living_index, base_cost_of_living_index, living_ratio):
    """ Calculate the remaining income after adjusting for cost of living. """
    return net_salary * (1 - cost_of_living_index / base_cost_of_living_index * living_ratio)


def calculate_assets_over_years(years, remaining_income, investment_rate, annual_return, capital_gains_tax):
    """ Calculate the total assets over a number of years. """
    current_cash = remaining_income * (1 - investment_rate)
    current_investment = remaining_income * investment_rate
    accumulate_investment = current_investment
    total_assets = [current_cash + current_investment]

    for year in range(2, years + 1):
        current_investment *= (1 + annual_return)
        current_investment += remaining_income * investment_rate
        accumulate_investment += remaining_income * investment_rate
        current_cash += remaining_income * (1 - investment_rate)
        total = current_cash + current_investment

        if year == years:
            capital_gain_deduction = (current_investment - accumulate_investment) * capital_gains_tax / 100
            total -= capital_gain_deduction
        total_assets.append(total)

    return total_assets


def plot(assets_over_time):
    line_styles = {
        'Japan': 'solid',
        'USA': 'dashed',
        'UK': (0, (10, 10)),
        'Germany': (0, (3, 1, 1, 1)),  # dash-dot style
        'France': (0, (5, 10))  # loosely dashed style
    }

    plt.figure(figsize=(12, 8))
    for country, assets in assets_over_time.items():
        plt.plot(range(0, years + 1), [0] + assets, label=country, linestyle=line_styles[country])

    plt.title(f'Asset Progression Over {years} Years (By Country) - After Cash Conversion')
    plt.xlabel('Years')
    plt.ylabel('Total Assets (Yen)')
    plt.xticks(range(0, years + 1))
    plt.yticks(np.arange(0, max([max(assets) for assets in assets_over_time.values()]) + 20000000, 20000000))
    plt.grid(True)
    plt.legend()
    plt.savefig('assets_over_time.png')

# Data
countries_data = {
    'Japan': {'salary': 12595032, 'cost_of_living_index': 43.6, 'effective_tax_rate': 13.9, 'capital_gains_tax': 20.3},
    'USA': {'salary': 35672530, 'cost_of_living_index': 60.3, 'effective_tax_rate': 20.0, 'capital_gains_tax': 25.3},
    'UK': {'salary': 16852080, 'cost_of_living_index': 46.6, 'effective_tax_rate': 28.3, 'capital_gains_tax': 20.0},
    'Germany': {'salary': 15395955, 'cost_of_living_index': 45.3, 'effective_tax_rate': 11.9, 'capital_gains_tax': 26.4},
    'France': {'salary': 11057120, 'cost_of_living_index': 47.5, 'effective_tax_rate': 12.4, 'capital_gains_tax': 30.0}
}

# Simulation parameters
years = 30
investment_rate = 0.30
annual_return = 0.05
actual_cost_of_living_ratio_in_japan = 0.60
base_cost_of_living_index = countries_data['Japan']['cost_of_living_index']

# Calculate assets over time for each country
assets_over_time = {}
for country, data in countries_data.items():
    net_salary = calculate_net_salary(data['salary'], data['effective_tax_rate'])
    remaining_income = calculate_remaining_income(net_salary, data['cost_of_living_index'], base_cost_of_living_index, actual_cost_of_living_ratio_in_japan)
    assets = calculate_assets_over_years(years, remaining_income, investment_rate, annual_return, data['capital_gains_tax'])
    assets_over_time[country] = assets

# Plot
plot(assets_over_time)
