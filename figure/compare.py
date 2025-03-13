import pandas as pd
import matplotlib.pyplot as plt


csv_data = pd.read_csv('../result/result-openai-15% test.csv')

excel_file = pd.ExcelFile('../data/set_temperature_22.xlsx')


df = excel_file.parse('Sheet1')

plt.rcParams['figure.dpi'] = 300

plt.rcParams['axes.unicode_minus'] = False


a = csv_data[['Energy_1', 'Energy_2', 'Energy_3', 'Energy_4', 'Energy_5']].sum(axis=1)


b = df[['Energy_1', 'Energy_2', 'Energy_3', 'Energy_4', 'Energy_5']].sum(axis=1) * 0.85


result = (a - b) / b
result_mean = result.mean()
print(f"result 的平均值为: {result_mean}")


plt.figure(figsize=(10, 6))
plt.plot(range(len(result)), result)
plt.xlabel('time')
plt.xticks(rotation=45)
plt.ylabel('(a - b) / b')
plt.title('Difference from 15%')
plt.grid(True)
plt.tight_layout()

plt.show()

