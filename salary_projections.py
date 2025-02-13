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
    
    # 2. Current annual gross
    old_annual_gross = current_gross_per_paycheck * num_pay_periods
    
    # 3. Apply a raise
    new_annual_gross_after_raise = old_annual_gross * (1 + raise_percent / 100.0)
    
    # 4. Add additional annual amount
    final_annual_gross = new_annual_gross_after_raise + additional_annual_amount
    
    # 5. Estimate the new net by using the same ratio (ROUGH GUESS!)
    approximate_new_annual_net = final_annual_gross * current_take_home_ratio
    approximate_new_net_per_paycheck = approximate_new_annual_net / num_pay_periods
    
    # 6. Calculate differences
    old_annual_net = current_net_per_paycheck * num_pay_periods
    
    increase_per_paycheck = approximate_new_net_per_paycheck - current_net_per_paycheck
    increase_per_paycheck_percent = (increase_per_paycheck / current_net_per_paycheck) * 100
    
    increase_annual_net = approximate_new_annual_net - old_annual_net
    increase_annual_net_percent = (increase_annual_net / old_annual_net) * 100
    
    return {
        "current_take_home_percent": current_take_home_percent,
        "old_annual_gross": old_annual_gross,
        "new_annual_gross_after_raise": new_annual_gross_after_raise,
        "final_annual_gross": final_annual_gross,
        "approximate_new_annual_net": approximate_new_annual_net,
        "approximate_new_net_per_paycheck": approximate_new_net_per_paycheck,
        "increase_per_paycheck": increase_per_paycheck,
        "increase_per_paycheck_percent": increase_per_paycheck_percent,
        "increase_annual_net": increase_annual_net,
        "increase_annual_net_percent": increase_annual_net_percent
    }

# Example usage:
current_gross = 4556.24  # Your current gross per paycheck
current_net   = 1923.43  # Your current net per paycheck

results = financial_projection(
    current_gross_per_paycheck=current_gross,
    current_net_per_paycheck=current_net,
    num_pay_periods=26,
    raise_percent=6.0,
    additional_annual_amount=11456.0
)

print("Current Take-Home Percentage: {:.2f}%".format(results["current_take_home_percent"]))
print("Old Annual Gross: ${:,.2f}".format(results["old_annual_gross"]))
print("New Annual Gross After 6% Raise: ${:,.2f}".format(results["new_annual_gross_after_raise"]))
print("Final Annual Gross (adding $11,456): ${:,.2f}".format(results["final_annual_gross"]))
print("Approx. New Annual Net (guess): ${:,.2f}".format(results["approximate_new_annual_net"]))
print("Approx. New Net Per Paycheck (guess): ${:,.2f}".format(results["approximate_new_net_per_paycheck"]))
print("Increase Per Paycheck: ${:,.2f} ({:.2f}%)".format(
    results["increase_per_paycheck"], results["increase_per_paycheck_percent"])
)
print("Annual Net Increase: ${:,.2f} ({:.2f}%)".format(
    results["increase_annual_net"], results["increase_annual_net_percent"])
)
