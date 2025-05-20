# ROI Calculator

Built With - python 3.12

---

## Getting Started

### Installation
```
$ pip install pandas
```

### How to Run
```
$ python calculate_roi.py
```


### Terminal Output
``` terminaloutput
{
  "Joe": {
    "Round1": {
      "first_deposit_date": "2024-05-01",
      "total_investment": "$1000.00",
      "share_percentage": "21.51%",
      "final_asset_value": "$4301.05",
      "roi": "330.10%",
      "transaction_log": [
        {
          "type": "deposit",
          "amount": 1000,
          "date": "2024-05-01",
          "transaction_id": 1
        }
      ]
    }
  },
  "Bob": {
    "Round1": {
      "first_deposit_date": "2024-05-05",
      "total_investment": "$2000.00",
      "share_percentage": "35.84%",
      "final_asset_value": "$7168.41",
      "roi": "258.42%",
      "transaction_log": [
        {
          "type": "deposit",
          "amount": 2000,
          "date": "2024-05-05",
          "transaction_id": 2
        }
      ]
    },
    "Round2": {
      "first_deposit_date": "2024-05-15",
      "total_investment": "$1000.00",
      "share_percentage": "2.26%",
      "final_asset_value": "$451.26",
      "roi": "15.13%",
      "transaction_log": [
        {
          "type": "deposit",
          "amount": 1000,
          "date": "2024-05-15",
          "transaction_id": 3
        },
        {
          "type": "withdrawal",
          "amount": 300,
          "date": "2024-05-17",
          "transaction_id": 5
        },
        {
          "type": "withdrawal",
          "amount": 400,
          "date": "2024-05-19",
          "transaction_id": 6
        }
      ]
    }
  },
  "Alice": {
    "Round1": {
      "first_deposit_date": "2024-05-10",
      "total_investment": "$3000.00",
      "share_percentage": "34.41%",
      "final_asset_value": "$6881.68",
      "roi": "129.39%",
      "transaction_log": [
        {
          "type": "deposit",
          "amount": 3000,
          "date": "2024-05-10",
          "transaction_id": 4
        }
      ]
    },
    "Round2": {
      "first_deposit_date": "2024-05-15",
      "total_investment": "$5000.00",
      "share_percentage": "5.99%",
      "final_asset_value": "$1197.60",
      "roi": "23.95%",
      "transaction_log": [
        {
          "type": "deposit",
          "amount": 4000,
          "date": "2024-05-15",
          "transaction_id": 7
        },
        {
          "type": "withdrawal",
          "amount": 5000,
          "date": "2024-05-17",
          "transaction_id": 7
        },
        {
          "type": "deposit",
          "amount": 1000,
          "date": "2024-05-18",
          "transaction_id": 8
        }
      ]
    }
  }
}
```

---

## English Version

### Overview

This Python script calculates the Return on Investment (ROI) for multiple investors across different investment rounds. It processes transaction data (deposits and withdrawals) and account value data (USDT balance and unrealized PnL) from CSV files to determine each investor's proportional share of the total account value and their ROI.

### How It Works

1. **Data Loading**:
   - The script reads `transaction_data.csv` and `account_value_data.csv` from the same directory.
   - Dates in both files are converted to datetime format for processing.

2. **Account Value Calculation**:
   - The total account value is computed as the sum of the USDT balance and unrealized profit and loss (PnL).
   - The final account value is taken from the latest date in the account value data.

3. **Transaction Processing**:
   - Transactions are grouped by investor and round.
   - **Deposits** (negative amounts in the data) are processed to calculate a weighted investment based on the account value at the time of investment.
   - **Withdrawals** (positive amounts) reduce the investor’s weighted investment, redistributing the reduced share proportionally among other investors.

4. **ROI Calculation**:
   - The final asset value for each investor-round is determined by their share of the total weighted investment applied to the final account value.
   - ROI is calculated with the formula:
     - ROI = (final asset value - total investment + total withdrawal) / total investment × 100
    
5. **Output**:
   - Results are formatted as a JSON dictionary, detailing each investor’s rounds with total investment, share percentage, final asset value, ROI, and transaction logs.

### Example Output

The script outputs results for investors Joe, Bob, and Alice. Below is a summary of the provided output:

- **Joe**:
  - **Round1**: Invested \$1000 on 2024-05-01, share percentage 21.51%, final asset value \$4301.05, ROI 330.10%.
- **Bob**:
  - **Round1**: Invested \$2000 on 2024-05-05, share percentage 35.84%, final asset value \$7168.41, ROI 258.42%.
  - **Round2**: Invested \$1000 on 2024-05-15, withdrew \$300 and \$400 later, share percentage 2.26%, final asset value \$451.26, ROI 15.13%.
