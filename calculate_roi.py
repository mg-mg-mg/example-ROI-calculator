"""
Calculate ROI (Return on Investment) for investors by round

This script reads transaction and account value data from CSV files and calculates
the ROI for each investor (Bob, Joe, Alice) by investment round.

Usage:
    python calculate_roi.py
"""

import pandas as pd
import os

def load_data():
    """Load transaction and account value data from CSV files"""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Load transaction data
    transaction_file = os.path.join(current_dir, 'transaction_data.csv')
    transactions_df = pd.read_csv(transaction_file)

    # Load account value data
    account_value_file = os.path.join(current_dir, 'account_value_data.csv')
    account_values_df = pd.read_csv(account_value_file)

    # Convert date columns to datetime
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    account_values_df['date'] = pd.to_datetime(account_values_df['date'])

    return transactions_df, account_values_df

def calculate_roi_by_round():
    """
    Calculate ROI for each person by investment round

    ROI is calculated by:
    1. Finding the account value at the time of investment
    2. Finding the account value at the end of the period (latest date)
    3. Calculating each investor's share of the total account
    4. Distributing the final account value proportionally based on each investor's share
    5. Calculating ROI based on this projected value and any withdrawals
    """
    # Load data
    transactions_df, account_values_df = load_data()

    # Calculate total account value (USDT balance + unrealized PnL)
    account_values_df['total_value'] = account_values_df['usdt_balance'] + account_values_df['unrealized_pnl']

    # Get the final account value (from the latest date)
    final_account_value = account_values_df.iloc[-1]['total_value']

    # Group transactions by investor and round
    investor_round_data = {}
    transaction_log = {}

    # Process all transactions and create a transaction log
    for _, transaction in transactions_df.iterrows():
        investor = transaction['name']
        round_name = transaction['code']
        amount = transaction['amount']
        date = transaction['date']
        key = f"{investor}_{round_name}"

        # Initialize data structures if needed
        if key not in investor_round_data:
            investor_round_data[key] = {
                'investor': investor,
                'round': round_name,
                'total_investment': 0,
                'total_withdrawal': 0,
                'weighted_investment': 0,
                'first_deposit_date': None
            }

        if key not in transaction_log:
            transaction_log[key] = []

        # Add to transaction log (chronological record of all transactions)
        transaction_log[key].append({
            'type': 'deposit' if amount < 0 else 'withdrawal',
            'amount': abs(amount),
            'date': date,
            'transaction_id': transaction['id']
        })

        # Process deposits (negative amounts)
        if amount < 0:
            # Find the account value on the investment date
            start_idx = account_values_df['date'].searchsorted(date)
            if start_idx >= len(account_values_df):
                start_idx = len(account_values_df) - 1
            start_value = account_values_df.iloc[start_idx]['total_value']

            # Update investment data
            investment_amount = abs(amount)
            investor_round_data[key]['total_investment'] += investment_amount
            investor_round_data[key]['weighted_investment'] += investment_amount / start_value

            # Track first deposit date
            if investor_round_data[key]['first_deposit_date'] is None or date < investor_round_data[key]['first_deposit_date']:
                investor_round_data[key]['first_deposit_date'] = date

        # Process withdrawals (positive amounts)
        else:
            investor_round_data[key]['total_withdrawal'] += amount

    # Calculate the total weighted investment across all investors and rounds
    total_weighted_investment = sum(data['weighted_investment'] for data in investor_round_data.values())

    # Calculate final asset values and ROI for each investor and round
    results = []
    for key, data in investor_round_data.items():
        # Calculate the proportional share of the final account value
        proportional_share = data['weighted_investment'] / total_weighted_investment
        final_asset_value = proportional_share * final_account_value

        # Calculate normalized share percentage (ensures sum equals 100%)
        share_percentage = proportional_share * 100

        # Calculate ROI
        roi = ((final_asset_value - data['total_investment'] + data['total_withdrawal']) / data['total_investment']) * 100

        # Sort transaction log by date
        sorted_transactions = sorted(transaction_log[key], key=lambda x: x['date'])

        result = {
            'investor': data['investor'],
            'round': data['round'],
            'total_investment': data['total_investment'],
            'first_deposit_date': data['first_deposit_date'].strftime('%Y-%m-%d'),
            'share_percentage': share_percentage,
            'final_asset_value': final_asset_value,
            'roi': roi,
            'transaction_log': [{
                'type': t['type'],
                'amount': t['amount'],
                'date': t['date'].strftime('%Y-%m-%d'),
                'transaction_id': t['transaction_id']
            } for t in sorted_transactions]
        }

        results.append(result)

    return results

def main():
    """Main function to calculate and display ROI"""
    results = calculate_roi_by_round()

    # Format results as a dictionary
    formatted_results = {}

    for result in results:
        investor = result['investor']
        round_name = result['round']

        # Create investor entry if it doesn't exist
        if investor not in formatted_results:
            formatted_results[investor] = {}

        # Create a unique key for this investor-round combination
        key = f"{round_name}"

        # Format the result with proper number formatting
        formatted_result = {
            'first_deposit_date': result['first_deposit_date'],
            'total_investment': f"${result['total_investment']:.2f}",
            'share_percentage': f"{result['share_percentage']:.2f}%",
            'final_asset_value': f"${result['final_asset_value']:.2f}",
            'roi': f"{result['roi']:.2f}%",
            'transaction_log': result['transaction_log']
        }

        # Add to formatted results
        formatted_results[investor][key] = formatted_result

    # Print the formatted results as a dictionary
    import json
    print(json.dumps(formatted_results, indent=2))

if __name__ == "__main__":
    main()
