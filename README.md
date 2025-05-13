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
      "share_percentage": "42.32%",
      "final_asset_value": "$8464.14",
      "roi": "746.41%",
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
      "share_percentage": "26.45%",
      "final_asset_value": "$5290.09",
      "roi": "164.50%",
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
      "share_percentage": "2.56%",
      "final_asset_value": "$512.98",
      "roi": "21.30%",
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
      "share_percentage": "15.87%",
      "final_asset_value": "$3174.05",
      "roi": "5.80%",
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
      "share_percentage": "12.79%",
      "final_asset_value": "$2558.75",
      "roi": "51.17%",
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

_[English Version]_
## 1. The ROI calculation method

The ROI (Return on Investment) that this Python code calculates is a way to see how much your investment has earned or lost, expressed as a percentage. Here, we have multiple investors (Joe, Bob, Alice) who have put money into (deposited) and taken money out of (withdrawn) an account at different times. The code figures out each person's investment performance by looking at when and how much they invested or withdrew, and how the account's total value changed over time.

## 2. What is ROI?

ROI is simply a number that shows "how much I've earned (or lost) compared to the money I invested." For example, if you invest \$100 and later have \$120, you've made \$20. To find the ROI, you divide that \$20 by your original \$100 and multiply by 100 to get 20%. Here, since multiple people are investing and withdrawing at different times, it gets a bit more complicated, but the basic idea is the same. We're looking at when and how much each person invested or withdrew, and how the account grew, to calculate each person's return.

What Data Are We Using?
The code uses two types of data:

### a. Transaction Data

This records who (Joe, Bob, Alice), when, and how much money was deposited or withdrawn.
For example: "Joe deposited \$1000 on May 1, 2024."
Deposits are shown as negative numbers (-), and withdrawals as positive numbers (+).

### b. Account Value Data

This shows how the total value of the account changed over time.
The account value is calculated as the cash balance (usdt_balance) plus any profits or losses from investments (unrealized_pnl).
For example: "On May 1, the account was worth \$5000, and by May 20, it grew to \$20,000."

## 3. How Is ROI Calculated?

Since the account size changes over time and people invest at different points, it wouldn't be fair to just compare "how much I invested" to "how much I have now." Instead, the code calculates each investment's "weight" based on the account's value at the time of investment. This way, it fairly accounts for when the money was invested and how the account grew afterward. Let's break it down step by step:

### a. Load the Data

The code reads the transaction and account value data from CSV files and organizes the dates.

### b. Find the Final Account Value

It looks at the most recent date in the account value data and calculates the total value (cash + profits/losses).
For example, if on May 20 the account is worth \$20,000, that's the final value.

### c. Calculate Each Investor's Investment Weight

Every time someone invests, the code looks at the account's value on that day and calculates a "weight" for that investment.
For example:
If Joe invests \$1000 on May 1 when the account is worth \$5000, his weight is 1000 / 5000 = 0.2 (20%).
If Bob invests \$2000 on May 5 when the account is worth \$7000, his weight is 2000 / 7000 ≈ 0.286 (28.6%).
This weight reflects how much of the account's value at that time was contributed by the investor.

### d. Sum Up All the Weights

The code adds up the weights from all investments. For example, Joe (0.2) + Bob (0.286) + others might total 1.0.

### e. Distribute the Final Account Value

Each investor's share of the final account value is calculated based on their weight relative to the total weights.
For example, if Joe's weight is 0.2 and the total weight is 1.0, his share is 0.2 / 1.0 = 20% of the final value.
So, if the final value is \$20,000, Joe's share is 20% of that, which is \$4000.

### f. Calculate ROI

For each investor, the ROI is calculated using their share of the final value, minus what they invested, plus any withdrawals.
The formula is:
ROI = [(final share - total invested + total withdrawn) / total invested] × 100
For example, if Joe invested \$1000 and his final share is \$4000, his ROI is [(4000 - 1000) / 1000] × 100 = 300%.

### g. Organize the Transaction History

The code also sorts and displays each investor's deposits and withdrawals in chronological order.

## 4. Understanding the Output with Examples
The output shows the investment performance for Joe, Bob, and Alice. Let's look at a couple of examples:

Joe - Round1

