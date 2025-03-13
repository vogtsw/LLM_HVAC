import os
from openai import OpenAI
import pandas as pd

# openai or deepseek api
os.environ["OPENAI_BASE_URL"] = "https://api.zhizengzeng.com/v1/"
os.environ["OPENAI_API_KEY"] = "sk-zk22d3b63d681ab4346a61c6e66a1212d8a66d581c98c8fd"

client = OpenAI()

# 读取文件
excel_file = pd.ExcelFile('../data/set_temperature_22.xlsx')
# 获取指定工作表中的数据
df = excel_file.parse('Sheet1')

# 初始化字典来存储分组后的数据
vars_dict = {}

# 参与分析的列名
columns = ['t_out', 'Energy_2', 'Energy_4', 'Energy_3', 'temperature:drybulb', 'Equip', 'Energy_5', 'Energy_1', 'light', 'occ']

# 分组的数量
num_groups = len(df) // 6

for group_index in range(1, num_groups + 1):
    start_index = (group_index - 1) * 6
    end_index = start_index + 6

    # 计算 Total_Energy
    total_energy = []
    for i in range(start_index, end_index):
        energy_sum = df.loc[i, 'Energy_1'] + df.loc[i, 'Energy_2'] + df.loc[i, 'Energy_3'] + df.loc[i, 'Energy_4'] + df.loc[i, 'Energy_5']
        total_energy.append(energy_sum)
    vars_dict[f'Total_Energy_{group_index}'] = total_energy

    for col in columns:
        data = df[col]
        group = data[start_index:end_index].tolist()
        if col == 'temperature:drybulb':
            col = 'temperature_drybulb'
        vars_dict[f'{col}_{group_index}'] = group

custom_prompt_1 = (
    """
Building Information:
Large office (conditioned area of 46,320.38 square meters)
Wall area: 12,183.90 square meters (window-to-wall ratio of 43.92%)
Roof area: 3,563.11 square meters (skylight ratio of 0%)
Openable window area: 5,350.65 square meters
Above-ground wall area: 11,589.54 square meters
Cooling: Water-cooled chillers with a cooling capacity of 3,959 kW
Ventilation: Variable Air Volume (VAV) system (maximum outdoor air intake of 157.54 cubic meters per second)

Current Operational Data (each value represents the situation at 10 - minute intervals):
You will be provided with 30 consecutive data points for various parameters.
For outdoor temperature, you have t_out_1 to t_out_30: {t_out_1} {t_out_2}... {t_out_30}
For equipment situation, Equip_1 to Equip_30: {Equip_1} {Equip_2}... {Equip_30}
For building's lighting, light_1 to light_30: {light_1} {light_2}... {light_30}
For occupancy ratio, occ_1 to occ_30: {occ_1} {occ_2}... {occ_30}
Total energy consumption for each 10 - minute interval from Total_Energy_1 to Total_Energy_30: {Total_Energy_1} {Total_Energy_2}... {Total_Energy_30}
The last 6 temperature setpoints are temperature_drybulb_25 to temperature_drybulb_30: {temperature_drybulb_25} {temperature_drybulb_26}... {temperature_drybulb_30}

Task:
Based on the above 30 - data - point information and your knowledge of HVAC systems, analyze the trends, especially focusing on the last 6 outdoor temperatures (t_out_25 to t_out_30), and set 6 recommended temperature values for the HVAC system within the current hour. The temperature goal is that compared to when the current temperature is set at the average of the last 6 temperature setpoints (average of temperature_drybulb_25 to temperature_drybulb_30), your recommended temperature values will reduce the building's total energy consumption by 15%.

Output Format:
temp_hour=[X.X X.X X.X X.X X.X X.X]
(6 temperature values, at 10 - minute intervals, with one decimal place precision, values within the range of 22.0 - 29.0°C)

Prohibited:
Code blocks
Explanatory text
"""
)

