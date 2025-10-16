import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 1. CSV 파일 불러오기 (탭으로 구분되어 있으므로 sep="\t")
# df = pd.read_csv("data.csv", sep="\t")
# df = pd.read_csv("/Users/heezee/Documents/project/example/data.csv", sep="\t")
df = pd.read_csv("data.csv", sep="\t", names=["date", "rain"], skiprows=1)


# 2. 컬럼 소문자화 (혹시 모를 오류 방지)
df.columns = df.columns.str.lower()

# 3. 'Jan.00' → '2000-01' 형태로 바꾸기 위한 전처리
# 월 이름 매핑
month_map = {
    'jan.': 1, 'feb.': 2, 'mar.': 3, 'apr.': 4, 'may.': 5, 'jun.': 6,
    'jul.': 7, 'aug.': 8, 'sep.': 9, 'oct.': 10, 'nov.': 11, 'dec.': 12
}

# date 컬럼 전처리
df['date'] = df['date'].str.lower().str.strip()

# 월과 연도 분리
df['month_str'] = df['date'].str.extract(r'([a-z]+\.)')
df['year_str'] = df['date'].str.extract(r'(\d+)$')

# 숫자로 변환
df['month'] = df['month_str'].map(month_map)
df['year'] = df['year_str'].astype(int).apply(lambda x: 2000 + x)

# datetime 컬럼 생성
df['date_parsed'] = pd.to_datetime(
    dict(year=df['year'], month=df['month'], day=1))

# 필요한 컬럼만 정리
df = df[['date_parsed', 'rain', 'year', 'month']].rename(
    columns={'date_parsed': 'date'})

# ------------------------------
# 분석: 2014~2018 vs 2019~2023
# ------------------------------

# 기간 필터링
period1 = df[(df['year'] >= 2014) & (df['year'] <= 2019)]
period2 = df[(df['year'] >= 2019) & (df['year'] <= 2023)]

# 월별 평균 강수량
monthly_avg1 = period1.groupby('month')['rain'].mean()
monthly_avg2 = period2.groupby('month')['rain'].mean()

# 시각화
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
plt.plot(monthly_avg1.index, monthly_avg1.values,
         marker='o', label='2000-2004')
plt.plot(monthly_avg2.index, monthly_avg2.values,
         marker='s', label='2019-2023')
plt.title('월별 평균 강수량 비교')
plt.xlabel('월')
plt.ylabel('평균 강수량 (mm)')
plt.xticks(range(1, 13))
plt.legend()
plt.tight_layout()
plt.show()
