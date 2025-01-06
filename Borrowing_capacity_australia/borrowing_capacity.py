def calculate_borrowing_capacity(
    annual_income,
    other_income,
    monthly_expenses,
    other_loan_payments,
    credit_card_limits,
    dependents,
    interest_rate=6.11,  # Current assessment rate as of 2024
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
    
    # Calculate disposable monthly income
    disposable_income = monthly_income - total_monthly_commitments
    
    # Apply debt service ratio (usually around 30-35% of gross income)
    max_loan_repayment = monthly_income * 0.35
    
    # Calculate maximum loan amount using standard loan formula
    monthly_rate = interest_rate / (12 * 100)
    num_payments = loan_term_years * 12
    
    max_loan = max_loan_repayment * (1 - (1 + monthly_rate)**(-num_payments)) / monthly_rate
    
    # Apply conservative buffer
    max_loan = max_loan * 0.95
    
    return {
        "borrowing_capacity": round(max_loan, 2),
        "monthly_income": round(monthly_income, 2),
        "total_monthly_commitments": round(total_monthly_commitments, 2),
        "disposable_income": round(disposable_income, 2),
        "maximum_monthly_repayment": round(max_loan_repayment, 2)
    }

# Example usage and report generation
def print_borrowing_report(calculation_result):
    """Print a formatted borrowing capacity report"""
    print("\n=== Borrowing Capacity Report ===")
    print(f"Maximum Borrowing Capacity: ${calculation_result['borrowing_capacity']:,.2f}")
    print(f"\nMonthly Metrics:")
    print(f"Gross Monthly Income: ${calculation_result['monthly_income']:,.2f}")
    print(f"Total Monthly Commitments: ${calculation_result['total_monthly_commitments']:,.2f}")
    print(f"Disposable Monthly Income: ${calculation_result['disposable_income']:,.2f}")
    print(f"Maximum Monthly Loan Repayment: ${calculation_result['maximum_monthly_repayment']:,.2f}")
    print("\nNote: This is an estimate only. Actual borrowing capacity may vary by lender.")

# Example usage
if __name__ == "__main__":
    # Example inputs
    result = calculate_borrowing_capacity(
        annual_income=163156,
        other_income=0,
        monthly_expenses=4130,
        other_loan_payments=0,
        credit_card_limits=0,
        dependents=2
    )
    
    print_borrowing_report(result)