client = OpenAI()
temp_hour = []
with open("../result/openai_setting22.txt", "w", encoding="utf-8") as file:
    for i in range(1, num_groups + 1):
        start_group = max(1, i - 4)
        end_group = min(num_groups, i)

        params = {}
        for col in columns:
            if col == 'temperature:drybulb':
                col = 'temperature_drybulb'
            for j in range(1, 31):
                group_index = start_group + (j - 1) // 6
                sub_index = (j - 1) % 6
                if group_index in vars_dict:
                    params[f'{col}_{j}'] = vars_dict[f'{col}_{group_index}'][sub_index]
                else:
                    # 处理前四个6组数据没有前面数据的情况，这里简单用0填充，可根据实际情况调整
                    params[f'{col}_{j}'] = 0

        for j in range(1, 31):
            group_index = start_group + (j - 1) // 6
            sub_index = (j - 1) % 6
            if group_index in vars_dict:
                params[f'Total_Energy_{j}'] = vars_dict[f'Total_Energy_{group_index}'][sub_index]
            else:
                # 处理前四个6组数据没有前面数据的情况，这里简单用0填充，可根据实际情况调整
                params[f'Total_Energy_{j}'] = 0

        completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are an AI assistant to a building operations manager in Singapore, responsible for optimizing the energy efficiency of the Heating, Ventilation, and Air Conditioning (HVAC) system while ensuring the comfort of the occupants."},
                {"role": "user", "content": custom_prompt_1.format(**params)}
            ]
        )

        respond = completion.choices[0].message
        text = respond.content
        file.write(f"hour {i}————————————————————————————————————————————————————————————————\n")

        print(text)
        print(f"hour {i}————————————————————————————————————————————————————————————————")
        start_index = text.find('[') + 1
        end_index = text.find(']')
        if start_index != 0 and end_index != -1:
            temp_str = text[start_index:end_index]
            temps = [float(temp.replace(',', '')) for temp in temp_str.split()]
            temp_hour.extend(temps)

print("最终的温度列表:", temp_hour)
print("最终的温度列表长度:", len(temp_hour))