- First Deposit Date: May 1, 2024
- Total Invested: \$1000
- Final Share: \$8464.14
- ROI: 746.41%
- Interpretation: Joe invested \$1000 on May 1, and because the account grew a lot, his share became \$8464.14.

```
ROI = [(8464.14 - 1000) / 1000] × 100 ≈ 746.41%
```
Bob - Round2

- First Deposit Date: May 15, 2024
- Total Invested: \$1000
- Withdrawals: \$300 + \$400 = \$700
- Final Share: \$512.98
- ROI: 21.30%
- Interpretation: Bob invested \$1000 and withdrew \$700. His remaining share is \$512.98, so:

```
ROI = [(512.98 - 1000 + 700) / 1000] × 100 ≈ 21.30%
```

Alice - Round2
- Total Invested: \$5000 (\$4000 + \$1000)
- Withdrawals: \$5000
- Final Share: \$2558.75
- ROI: 51.17%
- Interpretation: After accounting for her investments and withdrawals:

```
ROI = [(2558.75 - 5000 + 5000) / 5000] × 100 ≈ 51.17%
```

## 5. Why Use This Method?
This method is fair because it considers both when the investments were made and how the account grew over time.

- Early investors might see higher ROI because their money had more time to grow (like Joe).
- Later investors or those who withdrew money will see their contributions reflected accordingly (like Bob and Alice).

Instead of just looking at "how much did I invest," this method accounts for "when did I invest and how much did my investment contribute to the account's growth," giving a more accurate picture of each person's return.





---

_[Korean Version]_
## 1. ROI 계산 방식을 쉽게 풀어서 설명하기

이 파이썬 코드가 계산하는 ROI(Return on Investment, 투자 수익률)는 투자한 돈이 얼마나 수익을 냈는지, 또는 손실을 봤는지를 퍼센트(%)로 나타내는 방법이에요. 여기서는 여러 투자자(Joe, Bob, Alice)가 각기 다른 시점에 돈을 넣고(입금) 빼며(출금) 계좌에 투자한 상황에서, 각자의 투자 성과를 어떻게 계산하는지 설명할게요.

## 2. ROI가 뭔가요?

ROI는 간단히 말해 "내가 넣은 돈 대비 얼마나 벌었나(혹은 잃었나)"를 보여주는 숫자예요. 예를 들어, 100만 원을 투자했는데 나중에 120만 원이 됐다면, 20만 원을 번 거죠. 이걸 투자한 돈(100만 원)으로 나누고 100을 곱하면 ROI가 20%가 됩니다.

여기서는 계좌에 여러 사람이 돈을 넣고 빼는 상황이라 조금 복잡해 보이지만, 기본 아이디어는 똑같아요. 각 투자자가 언제, 얼마를 넣고 뺐는지 보고, 계좌 전체 가치가 어떻게 변했는지 고려해서 각자의 수익률을 계산하는 거예요.

어떤 데이터를 사용하는 걸까요?
이 코드는 두 가지 데이터를 사용해요:

### a. 거래 데이터 (Transaction Data)

누가(Joe, Bob, Alice), 언제, 얼마를 넣었거나 뺐는지 기록이에요.
예: "Joe가 2024년 5월 1일에 1000달러를 입금했어요" 같은 정보죠.
입금은 음수(-)로, 출금은 양수(+)로 표시돼 있어요.

### b. 계좌 가치 데이터 (Account Value Data)

계좌의 총 가치가 날짜별로 어떻게 변했는지 보여줘요.
계좌 가치 = 현금 잔고(usdt_balance) + 투자 수익/손실(unrealized_pnl).
예: "5월 1일에 계좌 가치가 5000달러였고, 5월 20일에는 2만 달러가 됐다" 이런 식이에요.

## 3. ROI 계산 과정: 어떻게 하나요?

계좌에 돈을 넣는 시점마다 계좌 크기가 다르고, 그 뒤로 가치가 오르거나 내리니까, 단순히 "내가 넣은 돈 대비 지금 얼마가 됐나"로 계산하면 불공평할 수 있어요. 그래서 이 코드는 투자 시점과 계좌 크기를 고려해서 공정하게 나눠 계산해요. 단계별로 쉽게 풀어볼게요:

### a. 데이터 불러오기

거래 데이터와 계좌 가치 데이터를 CSV 파일에서 읽어와요.
날짜도 잘 정리해서 준비합니다. 

### b. 계좌의 최종 가치 구하기

