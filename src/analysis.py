import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

START_DATE = "2021-01-01"
END_DATE = "2026-01-01"

TICKERS = {
    "Tesla": "TSLA",
    "Hyundai": "005380.KS"
}

print("Yahoo Finance에서 데이터를 다운로드합니다...")

raw_data = yf.download(
    list(TICKERS.values()),
    start=START_DATE,
    end=END_DATE,
    auto_adjust=True
)

print("\n데이터 다운로드 완료!")
print("=" * 50)

print("\n[1] 데이터 앞부분")
print(raw_data.head())

print("\n[2] 데이터 뒷부분")
print(raw_data.tail())

print("\n[3] 데이터 크기")
print(raw_data.shape)

print("\n[4] 데이터 정보")
print(raw_data.info())

print("\n[5] 결측치 개수")
print(raw_data.isna().sum())

# 종가 데이터만 추출
close = raw_data["Close"].copy()

print("\n[6] 종가 데이터")
print(close.head())

print("\n[7] 종가 데이터 크기")
print(close.shape)

close = close.rename(columns={
    "TSLA": "Tesla",
    "005380.KS": "Hyundai"
})

print("\n[8] 종목명 변경 후")
print(close.head())

print("\n[9] 종가 데이터 결측치")
print(close.isna().sum())

close = close.dropna()

print("\n[10] 결측치 제거 후 데이터 크기")
print(close.shape)

print("\n[11] 결측치 제거 후 결측치")
print(close.isna().sum())

print("\n[12] 최종 분석 데이터")
print(close.head(10))

print("\n[13] 최종 데이터 정보")
print(close.info())

print("\n[14] 데이터 시작일")
print(close.index.min())

print("\n[15] 데이터 종료일")
print(close.index.max())

print("\n[16] 최종 데이터 개수")
print(len(close))

print("\n[17] 중복 날짜 확인")
print("중복 날짜 개수:", close.index.duplicated().sum())

print("\n[18] 0 이하 가격 확인")
print((close <= 0).sum())

print("\n[19] 데이터 타입")
print(close.dtypes)

print("\n[20] 기본 통계")
print(close.describe())

# 일간 수익률 계산
returns = close.pct_change() * 100

# 첫 번째 날짜는 이전 날짜가 없기 때문에 결측치 발생
returns = returns.dropna()

print("\n[21] 일간 수익률")
print(returns.head())

print("\n[22] 일간 수익률 데이터 크기")
print(returns.shape)

print("\n[23] 일간 수익률 기본 통계")
print(returns.describe())

# 정규화 가격 계산
normalized = close / close.iloc[0] * 100

print("\n[24] 정규화 가격")
print(normalized.head())

print("\n[25] 정규화 가격 마지막 값")
print(normalized.tail())

plt.figure(figsize=(12, 6))

plt.plot(normalized.index, normalized["Hyundai"], label="Hyundai")
plt.plot(normalized.index, normalized["Tesla"], label="Tesla")

plt.title("Normalized Stock Price (Start = 100)")
plt.xlabel("Date")
plt.ylabel("Normalized Price")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("images/normalized_price.png", dpi=150)
plt.show()

plt.figure(figsize=(12, 6))

plt.plot(returns.index, returns["Hyundai"], label="Hyundai", alpha=0.7)
plt.plot(returns.index, returns["Tesla"], label="Tesla", alpha=0.7)

plt.title("Daily Returns")
plt.xlabel("Date")
plt.ylabel("Daily Return (%)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("images/daily_returns.png", dpi=150)
plt.show()

# 30일 이동 변동성
rolling_volatility = returns.rolling(window=30).std()

print("\n[26] 30일 이동 변동성")
print(rolling_volatility.tail())

plt.figure(figsize=(12, 6))

plt.plot(
    rolling_volatility.index,
    rolling_volatility["Hyundai"],
    label="Hyundai"
)

plt.plot(
    rolling_volatility.index,
    rolling_volatility["Tesla"],
    label="Tesla"
)

plt.title("30-Day Rolling Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility (%)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("images/rolling_volatility.png", dpi=150)
plt.show()

normalized = close / close.iloc[0] * 100