# import os
# from openai import OpenAI
# import pandas as pd
#
# # openai or deepseek api
# os.environ["OPENAI_BASE_URL"] =  "https://api.zhizengzeng.com/v1/"
# os.environ["OPENAI_API_KEY"] = "sk-zk22d3b63d681ab4346a61c6e66a1212d8a66d581c98c8fd"
#
# client = OpenAI()
#
# models = client.models.list()
# print(models)
#
# # 读取文件
# excel_file = pd.ExcelFile('../data/set_temperature_22.xlsx')
#
# # 获取指定工作表中的数据
# df = excel_file.parse('Sheet1')
#
# # 初始化字典来存储分组后的数据
# vars_dict = {}
#
# # 参与分析的列名
# columns = ['t_out', 'Energy_2', 'Energy_4', 'Energy_3', 'temperature:drybulb', 'Equip', 'Energy_5', 'Energy_1', 'light', 'occ']
#
# for col in columns:
#     data = df[col]
#     group_index = 1
#     for i in range(0, len(data), 6):
#         group = data[i:i + 6].tolist()
#         if col == 'temperature:drybulb':
#             col = 'temperature_drybulb'
#         vars_dict[f'{col}_{group_index}'] = group
#         group_index += 1
#
# custom_prompt_1 = (
#     """
#     Role:
#     You are an AI assistant for a building operations manager in Singapore responsible for optimizing HVAC energy efficiency while maintaining occupant comfort. Your task is to recommend optimal indoor temperature settings for a 1-hour period with 10-minute intervals during August's peak cooling season.
#
#     Building Specifications:
#     1.Structure:
#     Large Office (46,320.38 m² conditioned area)
#     Wall Area: 12,183.90 m² (43.92% window-wall ratio)
#     Roof Area: 3,563.11 m² (0% skylights)
#     Window Opening Area: 5,350.65 m²
#     Above Ground Wall Area: 11,589.54 m²
#     2.Systems:
#     Cooling: Water-cooled chillers with 3,959 kW cooling capacity
#     Ventilation: VAV system (157.54 m³/s max outdoor airflow)
#
#     Current Operational Data (6x10-minute intervals):
#     1.t_out: Outdoor temperatures [°C] = {t_out}
#     2.Zone Energy Consumption [kW]:
#         Zone 1: {Energy_1}
#         Zone 2: {Energy_2}
#         Zone 3: {Energy_3}
#         Zone 4: {Energy_4}
#         Zone 5: {Energy_5}
#         Total Energy consumption: Total energy consumption of all zones
#     3.Ancillary Loads:
#     Equipment: {Equip}
#     Lighting: {light}
#     Occupancy: {occ}
#     4.Current Temperature Setpoint: {temperature_drybulb}°C
#
#     Analysis Requirements:
#     1.Consider dynamic interactions between:
#     External heat gain (window-dominated facade)
#     Internal heat loads (equipment/occupancy)
#     Chiller system efficiency curves
#     2.Prioritize energy-saving opportunities during:
#     Lower occupancy periods
#     Equipment load fluctuations
#     Natural temperature variations
#
#     Task：
#     Set a temperature recommendation for the building every 10 minutes for the current hour. The temperature goal is to reduce the building's total energy consumption by 15% compared to when the temperature is set to {temperature_drybulb}.
#     Output Format：
#     temp_hour=[X.X X.X X.X X.X X.X X.X]
#     (6 temperature values, 10-minute intervals, 1 decimal precision) for example：temp_hour=[25.5, 26, 26.5, 26.5, 25.0, 24.0]
#
#     Prohibited:
#     Code blocks
#     Explanatory text
#     Values outside 22 - 29°C range
#     """
# )
#
# # 总组数，24 小时 * 7 天，每六个数据一组代表十分钟
# total_groups = 24 * 7
# temp_hour = []  # 初始化一个空列表用于存储所有温度值
# client = OpenAI()  # 创建OpenAI客户端对象
#
# with open("../result/openai_setting22.txt", "w", encoding="utf-8") as file:
#     for i in range(1, total_groups + 1):
#     # for i in range(0, 2):
#         # 构建用于格式化提示的参数
#         params = {col.replace(':', '_'): vars_dict.get(f'{col.replace(":", "_")}_{i}', None) for col in columns}
#
#         # 调用模型
#         completion = client.chat.completions.create(
#             model="gpt-4o-mini-2024-07-18",
#             messages=[
#                 {"role": "system", "content": "You are an expert in air conditioning systems and construction equipment。"},
#                 {"role": "user", "content": custom_prompt_1.format(**params)}
#             ]
#         )
#
#         # 输出模型回复
#         respond = completion.choices[0].message
#         text = respond.content
#         file.write(text + "\n")  # 写入温度设置
#         file.write(f"hour {i}————————————————————————————————————————————————————————————————\n")  # 写入分隔线
#
#         print(text)
#         print(f"hour {i}————————————————————————————————————————————————————————————————")
#             # 解析回复中的温度值
#         start_index = text.find('[') + 1
#         end_index = text.find(']')
#         if start_index != 0 and end_index != -1:
#             temp_str = text[start_index:end_index]
#             temps = [float(temp.replace(',', '')) for temp in temp_str.split()]
#             temp_hour.extend(temps)
#
# print("最终的温度列表:", temp_hour)
# print("最终的温度列表:", len(temp_hour))
# # temp_hour=[24.5, 24.7, 25.0, 25.2, 25.5, 25.5, 24.5, 24.7, 24.9, 25.1, 25.3, 25.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 25.0, 25.0, 25.0, 25.5, 25.5, 25.5, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.5, 25.5, 25.5, 25.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.7, 24.8, 24.5, 24.7, 24.5, 24.0, 24.0, 24.5, 25.0, 25.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 23.5, 25.0, 25.5, 25.5, 25.5, 25.0, 24.5, 24.5, 24.8, 25.0, 25.2, 25.5, 25.8, 25.5, 25.5, 25.0, 25.0, 24.5, 24.5, 25.0, 25.5, 26.0, 26.0, 25.5, 25.0, 24.0, 24.2, 24.5, 24.6, 24.8, 25.0, 24.5, 24.7, 24.9, 25.1, 25.3, 25.5, 24.0, 24.2, 24.4, 24.6, 24.5, 24.3, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 25.0, 25.5, 25.5, 25.5, 25.0, 24.5, 24.5, 24.5, 24.0, 24.0, 23.5, 23.5, 25.0, 25.5, 26.0, 26.0, 25.5, 25.0, 25.0, 25.3, 25.5, 25.5, 25.2, 25.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 23.5, 23.5, 24.5, 24.7, 24.5, 24.7, 24.5, 24.5, 25.0, 25.2, 25.4, 25.4, 25.2, 25.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 25.0, 25.0, 25.5, 25.5, 25.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 23.5, 24.5, 24.5, 24.8, 25.0, 25.5, 25.5, 25.5, 25.5, 25.0, 25.0, 25.5, 25.5, 25.0, 25.2, 25.5, 25.7, 25.4, 25.1, 24.0, 24.5, 24.5, 24.5, 24.0, 23.5, 25.0, 25.5, 25.5, 26.0, 26.0, 26.5, 25.5, 25.5, 25.0, 24.5, 24.0, 23.5, 24.5, 24.5, 24.7, 24.7, 24.5, 24.5, 24.5, 24.9, 25.2, 25.3, 25.7, 26.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 23.0, 23.2, 23.4, 23.5, 23.3, 23.1, 24.5, 24.6, 24.7, 24.8, 24.6, 24.5, 24.5, 24.7, 25.0, 25.0, 24.5, 24.2, 25.0, 25.0, 25.5, 26.0, 26.0, 25.5, 25.0, 25.3, 25.5, 25.7, 25.5, 25.0, 24.5, 24.5, 24.5, 24.5, 24.0, 23.5, 25.0, 25.2, 25.5, 25.7, 25.5, 25.3, 24.5, 24.8, 25.0, 25.2, 25.0, 24.5, 24.0, 24.0, 24.0, 24.5, 24.5, 24.0, 24.0, 24.5, 25.0, 25.0, 24.5, 24.0, 25.0, 25.0, 25.0, 25.0, 24.5, 24.5, 24.5, 24.7, 24.8, 25.0, 25.2, 25.4, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 26.0, 26.0, 26.0, 26.5, 26.5, 27.0, 25.0, 25.5, 25.0, 24.5, 25.5, 25.0, 25.0, 25.2, 25.5, 25.5, 25.2, 25.0, 24.5, 24.7, 24.9, 24.7, 24.5, 24.3, 24.5, 24.8, 25.0, 25.2, 25.5, 25.8, 24.5, 24.5, 24.5, 24.0, 24.0, 24.0, 25.0, 25.0, 25.0, 25.0, 25.5, 25.5, 24.5, 24.5, 24.0, 24.0, 23.5, 23.5, 25.0, 25.0, 25.5, 25.5, 25.0, 24.5, 25.5, 25.5, 25.5, 25.5, 25.0, 24.5, 25.0, 25.5, 26.0, 26.0, 25.5, 25.0, 25.0, 25.0, 25.5, 25.5, 25.0, 24.5, 24.5, 24.5, 24.5, 25.0, 25.0, 25.5, 24.5, 24.7, 25.0, 25.2, 24.8, 24.6, 25.5, 25.5, 25.7, 25.7, 25.5, 25.2, 24.5, 24.7, 24.7, 24.9, 24.8, 24.6, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 23.5, 23.8, 24.0, 24.2, 24.5, 24.7, 24.5, 24.0, 24.0, 24.5, 25.0, 25.5, 25.0, 25.5, 26.0, 26.0, 25.5, 25.0, 24.5, 24.8, 25.0, 25.2, 25.5, 26.0, 25.0, 25.0, 25.5, 25.5, 25.5, 25.0, 25.5, 25.5, 25.5, 25.0, 24.5, 24.0, 24.5, 24.5, 24.5, 24.5, 25.0, 25.0, 22.0, 22.5, 22.5, 23.0, 23.0, 23.5, 25.5, 25.5, 25.6, 25.6, 25.7, 25.7, 25.0, 25.5, 25.5, 25.5, 25.0, 24.5, 23.0, 23.2, 23.4, 23.3, 23.1, 22.9, 24.0, 24.0, 24.0, 24.5, 25.0, 25.0, 22.0, 22.0, 22.0, 22.0, 22.5, 22.5, 24.0, 24.5, 25.0, 25.0, 24.5, 24.0, 25.0, 25.5, 25.5, 26.0, 26.0, 26.0, 24.5, 24.5, 24.0, 24.0, 24.5, 25.0, 24.5, 24.7, 24.9, 25.0, 25.2, 25.3, 24.5, 24.0, 23.5, 23.5, 24.0, 24.5, 24.5, 24.7, 25.0, 25.2, 25.5, 25.7, 25.0, 25.0, 25.5, 25.5, 25.0, 24.5, 25.0, 25.5, 26.0, 26.5, 26.5, 25.5, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 25.0, 25.5, 25.5, 25.5, 25.0, 24.5, 25.0, 25.0, 24.5, 24.0, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 26.0, 25.5, 25.5, 25.5, 25.0, 25.0, 24.5, 24.0, 25.0, 25.5, 25.5, 25.0, 24.5, 24.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 25.0, 25.2, 25.5, 25.7, 25.9, 26.1, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.7, 24.9, 25.1, 25.3, 25.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 25.0, 25.0, 25.5, 25.5, 26.0, 26.0, 24.0, 24.5, 25.0, 25.5, 25.0, 24.5, 25.0, 25.5, 26.0, 26.5, 26.5, 25.5, 24.5, 24.6, 24.7, 24.7, 24.8, 24.9, 25.5, 25.8, 26.0, 26.2, 26.5, 26.7, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 24.5, 24.7, 25.0, 25.2, 25.5, 25.7, 25.6, 25.8, 25.7, 25.9, 25.5, 25.4, 25.5, 25.5, 25.5, 25.5, 25.0, 24.5, 24.5, 24.7, 25.0, 25.2, 25.5, 25.7, 23.5, 23.5, 23.8, 24.0, 24.0, 24.2, 25.0, 25.5, 26.0, 26.5, 26.0, 25.5, 25.5, 25.7, 25.9, 26.1, 26.3, 26.5, 24.5, 24.0, 24.0, 24.5, 25.0, 25.0, 23.5, 23.5, 24.0, 24.5, 24.5, 24.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 25.0, 25.5, 25.5, 25.0, 24.5, 24.0, 25.5, 25.0, 25.0, 24.5, 24.5, 24.0, 25.0, 25.5, 25.5, 26.0, 26.0, 26.5, 24.0, 24.5, 24.5, 25.0, 25.5, 25.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 24.5, 25.0, 25.0, 24.5, 24.0, 25.0, 25.5, 25.5, 26.0, 26.0, 26.5, 25.0, 25.5, 26.0, 26.0, 25.5, 25.0, 25.0, 25.2, 25.4, 25.4, 25.2, 25.0, 24.5, 24.7, 24.9, 24.7, 24.5, 24.3, 24.5, 24.7, 24.5, 24.3, 24.1, 24.0, 25.5, 25.5, 25.5, 25.5, 25.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 23.5, 23.7, 24.0, 24.2, 24.5, 24.7, 25.0, 25.0, 25.5, 25.5, 25.0, 24.5, 25.0, 25.0, 25.0, 25.5, 25.5, 25.0, 24.0, 24.5, 24.5, 25.0, 25.0, 25.5, 24.5, 24.5, 24.5, 25.0, 25.0, 25.5, 24.5, 24.7, 24.9, 25.1, 25.3, 25.5, 24.5, 24.8, 25.0, 25.2, 24.9, 24.5, 24.0, 24.5, 25.0, 25.5, 25.5, 25.0, 24.5, 24.8, 25.0, 25.2, 24.7, 24.5, 23.5, 23.7, 23.9, 24.0, 24.2, 24.4, 24.5, 24.5, 24.0, 24.0, 23.5, 23.0, 24.5, 24.5, 24.5, 24.6, 24.6, 24.6, 24.6, 24.8, 25.0, 25.2, 25.4, 25.5, 25.0, 25.0, 25.5, 25.5, 25.0, 24.5, 24.5, 24.8, 25.0, 25.2, 25.4, 25.5, 25.5, 25.5, 25.0, 25.0, 24.5, 24.5, 24.0, 24.5, 25.0, 25.5, 25.5, 25.0, 25.0, 25.0, 25.5, 25.5, 25.0, 24.5, 22.0, 22.5, 23.0, 23.0, 22.5, 22.0, 25.0, 25.5, 25.5, 25.7, 25.3, 25.0, 25.0, 25.0, 25.0, 25.5, 25.5, 25.5, 24.5, 24.7, 24.8, 25.0, 24.6, 24.3, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 25.0, 25.5, 24.5, 24.8, 25.0, 25.2, 25.5, 25.8, 25.0, 25.2, 25.4, 25.5, 25.3, 25.1, 25.0, 25.5, 26.0, 26.0, 25.5, 25.0, 24.5, 24.5, 24.0, 24.0, 24.5, 24.5, 24.5, 24.5, 24.7, 24.7, 24.5, 24.3, 25.0, 25.5, 25.0, 25.5, 26.0, 26.5, 25.5, 25.5, 25.5, 25.5, 25.5, 25.5, 24.5, 24.2, 24.0, 24.1, 24.3, 24.6, 24.5, 24.8, 25.0, 25.3, 25.5, 25.7, 24.5, 24.7, 25.0, 25.3, 25.5, 25.8, 25.0, 25.0, 25.5, 25.5, 25.5, 25.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.7, 24.9, 25.1, 25.0, 24.8, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.8, 25.0, 25.2, 25.5, 25.7]

