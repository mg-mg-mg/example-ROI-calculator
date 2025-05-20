"""
Calculate ROI (Return on Investment) for investors by round

This script reads transaction and account value data from CSV files and calculates
the ROI for each investor (Bob, Joe, Alice) by investment round.

Usage:
    python calculate_roi.py
"""

import logging
import os

import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

USDT_BALANCE = 'usdt_balance'
UNREALIZED_PNL = "unrealized_pnl"


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
    logger.info("Loading data for ROI calculation")
    # Load data
    transactions_df, account_values_df = load_data()

    # Calculate total account value (USDT balance + unrealized PnL)
    account_values_df['total_value'] = account_values_df[USDT_BALANCE] + account_values_df[UNREALIZED_PNL]
    logger.info("Calculated total account values")

    # Get the final account value (from the latest date)
    final_account_value = account_values_df.iloc[-1]['total_value']
    logger.info(f"Final account value: ${final_account_value:.2f}")

    # Group transactions by investor and round
    investor_round_data = {}
    transaction_log = {}

    # Group transactions by date to ensure same-day investments use the same start_value and ROI
    date_to_start_value = {}
    date_to_investments = {}

    # First pass: calculate start_value for each unique date and group investments by date
    for _, transaction in transactions_df.iterrows():
        date = transaction['date']
        amount = transaction['amount']
        date_str = date.strftime('%Y-%m-%d')

        # Only process deposits (negative amounts)
        if amount < 0:
            # Calculate start_value for this date if not already done
            if date_str not in date_to_start_value:
                # Find the account value on the investment date
                start_idx = account_values_df['date'].searchsorted(date)
                if start_idx >= len(account_values_df):
                    start_idx = len(account_values_df) - 1
                start_value = account_values_df.iloc[start_idx]['total_value']
                date_to_start_value[date_str] = start_value
                date_to_investments[date_str] = []
                logger.info(f"Date {date_str}: start_value = {start_value:.2f}")

            # Add this investment to the date's investment list
            date_to_investments[date_str].append({
                'investor': transaction['name'],
                'round_name': transaction['code'],
                'amount': abs(amount),
                'transaction_id': transaction['id']
            })

    # Second pass: calculate weighted_investment for each date
    all_dates = sorted(date_to_investments.keys())

    # Calculate weighted investments based on the account value at each investment date
    # This approach ensures that when a new investment is made, the shares are distributed
    # proportionally based on the current account value

    # Initialize variables to track the account values and investments
    date_to_weighted_investment = {}

    for i, date_str in enumerate(all_dates):
        start_value = date_to_start_value[date_str]
        investments = date_to_investments[date_str]

        # Calculate total investment amount for this date
        total_investment_amount = sum(inv['amount'] for inv in investments)

        # For the first date, the account value is just the investment amount
        if i == 0:
            date_to_weighted_investment[date_str] = 1.0
            logger.info(f"Date {date_str}: First investment = {total_investment_amount:.2f}, "
                       f"weighted = 1.0")
        else:
            # For subsequent dates, use the start_value as the current account value
            # This accounts for growth between investments

            # Calculate the new investment's share based on the current account value
            new_investment_share = total_investment_amount / start_value

            # Adjust previous dates' weights to maintain the sum at 1.0
            for prev_date in date_to_weighted_investment:
                date_to_weighted_investment[prev_date] *= (1.0 - new_investment_share)

            # Store the weighted investment for this date
            date_to_weighted_investment[date_str] = new_investment_share

            logger.info(f"Date {date_str}: investment = {total_investment_amount:.2f}, "
                       f"account value before = {start_value:.2f}, "
                       f"account value after = {start_value + total_investment_amount:.2f}, "
                       f"weighted = {new_investment_share:.6f}")

        # Log all dates' weighted investments for debugging
        for d in all_dates:
            if d in date_to_weighted_investment:
                logger.info(f"  - Date {d}: weighted = {date_to_weighted_investment[d]:.6f}")

        # Verify that the sum of all weighted investments is 1.0
        total_weighted = sum(date_to_weighted_investment.values())
        logger.info(f"Total weighted investment: {total_weighted:.6f}")

    # Third pass: process all transactions and create transaction logs
    for _, transaction in transactions_df.iterrows():
        investor = transaction['name']
        round_name = transaction['code']
        amount = transaction['amount']
        date = transaction['date']
        date_str = date.strftime('%Y-%m-%d')
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
            # Update investment data
            investment_amount = abs(amount)
            investor_round_data[key]['total_investment'] += investment_amount

            # Calculate this investor's share of the date's weighted investment
            if date_str in date_to_investments and date_str in date_to_weighted_investment:
                date_total_investment = sum(inv['amount'] for inv in date_to_investments[date_str])
                if date_total_investment > 0:
                    investor_share = investment_amount / date_total_investment
                    investor_weighted = investor_share * date_to_weighted_investment[date_str]
                    investor_round_data[key]['weighted_investment'] += investor_weighted

                    logger.info(f"Investor {investor} ({round_name}) on {date_str}: "
                               f"investment = {investment_amount:.2f}, "
                               f"share = {investor_share:.6f}, "
                               f"weighted = {investor_weighted:.6f}")

            # Track first deposit date
            if investor_round_data[key]['first_deposit_date'] is None or date < investor_round_data[key]['first_deposit_date']:
                investor_round_data[key]['first_deposit_date'] = date

        # Process withdrawals (positive amounts)
        else:
            withdrawal_amount = amount
            investor_round_data[key]['total_withdrawal'] += withdrawal_amount

            # Calculate the proportion of the investor's weighted_investment to reduce
            current_weighted = investor_round_data[key]['weighted_investment']
            if current_weighted > 0:
                # Calculate what percentage of their investment they're withdrawing
                total_invested = investor_round_data[key]['total_investment']
                withdrawal_percentage = min(withdrawal_amount / (total_invested - investor_round_data[key]['total_withdrawal'] + withdrawal_amount), 1.0)

                # Reduce their weighted_investment proportionally
                weighted_reduction = current_weighted * withdrawal_percentage
                investor_round_data[key]['weighted_investment'] -= weighted_reduction

                # Redistribute the reduced weighted_investment among other investors proportionally
                remaining_weighted = sum(data['weighted_investment'] for k, data in investor_round_data.items() if k != key)
                if remaining_weighted > 0:
                    for k, data in investor_round_data.items():
                        if k != key and data['weighted_investment'] > 0:
                            # Increase proportionally to their current weighted_investment
                            data['weighted_investment'] += (data['weighted_investment'] / remaining_weighted) * weighted_reduction

                # Verify that the sum of all weighted investments is still 1.0 after redistribution
                total_after_withdrawal = sum(data['weighted_investment'] for data in investor_round_data.values())
                logger.info(f"Investor {investor} ({round_name}) on {date_str}: "
                           f"withdrawal = {withdrawal_amount:.2f}, "
                           f"withdrawal_percentage = {withdrawal_percentage:.6f}, "
                           f"weighted_reduction = {weighted_reduction:.6f}, "
                           f"new_weighted = {investor_round_data[key]['weighted_investment']:.6f}, "
                           f"total_weighted_after = {total_after_withdrawal:.6f}")

    # Calculate the total weighted investment across all investors and rounds
    total_weighted_investment = sum(data['weighted_investment'] for data in investor_round_data.values())
    logger.info(f"Total weighted investment: {total_weighted_investment:.6f}")

    # Calculate final asset values and ROI for each investor and round
    logger.info("Calculating final asset values and ROI for each investor and round")
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

    logger.info(f"Calculated ROI for {len(results)} investor-round combinations")
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