계좌 가치 데이터에서 가장 최근 날짜의 총 가치를 계산해요(현금 + 수익/손실).
예: 5월 20일에 계좌 가치가 2만 달러라면, 이게 최종 가치예요.

### c. 각 투자자의 투자 비중 계산하기

투자자가 돈을 넣을 때마다, 그 시점의 계좌 가치와 비교해서 "비중"을 계산해요.
예를 들어:
5월 1일에 Joe가 1000달러를 넣었는데, 그때 계좌 가치가 5000달러였다면, Joe의 비중은 1000 / 5000 = 0.2(20%)이에요.
5월 5일에 Bob이 2000달러를 넣었는데, 그때 계좌 가치가 7000달러였다면, Bob의 비중은 2000 / 7000 ≈ 0.286(28.6%)예요.
이렇게 "비중"을 계산하면, 돈을 넣은 시점에 따라 공정하게 나눌 수 있어요.

### d. 모든 투자 비중 합치기

모든 투자자의 비중을 더해요. 예를 들어, Joe(0.2) + Bob(0.286) + 기타 투자자 비중 = 총합(예: 1.0).

### e. 최종 계좌 가치를 각 투자자에게 나누기

각 투자자의 비중을 총합으로 나눠서, 최종 계좌 가치에서 각자가 차지하는 몫을 구해요.
예: Joe의 비중이 0.2이고 총합이 1.0이면, Joe의 몫은 0.2 / 1.0 = 20%.
최종 가치 2만 달러의 20% = 4000달러가 Joe의 "최종 자산 가치"예요.

### f. ROI 계산하기

각 투자자의 최종 자산 가치에서 투자한 금액을 빼고, 출금한 금액을 더해줘요(출금은 투자한 돈이 줄어든 거니까). 그걸 투자 금액으로 나누고 100을 곱하면 ROI가 나와요.
공식:
ROI = [(최종 자산 가치 - 총 투자금 + 총 출금액) / 총 투자금] × 100
예: Joe가 1000달러를 투자했고, 최종 자산 가치가 4000달러라면:
ROI = [(4000 - 1000) / 1000] × 100 = 300%

### g. 거래 내역 정리하기

각 투자자가 언제 얼마를 넣고 뺐는지 날짜순으로 정리해서 보여줘요.

## 4. 출력 결과 예시로 이해하기

출력을 보면 Joe, Bob, Alice의 투자 성과가 나와요. 하나씩 살펴볼게요:

Joe - Round1
- 첫 입금 날짜: 2024-05-01
- 총 투자금: $1000
- 최종 자산 가치: $8464.14
- ROI: 746.41%
- 해석: Joe가 5월 1일에 1000달러를 넣었는데, 계좌가 엄청 커져서 그의 몫이 8464달러가 됐어요.

```
ROI = [(8464.14 - 1000) / 1000] × 100 ≈ 746.41%
```

Bob - Round2
- 첫 입금 날짜: 2024-05-15
- 총 투자금: $1000
- 출금: $300 + $400 = $700
- 최종 자산 가치: $512.98
- ROI: 21.30%
- 해석: Bob이 1000달러를 넣고 700달러를 뺐어요. 남은 몫이 512.98달러니까:

```
ROI = [(512.98 - 1000 + 700) / 1000] × 100 ≈ 21.30%
```

Alice - Round2
- 총 투자금: $5000(4000 + 1000)
- 출금: $5000
- 최종 자산 가치: $2558.75
- ROI: 51.17%
- 해석: 복잡해 보이지만, 투자와 출금을 고려해서 계산하면:
```
ROI = [(2558.75 - 5000 + 5000) / 5000] × 100 ≈ 51.17%
```

## 5. 왜 이렇게 계산하나요?

이 방식은 투자 시점과 계좌 성장을 고려해서 공정하게 나누는 방법이에요.

- 일찍 투자한 사람은 계좌가 더 많이 성장할 시간적 이점이 있으니 ROI가 높을 수 있어요(Joe처럼).
- 나중에 투자하거나 돈을 뺀 사람은 그만큼 덜 반영돼요(Bob, Alice처럼).

이렇게 하면 단순히 "누가 얼마 넣었나"가 아니라 "언제 넣었고, 그 돈이 얼마나 기여했나"를 반영해서 더 정확한 수익률을 알 수 있어요.