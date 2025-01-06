def calculate_borrowing_capacity(
    annual_income,
    other_income,
    monthly_expenses,
    other_loan_payments,
    credit_card_limits,
    dependents,
    interest_rate=7.0,  # Current assessment rate as of 2024
    loan_term_years=30
):
    """
    Calculate home loan borrowing capacity based on Australian lending criteria.
    
    Parameters:
    annual_income (float): Total annual income before tax
    other_income (float): Annual other income (rental, investments etc.)
    monthly_expenses (float): Total monthly living expenses
    other_loan_payments (float): Monthly payments for other loans
    credit_card_limits (float): Total credit card limits
    dependents (int): Number of dependents
    interest_rate (float): Annual interest rate (default 7.0%)
    loan_term_years (int): Loan term in years (default 30)
    
    Returns:
    dict: Containing borrowing capacity and key financial metrics
    """
    # Monthly income calculation
    total_annual_income = annual_income + other_income
    monthly_income = total_annual_income / 12
    
    # Basic living expenses based on number of dependents
    base_living_cost = 2500  # Base living cost for single person
    dependent_cost = 500  # Additional cost per dependent
    estimated_living_cost = base_living_cost + (dependent_cost * dependents)
    
    # Use higher of declared or estimated living expenses
    total_living_expenses = max(monthly_expenses, estimated_living_cost)
    
    # Credit card commitments (3% of total limits as per bank policies)
    credit_card_commitments = credit_card_limits * 0.03
    
    # Total monthly commitments
    total_monthly_commitments = (
        total_living_expenses +
        other_loan_payments +
        credit_card_commitments
    )
    
    # Calculate disposable monthly income AFTER all commitments
    disposable_income = monthly_income - total_monthly_commitments
    
    # Apply debt service ratio (usually around 30-35% of gross income)
    # But now we need to consider existing commitments
    max_total_debt_payments = monthly_income * 0.35
    
    # Available capacity for mortgage after other commitments
    available_for_mortgage = max_total_debt_payments - (other_loan_payments + credit_card_commitments)
    
    # Ensure available_for_mortgage doesn't go negative
    available_for_mortgage = max(0, available_for_mortgage)
    
    # Calculate maximum loan amount using standard loan formula
    monthly_rate = interest_rate / (12 * 100)
    num_payments = loan_term_years * 12
    
    max_loan = available_for_mortgage * (1 - (1 + monthly_rate)**(-num_payments)) / monthly_rate
    
    # Apply conservative buffer
    max_loan = max_loan * 0.95
    
    return {
        "borrowing_capacity": round(max_loan, 2),
        "monthly_income": round(monthly_income, 2),
        "total_monthly_commitments": round(total_monthly_commitments, 2),
        "disposable_income": round(disposable_income, 2),
        "maximum_monthly_repayment": round(available_for_mortgage, 2),
        "credit_card_commitments": round(credit_card_commitments, 2),
        "total_debt_payments": round(other_loan_payments + credit_card_commitments, 2)
    }

def print_borrowing_report(calculation_result):
    """Print a formatted borrowing capacity report"""
    print("\n=== Borrowing Capacity Report ===")
    print(f"Maximum Borrowing Capacity: ${calculation_result['borrowing_capacity']:,.2f}")
    print(f"\nMonthly Metrics:")
    print(f"Gross Monthly Income: ${calculation_result['monthly_income']:,.2f}")
    print(f"Total Monthly Commitments: ${calculation_result['total_monthly_commitments']:,.2f}")
    print(f"→ Including Debt Payments: ${calculation_result['total_debt_payments']:,.2f}")
    print(f"→ Credit Card Commitments: ${calculation_result['credit_card_commitments']:,.2f}")
    print(f"Disposable Monthly Income: ${calculation_result['disposable_income']:,.2f}")
    print(f"Maximum Monthly Loan Repayment: ${calculation_result['maximum_monthly_repayment']:,.2f}")
    print("\nNote: This is an estimate only. Actual borrowing capacity may vary by lender.")

# Example usage
if __name__ == "__main__":
    # Let's test with different scenarios
    print("\nScenario 1: No existing debts")
    result1 = calculate_borrowing_capacity(
        annual_income=193156,
        other_income=27288,
        monthly_expenses=8088,
        other_loan_payments=0,
        credit_card_limits=0,
        dependents=2
    )
    print_borrowing_report(result1)
    
    print("\nScenario 2: With existing debts")
    result2 = calculate_borrowing_capacity(
        annual_income=193156,
        other_income=27288,
        monthly_expenses=8088,
        other_loan_payments=171,
        credit_card_limits=6000,
        dependents=2
    )
    print_borrowing_report(result2)