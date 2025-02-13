# Disclaimer: This code is a rough approximation and does not account for
# actual tax brackets, new 401(k) limits, etc.

def financial_projection(
    current_gross_per_paycheck,
    current_net_per_paycheck,
    num_pay_periods=26,
    raise_percent=6.0,
    additional_annual_amount=11456.0
):
    """
    Approximates the change in take-home pay given:
    - current gross and net per paycheck
    - number of pay periods (default=26 bi-weekly)
    - percentage raise
    - additional annual amount (e.g., bonus or new compensation)
    """
    # 1. Current take-home percentage
    current_take_home_ratio = current_net_per_paycheck / current_gross_per_paycheck
    current_take_home_percent = current_take_home_ratio * 100
    
    # 2. Calculate current annual gross
    old_annual_gross = current_gross_per_paycheck * num_pay_periods
    
    # 3. Apply raise
    new_annual_gross_after_raise = old_annual_gross * (1 + raise_percent / 100.0)
    
    # 4. Add additional annual amount
    final_annual_gross = new_annual_gross_after_raise + additional_annual_amount
    
    # 5. Estimate new net by using the same ratio (rough guess)
    approximate_new_annual_net = final_annual_gross * current_take_home_ratio
    approximate_new_net_per_paycheck = approximate_new_annual_net / num_pay_periods
    
    return {
        "current_take_home_percent": current_take_home_percent,
        "old_annual_gross": old_annual_gross,
        "new_annual_gross_after_raise": new_annual_gross_after_raise,
        "final_annual_gross": final_annual_gross,
        "approximate_new_annual_net": approximate_new_annual_net,
        "approximate_new_net_per_paycheck": approximate_new_net_per_paycheck
    }

# Example usage:
current_gross = 4556.24
current_net   = 1923.43

results = financial_projection(
    current_gross_per_paycheck=current_gross,
    current_net_per_paycheck=current_net,
    num_pay_periods=26,
    raise_percent=6.0,
    additional_annual_amount=11456.0
)

# Print the results
print("Current Take-Home Percentage: {:.2f}%".format(results["current_take_home_percent"]))
print("Old Annual Gross: ${:,.2f}".format(results["old_annual_gross"]))
print("New Annual Gross After 6% Raise: ${:,.2f}".format(results["new_annual_gross_after_raise"]))
print("Final Annual Gross (adding $11,456): ${:,.2f}".format(results["final_annual_gross"]))
print("Approx. New Annual Net (guess): ${:,.2f}".format(results["approximate_new_annual_net"]))
print("Approx. New Net Per Paycheck (guess): ${:,.2f}".format(results["approximate_new_net_per_paycheck"]))
