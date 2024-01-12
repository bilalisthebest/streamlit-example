import streamlit as st

# IN & F rates
insurance_rates = {
    (5000, 10000.1): {3: 0.025, 6: 0.035, 9: 0.045, 12: 0.05},
    (10001, 20000.1): {3: 0.035, 6: 0.055, 9: 0.065, 12: 0.08},
    (20001, 30000.1): {3: 0.035, 6: 0.055, 9: 0.065, 12: 0.07},
    (30001, 40000.1): {3: 0.035, 6: 0.055, 9: 0.075, 12: 0.08},
    (40001, 50000.1): {3: 0.035, 6: 0.055, 9: 0.075, 12: 0.08},
    (50001, 60000.1): {3: 0.035, 6: 0.055, 9: 0.075, 12: 0.08},
    (60001, 70000.1): {3: 0.045, 6: 0.055, 9: 0.085, 12: 0.09},
    (70001, 80000.1): {3: 0.045, 6: 0.075, 9: 0.095, 12: 0.11},
    (80001, 100000.1): {3: 0.055, 6: 0.085, 9: 0.105, 12: 0.12},
    (100001, 200000.1): {3: 0.075, 6: 0.115, 9: 0.135, 12: 0.16},
    (200001, 300000.1): {3: 0.085, 6: 0.125, 9: 0.145, 12: 0.16},
    (300001, 400000.1): {3: 0.085, 6: 0.125, 9: 0.145, 12: 0.16},
    (400001, 1000000): {3: 0.085, 6: 0.125, 9: 0.145, 12: 0.16}
}

financing_fee_rates = {
    "B2B": {3: 0.075, 6: 0.15, 9: 0.225, 12: 0.30},
    "General": {3: 0.075, 6: 0.15, 9: 0.225, 12: 0.30},
    "Website": {3: 0.075, 6: 0.15, 9: 0.225, 12: 0.30},
    "Telenor": {3: 0.075, 6: 0.15, 9: 0.225, 12: 0.30},
    "Jazz": {3: 0.075, 6: 0.15, 9: 0.225, 12: 0.30},
    "Ufone": {3: 0.075, 6: 0.15, 9: 0.225, 12: 0.30}
}

# Function to calculate monthly installment, revenue, cost, profit, and ROI
def calculate_monthly_installment(Unit_price, Down_payment_percentage, Financing_type, Divide_Insurance, Divide_Processing_Fee, Divide_Weekly):
    results = []

    for tenure in [3, 6, 9, 12]:
        # Divide_Insurance and Divide_Processing_Fee
        monthly_insurance_amount = 0
        monthly_processing_fee = 0

        insurance_rate = 0

        # Find IN rates
        for price_range, rate_map in insurance_rates.items():
            lower_range, upper_range = price_range
            if lower_range <= Unit_price <= upper_range:
                if tenure in rate_map:
                    insurance_rate = rate_map[tenure]
                    break

        # Calculate insurance_amount
        insurance_amount = insurance_rate * Unit_price

        # Calculate processing_fee
        processing_fee = 0.025 * Unit_price

        # Calculate remaining amount
        remaining_amount = Unit_price - (Down_payment_percentage / 100 * Unit_price)

        # Calculate financing_fee
        financing_fee = financing_fee_rates[Financing_type][tenure]
        financing_fee_amount = remaining_amount * financing_fee
        monthly_financing_fee = financing_fee_amount / tenure

        # Divide insurance and processing fee by Tenure if selected
        if Divide_Insurance:
            monthly_insurance_amount = insurance_amount / tenure
        if Divide_Processing_Fee:
            monthly_processing_fee = processing_fee / tenure

        # Calculate total advance cost
        total_advance_cost = 0

    
        # Divide monthly installment by 4 if selected
        if Divide_Weekly:
            weekly_installment = installment / 4
        else:
            weekly_installment = None

        # Calculate total cost of ownership
        total_cost_of_ownership = (installment * tenure) + total_advance_cost

        results.append((tenure, total_advance_cost, installment, total_cost_of_ownership))

    return results

# Streamlit app main function
def main():
    # Set the title
    st.title("Financing Calculator")

    # Input
    Unit_price = st.number_input("Unit price", min_value=None, value=None, step=1.0)
    Financing_type = st.selectbox("Select financing type", ("B2B", "General", "Telenor", "Jazz", "Ufone"))
    Down_payment_percentage = st.number_input("Down payment percentage", min_value=0, max_value=100, value=None)
    Divide_Insurance = st.checkbox("Divide insurance by tenure?")
    Divide_Processing_Fee = st.checkbox("Divide processing fee by tenure?")
    Divide_Weekly = st.checkbox("Divide monthly installment on a weekly basis?")

    # Calculate button
    if st.button("Calculate"):
        st.write(f"### Results for {Financing_type} Financing")

        # Display results for each tenure
        results = calculate_monthly_installment(
            Unit_price, Down_payment_percentage, Financing_type, Divide_Insurance, Divide_Processing_Fee, Divide_Weekly
        )

        for result in results:
            (tenure, total_advance_cost, installment, total_cost_of_ownership) = result

            # Total Advance, Monthly Installment, and Total Cost of Ownership in bold and larger font size
            st.write(f"**Tenure: {tenure} months**")
            st.write(f"*Total Advance*: Rs **{total_advance_cost:,.2f}**")
            st.write(f"*Monthly Installment*: Rs **{installment:,.2f}**")
            st.write(f"*Total Cost of Ownership*: Rs **{total_cost_of_ownership:,.2f}**")

if __name__ == "__main__":
    main()
