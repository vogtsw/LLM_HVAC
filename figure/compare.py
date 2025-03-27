
rate = 0.85
# 读取 CSV 文件
# csv_data = pd.read_csv('../result/result-gpt4o-15%-30day.csv')
csv_data = pd.read_csv('../result/result-gpt4o-rag-15%-30day.csv')
df = pd.read_csv('../data/result-11-22.csv')


plt.rcParams['figure.dpi'] = 300
plt.rcParams['axes.unicode_minus'] = False
combined_df = pd.concat([csv_data[['Energy_1', 'Energy_2', 'Energy_3', 'Energy_4', 'Energy_5']],
                         df[['Energy_1', 'Energy_2', 'Energy_3', 'Energy_4', 'Energy_5']]],
                        axis=1, keys=['csv', 'df'])


filtered_df = combined_df[
    (combined_df.loc[:, (slice(None), ['Energy_1', 'Energy_2', 'Energy_3', 'Energy_4', 'Energy_5'])] != 0).all(axis=1)]


csv_data_filtered = filtered_df['csv']
df_filtered = filtered_df['df']

a = csv_data_filtered.sum(axis=1)


b = df_filtered.sum(axis=1) * rate

result = (a - b) / b
result_median = np.median(result)

print(f"middle of result: {result_median}")


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
print("smaller than 5%", error_less_than_5_percent)
print("smaller than 10%", error_less_than_10_percent)
plt.show()