- **Alice**:
  - **Round1**: Invested \$3000 on 2024-05-10, share percentage 34.41%, final asset value \$6881.68, ROI 129.39%.
  - **Round2**: Invested \$5000 total (including a \$4000 deposit, \$5000 withdrawal, and \$1000 deposit), share percentage 5.99%, final asset value \$1197.60, ROI 23.95%.


### Summary

This method fairly distributes returns by considering the timing of investments and account growth.

- Early investors benefit from more time for account growth, so their ROI may be higher.
- Those who invest later, when the account has already grown significantly, or withdraw funds, have a reduced share.
- This approach goes beyond simply tracking "who invested how much" by factoring in "when they invested and how much their money contributed," resulting in a more accurate calculation of returns.

---

## 한글 버전

### 개요

이 파이썬 스크립트는 여러 투자자의 다양한 투자 라운드에 대한 투자 수익률(ROI)을 계산합니다. CSV 파일에서 거래 데이터(입금 및 출금)와 계정 가치 데이터(USDT 잔액 및 미실현 손익)를 처리하여 각 투자자의 총 계정 가치에 대한 비례 지분과 ROI를 계산합니다.

### 작동 방식

1. **데이터 로딩**:
   - 스크립트는 동일한 디렉토리에서 `transaction_data.csv`와 `account_value_data.csv`를 읽습니다.
   - 두 파일의 날짜는 처리하기 쉽도록 datetime 형식으로 변환됩니다.

2. **계정 가치 계산**:
   - 총 계정 가치는 USDT 잔액과 미실현 손익(PnL)의 합으로 계산됩니다.
   - 최종 계정 가치는 계정 가치 데이터의 가장 최근 날짜에서 가져옵니다.

3. **거래 처리**:
   - 거래는 투자자와 라운드별로 그룹화됩니다.
   - **입금**(데이터에서 음수 금액)은 투자 시점의 계정 가치를 기준으로 가중 투자 금액을 계산합니다.
   - **출금**(양수 금액)은 투자자의 가중 투자 금액을 줄이고, 감소된 지분을 다른 투자자들에게 비례적으로 재분배합니다.

4. **ROI 계산**:
   - 각 투자자-라운드의 최종 자산 가치는 총 가중 투자에 대한 지분을 최종 계정 가치에 적용하여 계산됩니다.
   - ROI는 다음 공식으로 계산됩니다:
     - ROI = (최종 자산 가치 - 총 투자 금액 + 총 출금 금액) / 총 투자 금액 × 100
     
5. **출력**:
   - 결과는 JSON 딕셔너리로 형식화되며, 각 투자자의 라운드별 총 투자 금액, 지분 비율, 최종 자산 가치, ROI 및 거래 로그를 자세히 보여줍니다.

### 예시 출력

스크립트는 Joe, Bob, Alice의 결과를 출력합니다. 제공된 출력의 요약은 다음과 같습니다:

- **Joe**:
  - **Round1**: 2024-05-01에 \$1000 투자, 지분 비율 21.51%, 최종 자산 가치 \$4301.05, ROI 330.10%.
- **Bob**:
  - **Round1**: 2024-05-05에 \$2000 투자, 지분 비율 35.84%, 최종 자산 가치 \$7168.41, ROI 258.42%.
  - **Round2**: 2024-05-15에 \$1000 투자, 이후 \$300 및 \$400 출금, 지분 비율 2.26%, 최종 자산 가치 \$451.26, ROI 15.13%.
- **Alice**:
  - **Round1**: 2024-05-10에 \$3000 투자, 지분 비율 34.41%, 최종 자산 가치 \$6881.68, ROI 129.39%.
  - **Round2**: 총 \$5000 투자(\$4000 입금, \$5000 출금, \$1000 입금 포함), 지분 비율 5.99%, 최종 자산 가치 \$1197.60, ROI 23.95%.

### 정리

이 방식은 투자 시점과 계좌 성장을 고려해서 공정하게 나누는 방법입니다.

- 일찍 투자한 사람은 계좌가 더 많이 성장할 시간적 이점이 있으니 ROI가 높을 수 있습니다.
- 이미 계좌가 많이 성장한 시점에 투자하거나, 돈을 뺀 사람은 그만큼 덜 반영됩니다.
- 이렇게 하면 단순히 "누가 얼마 넣었나"가 아니라 "언제 넣었고, 그 돈이 얼마나 기여했나"를 반영해서 더 정확한 수익률을 알 수 있습니다.