#
# # 读取文件
# excel_file = pd.ExcelFile('/kaggle/input/final-llm-building-data/set_temperature_22.xlsx')
# 获取指定工作表中的数据
# df = excel_file.parse('Sheet1')
#
# # 初始化字典来存储分组后的数据
# vars_dict = {}
#
# # 参与分析的列名
# columns = ['t_out', 'Energy_2', 'Energy_4', 'Energy_3', 'temperature:drybulb', 'Equip', 'Energy_5', 'Energy_1', 'light', 'occ']
#
# # 分组的数量
# num_groups = len(df) // 6
#
# for group_index in range(1, num_groups + 1):
#     start_index = (group_index - 1) * 6
#     end_index = start_index + 6
#
#     # 计算 Total_Energy
#     total_energy = []
#     for i in range(start_index, end_index):
#         energy_sum = df.loc[i, 'Energy_1'] + df.loc[i, 'Energy_2'] + df.loc[i, 'Energy_3'] + df.loc[i, 'Energy_4'] + df.loc[i, 'Energy_5']
#         total_energy.append(energy_sum)
#     vars_dict[f'Total_Energy_{group_index}'] = total_energy
#
#     for col in columns:
#         data = df[col]
#         group = data[start_index:end_index].tolist()
#         if col == 'temperature:drybulb':
#             col = 'temperature_drybulb'
#         vars_dict[f'{col}_{group_index}'] = group
#
#
# custom_prompt_1 = (
#     """
# Building Information:
# Large office (conditioned area of 46,320.38 square meters)
# Wall area: 12,183.90 square meters (window-to-wall ratio of 43.92%)
# Roof area: 3,563.11 square meters (skylight ratio of 0%)
# Openable window area: 5,350.65 square meters
# Above-ground wall area: 11,589.54 square meters
# Cooling: Water-cooled chillers with a cooling capacity of 3,959 kW
# Ventilation: Variable Air Volume (VAV) system (maximum outdoor air intake of 157.54 cubic meters per second)
#
# Current Operational Data (each value represents the situation at 10 - minute intervals):
# You will be provided with 30 consecutive data points for various parameters.
# For outdoor temperature, you have t_out_1 to t_out_30: {t_out_1} {t_out_2}... {t_out_30}
# For equipment situation, Equip_1 to Equip_30: {Equip_1} {Equip_2}... {Equip_30}
# For building's lighting, light_1 to light_30: {light_1} {light_2}... {light_30}
# For occupancy ratio, occ_1 to occ_30: {occ_1} {occ_2}... {occ_30}
# Total energy consumption for each 10 - minute interval from Total_Energy_1 to Total_Energy_30: {Total_Energy_1} {Total_Energy_2}... {Total_Energy_30}
# The last 6 temperature setpoints are temperature_drybulb_25 to temperature_drybulb_30: {temperature_drybulb_25} {temperature_drybulb_26}... {temperature_drybulb_30}
#
# Task:
# Based on the above 30 - data - point information and your knowledge of HVAC systems, analyze the trends, especially focusing on the last 6 outdoor temperatures (t_out_25 to t_out_30), and set 6 recommended temperature values for the HVAC system within the current hour. The temperature goal is that compared to when the current temperature is set at the average of the last 6 temperature setpoints (average of temperature_drybulb_25 to temperature_drybulb_30), your recommended temperature values will reduce the building's total energy consumption by 15%.
#
# Output Format:
# temp_hour=[X.X X.X X.X X.X X.X X.X]
# (6 temperature values, at 10 - minute intervals, with one decimal place precision, values within the range of 22.0 - 29.0°C)
#
# Prohibited:
# Code blocks
# Explanatory text
# """
# )
#
# # 总组数，调整为每30个数据一组
# total_groups = (len(df) // 6) // 5
#
# client = OpenAI()
# temp_hour = []
# with open("../result/openai_setting22.txt", "w", encoding="utf-8") as file:
#     for i in range(total_groups):
#         start_group = i * 5 + 1
#         end_group = start_group + 4
#
#         params = {}
#         for col in columns:
#             if col == 'temperature:drybulb':
#                 col = 'temperature_drybulb'
#             for j in range(1, 31):
#                 group_index = start_group + (j - 1) // 6
#                 sub_index = (j - 1) % 6
#                 if group_index in vars_dict:
#                     params[f'{col}_{j}'] = vars_dict[f'{col}_{group_index}'][sub_index]
#                 else:
#                     # 处理前四个6组数据没有前面数据的情况，这里简单用0填充，可根据实际情况调整
#                     params[f'{col}_{j}'] = 0
#
#         for j in range(1, 31):
#             group_index = start_group + (j - 1) // 6
#             sub_index = (j - 1) % 6
#             if group_index in vars_dict:
#                 params[f'Total_Energy_{j}'] = vars_dict[f'Total_Energy_{group_index}'][sub_index]
#             else:
#                 # 处理前四个6组数据没有前面数据的情况，这里简单用0填充，可根据实际情况调整
#                 params[f'Total_Energy_{j}'] = 0
#
#         completion = client.chat.completions.create(
#             model="gpt-4o-mini-2024-07-18",
#             messages=[
#                 {"role": "system", "content": "You are an AI assistant to a building operations manager in Singapore, responsible for optimizing the energy efficiency of the Heating, Ventilation, and Air Conditioning (HVAC) system while ensuring the comfort of the occupants."},
#                 {"role": "user", "content": custom_prompt_1.format(**params)}
#             ]
#         )
#
#         respond = completion.choices[0].message
#         text = respond.content
#         file.write(f"hour {i}————————————————————————————————————————————————————————————————\n")
#
#         print(text)
#         print(f"hour {i}————————————————————————————————————————————————————————————————")
#         start_index = text.find('[') + 1
#         end_index = text.find(']')
#         if start_index != 0 and end_index != -1:
#             temp_str = text[start_index:end_index]
#             temps = [float(temp.replace(',', '')) for temp in temp_str.split()]
#             temp_hour.extend(temps)
#
# print("最终的温度列表:", temp_hour)
# print("最终的温度列表长度:", len(temp_hour))

