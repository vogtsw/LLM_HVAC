import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件
csv_data = pd.read_csv('../result/result-openai-15% test.csv')
# csv_data = pd.read_csv('../result/result-openai-rag-15% test.csv')
# 读取 Excel 文件
excel_file = pd.ExcelFile('../data/set_temperature_22.xlsx')

# 获取指定工作表中的数据
df = excel_file.parse('Sheet1')

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 正常显示中文
# plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']

# 正常显示负号
plt.rcParams['axes.unicode_minus'] = False

# 计算 csv 文件中 5 列能量值的总和
a = csv_data[['Energy_1', 'Energy_2', 'Energy_3', 'Energy_4', 'Energy_5']].sum(axis=1)

# 计算 excel 文件中 5 列能量值的总和，并降低 15%
b = df[['Energy_1', 'Energy_2', 'Energy_3', 'Energy_4', 'Energy_5']].sum(axis=1) * 0.85

# 计算 (a - b) / b 的值
result = (a - b) / b
result_mean = result.mean()
print(f"result 的平均值为: {result_mean}")

# 绘制时间与 (a - b) / b 的变化图像
plt.figure(figsize=(10, 6))
plt.plot(range(len(result)), result)
plt.xlabel('time')
plt.xticks(rotation=45)
plt.ylabel('(a - b) / b')
plt.title('Difference from 15%')
plt.grid(True)
plt.tight_layout()

plt.show()

