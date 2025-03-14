import os
from openai import OpenAI
import pandas as pd


os.environ["OPENAI_BASE_URL"] = ""
os.environ["OPENAI_API_KEY"] = ""

client = OpenAI()


excel_file = pd.ExcelFile('../data/set_temperature_22.xlsx')

df = excel_file.parse('Sheet1')

vars_dict = {}


columns = ['t_out', 'Energy_2', 'Energy_4', 'Energy_3', 'temperature:drybulb', 'Equip', 'Energy_5', 'Energy_1', 'light', 'occ']


num_groups = len(df) // 6

for group_index in range(1, num_groups + 1):
    start_index = (group_index - 1) * 6
    end_index = start_index + 6


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

                    params[f'{col}_{j}'] = 0

        for j in range(1, 31):
            group_index = start_group + (j - 1) // 6
            sub_index = (j - 1) % 6
            if group_index in vars_dict:
                params[f'Total_Energy_{j}'] = vars_dict[f'Total_Energy_{group_index}'][sub_index]
            else:

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






