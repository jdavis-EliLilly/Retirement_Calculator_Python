def calculate_annual_taxes(income, tax_brackets):
    """
    Calculate the annual taxes based on progressive tax brackets.

    Parameters:
    income (float): Annual income
    tax_brackets (dict): Tax brackets with upper limits and rates

    Returns:
    float: Total tax owed for the year
    """
    tax = 0
    previous_limit = 0

    # Iterate through each tax bracket to calculate the tax owed
    for limit, rate in tax_brackets.items():
        if income > limit:
            tax += (limit - previous_limit) * rate
        else:
            tax += (income - previous_limit) * rate
            break
        previous_limit = limit

    return tax

def retirement_savings_with_taxes(initial_income, years, rate_of_return, inflation, income_growth, max_401k_contribution, tax_brackets):
    """
    Calculate the future value of retirement savings adjusted for taxes, inflation, and income growth.

    Parameters:
    initial_income (float): Initial annual income
    years (int): Number of years until retirement
    rate_of_return (float): Annual rate of return (as a decimal)
    inflation (float): Annual inflation rate (as a decimal)
    income_growth (float): Annual income growth rate (as a decimal)
    max_401k_contribution (float): Maximum annual 401(k) contribution
    tax_brackets (dict): Tax brackets with upper limits and rates

    Returns:
    tuple: Future value of 401(k) and additional savings
    """
    real_rate_of_return = rate_of_return - inflation
    income = initial_income
    total_401k = 0
    total_additional_savings = 0

    # Calculate savings for each year, taking into account taxes, 401(k) contributions, and additional savings
    for year in range(years):
        # Calculate annual taxes
        annual_tax = calculate_annual_taxes(income, tax_brackets)
        after_tax_income = income - annual_tax

        # Calculate 401(k) contribution and its future value
        contribution_401k = min(max_401k_contribution, after_tax_income)
        total_401k = (total_401k + contribution_401k) * (1 + real_rate_of_return)

        # Calculate additional savings beyond 401(k) and its future value
        additional_savings = max(0, after_tax_income - contribution_401k)
        total_additional_savings = (total_additional_savings + additional_savings) * (1 + real_rate_of_return)

        # Increase income for the next year based on income growth rate
        income *= (1 + income_growth)

    return total_401k, total_additional_savings

# Parameters (same as before)
initial_income = 112000
years = 20
rate_of_return = 0.05
inflation = 0.03
income_growth = 0.05
max_401k_contribution = 23000
tax_brackets = {
    11600: 0.10,
    47150: 0.12,
    100525: 0.22,
    191950: 0.24,
    243725: 0.32,
    609350: 0.35,
    float('inf'): 0.37
}

# Calculate future value of retirement savings
total_401k_with_taxes, total_additional_savings_with_taxes = retirement_savings_with_taxes(
    initial_income, years, rate_of_return, inflation, income_growth, max_401k_contribution, tax_brackets
)
