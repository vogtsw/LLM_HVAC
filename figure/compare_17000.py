import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

rate=0.85


# csv_data = pd.read_csv('../result/result-gpt4o-17000-30day.csv')
csv_data = pd.read_csv('../result/result-gpt4o-rag-15%-17000-30day.csv')

df = pd.read_csv('../data/result-11-22.csv')

plt.rcParams['figure.dpi'] = 300

plt.rcParams['axes.unicode_minus'] = False
csv_data = csv_data[(csv_data[['Energy_1', 'Energy_2', 'Energy_3', 'Energy_4', 'Energy_5']] != 0).all(axis=1)]

a = csv_data[['Energy_1', 'Energy_2', 'Energy_3', 'Energy_4', 'Energy_5']].sum(axis=1)
b=17000


result = (a-b) / b
result_median = np.median(result)

print(f"middle of result {result_median}")


plt.figure(figsize=(10, 6))
plt.plot(range(len(result)), result)
plt.xlabel('time')
plt.xticks(rotation=45)
plt.ylabel('(a - b) / b')
plt.title('error from 15%')
plt.grid(True)
plt.tight_layout()

plt.show()


error_less_than_5_percent = (abs(result) < 0.05).sum() / len(result)
error_less_than_10_percent = (abs(result) < 0.1).sum() / len(result)


labels = ['< 5%', '< 10%']
sizes = [error_less_than_5_percent, error_less_than_10_percent]


plt.figure(figsize=(8, 6))
plt.bar(labels, sizes)
plt.xlabel('Error Range')
plt.ylabel('Proportion')
plt.title('Proportion of Errors within Different Ranges')
plt.grid(axis='y')
plt.tight_layout()
print("smaller than 5%",error_less_than_5_percent)
print("smaller than 5%",error_less_than_10_percent)
plt.show()