# import os
# from openai import OpenAI
# import pandas as pd
#
#
# # openai or deepseek api
# os.environ["OPENAI_BASE_URL"] = "https://api.zhizengzeng.com/v1/"
# os.environ["OPENAI_API_KEY"] = "sk-zk22d3b63d681ab4346a61c6e66a1212d8a66d581c98c8fd"
#
# client = OpenAI()
#
#
# # 读取文件
# excel_file = pd.ExcelFile('../data/set_temperature_22.xlsx')
# # 获取指定工作表中的数据
# df = excel_file.parse('Sheet1')
#
# # 初始化字典来存储分组后的数据
# vars_dict = {}
#
# # 参与分析的列名
# columns = ['t_out', 'Energy_2', 'Energy_4', 'Energy_3', 'temperature:drybulb', 'Equip', 'Energy_5', 'Energy_1', 'light', 'occ']
#
# # 分组的数量
# num_groups = len(df) // 6
#
# for group_index in range(1, num_groups + 1):
#     start_index = (group_index - 1) * 6
#     end_index = start_index + 6
#
#     # 计算 Total_Energy
#     total_energy = []
#     for i in range(start_index, end_index):
#         energy_sum = df.loc[i, 'Energy_1'] + df.loc[i, 'Energy_2'] + df.loc[i, 'Energy_3'] + df.loc[i, 'Energy_4'] + df.loc[i, 'Energy_5']
#         total_energy.append(energy_sum)
#     vars_dict[f'Total_Energy_{group_index}'] = total_energy
#
#     for col in columns:
#         data = df[col]
#         group = data[start_index:end_index].tolist()
#         if col == 'temperature:drybulb':
#             col = 'temperature_drybulb'
#         vars_dict[f'{col}_{group_index}'] = group
#
#
# custom_prompt_1 = (
#     """
# Building Information:
# Large office (conditioned area of 46,320.38 square meters)
# Wall area: 12,183.90 square meters (window-to-wall ratio of 43.92%)
# Roof area: 3,563.11 square meters (skylight ratio of 0%)
# Openable window area: 5,350.65 square meters
# Above-ground wall area: 11,589.54 square meters
# Cooling: Water-cooled chillers with a cooling capacity of 3,959 kW
# Ventilation: Variable Air Volume (VAV) system (maximum outdoor air intake of 157.54 cubic meters per second)
#
# Current Operational Data (each value represents the situation at 10 - minute intervals):
# You will be provided with 30 consecutive data points for various parameters.
# For outdoor temperature, you have t_out_1 to t_out_30: {t_out_1} {t_out_2}... {t_out_30}
# For equipment situation, Equip_1 to Equip_30: {Equip_1} {Equip_2}... {Equip_30}
# For building's lighting, light_1 to light_30: {light_1} {light_2}... {light_30}
# For occupancy ratio, occ_1 to occ_30: {occ_1} {occ_2}... {occ_30}
# Total energy consumption for each 10 - minute interval from Total_Energy_1 to Total_Energy_30: {Total_Energy_1} {Total_Energy_2}... {Total_Energy_30}
# The last 6 temperature setpoints are temperature_drybulb_25 to temperature_drybulb_30: {temperature_drybulb_25} {temperature_drybulb_26}... {temperature_drybulb_30}
#
# Task:
# Based on the above 30 - data - point information and your knowledge of HVAC systems, analyze the trends, especially focusing on the last 6 outdoor temperatures (t_out_25 to t_out_30), and set 6 recommended temperature values for the HVAC system within the current hour. The temperature goal is that compared to when the current temperature is set at the average of the last 6 temperature setpoints (average of temperature_drybulb_25 to temperature_drybulb_30), your recommended temperature values will reduce the building's total energy consumption by 15%.
#
# Output Format:
# temp_hour=[X.X X.X X.X X.X X.X X.X]
# (6 temperature values, at 10 - minute intervals, with one decimal place precision, values within the range of 22.0 - 29.0°C)
#
# Prohibited:
# Code blocks
# Explanatory text
# """
# )
#
#
# client = OpenAI()
# temp_hour = []
# with open("../result/openai_setting22.txt", "w", encoding="utf-8") as file:
#     for i in range(1, num_groups - 4 + 1):
#         start_group = i
#         end_group = i + 4
#
#         params = {}
#         for col in columns:
#             if col == 'temperature:drybulb':
#                 col = 'temperature_drybulb'
#             for j in range(1, 31):
#                 group_index = start_group + (j - 1) // 6
#                 sub_index = (j - 1) % 6
#                 if group_index in vars_dict:
#                     params[f'{col}_{j}'] = vars_dict[f'{col}_{group_index}'][sub_index]
#                 else:
#                     # 处理前四个6组数据没有前面数据的情况，这里简单用0填充，可根据实际情况调整
#                     params[f'{col}_{j}'] = 0
#
#         for j in range(1, 31):
#             group_index = start_group + (j - 1) // 6
#             sub_index = (j - 1) % 6
#             if group_index in vars_dict:
#                 params[f'Total_Energy_{j}'] = vars_dict[f'Total_Energy_{group_index}'][sub_index]
#             else:
#                 # 处理前四个6组数据没有前面数据的情况，这里简单用0填充，可根据实际情况调整
#                 params[f'Total_Energy_{j}'] = 0
#
#         completion = client.chat.completions.create(
#             model="gpt-4o-mini-2024-07-18",
#             messages=[
#                 {"role": "system", "content": "You are an AI assistant to a building operations manager in Singapore, responsible for optimizing the energy efficiency of the Heating, Ventilation, and Air Conditioning (HVAC) system while ensuring the comfort of the occupants."},
#                 {"role": "user", "content": custom_prompt_1.format(**params)}
#             ]
#         )
#
#         respond = completion.choices[0].message
#         text = respond.content
#         file.write(f"hour {i}————————————————————————————————————————————————————————————————\n")
#
#         print(text)
#         print(f"hour {i}————————————————————————————————————————————————————————————————")
#         start_index = text.find('[') + 1
#         end_index = text.find(']')
#         if start_index != 0 and end_index != -1:
#             temp_str = text[start_index:end_index]
#             temps = [float(temp.replace(',', '')) for temp in temp_str.split()]
#             temp_hour.extend(temps)
#
# print("最终的温度列表:", temp_hour)
# print("最终的温度列表长度:", len(temp_hour))
