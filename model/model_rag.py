import os
from openai import OpenAI
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser

# openai or deepseek api
os.environ["OPENAI_BASE_URL"] = ""
os.environ["OPENAI_API_KEY"] = ""

client = OpenAI()


df = pd.read_csv('../data/result-11-22.csv')


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
Building Information:
The small office building has a total floor area of 511.16 m², with a net conditioned area of 511.16 m² and no unconditioned area, meaning 100% of the building is conditioned space. The HTML file doesn't explicitly state the number of zones or rooms, but DOE reference models usually structure a single - story small office with 3 zones per floor (like perimeter and core zones), and to get the exact zone breakdown, zone summary tables, IDF or input schema (such as .idf or .epJSON) are needed. The current HTML report lacks explicit information on wall or roof insulation levels (R/U - values), window - to - wall ratio (WWR), and glazing properties (U - value, SHGC), but since the simulation uses the DOE Reference Small Office for ASHRAE 169 - 2006 Climate Zone 1A (Miami), we can infer a WWR of ~33%, roof insulation of ~R - 20, wall insulation of ~R - 13, and double - pane, low - SHGC glazing suitable for hot - humid climates. The HTML file doesn't show thermal mass details (such as material types, density, heat capacity), yet we can infer internal heat gains from energy use. Over the simulation period, interior lighting gains are 5.36 GJ, interior equipment gains are 6.35 GJ, and fan (circulation heat) gains are 5.36 GJ. These internal heat gains significantly affect cooling loads and can be modulated in demand response control.

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

custom_prompt_2 = (
    """
Building Information:
The small office building has a total floor area of 511.16 m², with a net conditioned area of 511.16 m² and no unconditioned area, meaning 100% of the building is conditioned space. The HTML file doesn't explicitly state the number of zones or rooms, but DOE reference models usually structure a single - story small office with 3 zones per floor (like perimeter and core zones), and to get the exact zone breakdown, zone summary tables, IDF or input schema (such as .idf or .epJSON) are needed. The current HTML report lacks explicit information on wall or roof insulation levels (R/U - values), window - to - wall ratio (WWR), and glazing properties (U - value, SHGC), but since the simulation uses the DOE Reference Small Office for ASHRAE 169 - 2006 Climate Zone 1A (Miami), we can infer a WWR of ~33%, roof insulation of ~R - 20, wall insulation of ~R - 13, and double - pane, low - SHGC glazing suitable for hot - humid climates. The HTML file doesn't show thermal mass details (such as material types, density, heat capacity), yet we can infer internal heat gains from energy use. Over the simulation period, interior lighting gains are 5.36 GJ, interior equipment gains are 6.35 GJ, and fan (circulation heat) gains are 5.36 GJ. These internal heat gains significantly affect cooling loads and can be modulated in demand response control.

Current Operational Data (each value represents the situation at 10 - minute intervals):
You will be provided with 30 consecutive data points for various parameters.
For outdoor temperature, you have t_out_1 to t_out_30: {t_out_1} {t_out_2}... {t_out_30}
For equipment situation, Equip_1 to Equip_30: {Equip_1} {Equip_2}... {Equip_30}
For building's lighting, light_1 to light_30: {light_1} {light_2}... {light_30}
For occupancy ratio, occ_1 to occ_30: {occ_1} {occ_2}... {occ_30}
Total energy consumption for each 10 - minute interval from Total_Energy_1 to Total_Energy_30: {Total_Energy_1} {Total_Energy_2}... {Total_Energy_30}
The last 6 temperature setpoints are temperature_drybulb_25 to temperature_drybulb_30: {temperature_drybulb_25} {temperature_drybulb_26}... {temperature_drybulb_30}

Task:
Based on the above 30 - data - point information and your knowledge of HVAC systems, analyze the trends, especially focusing on the last 6 outdoor temperatures (t_out_25 to t_out_30), and set 6 recommended temperature values for the HVAC system within the current hour. The temperature goal is that compared to when the current temperature is set at the average of the last 6 temperature setpoints (average of temperature_drybulb_25 to temperature_drybulb_30), your recommended temperature values will let the building's total energy consumption close to 17000 each timer.
Output Format:
temp_hour=[X.X X.X X.X X.X X.X X.X]
(6 temperature values, at 10 - minute intervals, with one decimal place precision, values within the range of 22.0 - 29.0°C)

Prohibited:
Code blocks
Explanatory text
"""
)


file_path = '../data/rag.csv'
data = pd.read_csv(file_path)


def generate_sentence_english(row):
    return f"At NTU, during the period {row['Date/Time']}, the outdoor temperature was {row['Environment Temperature']}°C. When the HVAC system was set to {row['Setting Temperature']}°C, the energy consumption during this period was {row['Electricity']} joules."


data['Generated Sentence (English)'] = data.apply(generate_sentence_english, axis=1)


output_file_path_english = '/kaggle/working/modified_data_with_english_sentences.csv'
data.to_csv(output_file_path_english, index=False)


data_with_english = pd.read_csv(output_file_path_english)
english_sentences = data_with_english['Generated Sentence (English)'].tolist()


combined_text = " ".join(english_sentences)

persist_directory = "embedding"


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
print("Splitting text into chunks...")
splits = text_splitter.split_text(combined_text)


if os.path.exists(persist_directory):

    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())
else:

    print("Embedding text...")
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(
        texts=[text for text in tqdm(splits, desc="Embedding")],
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectorstore.persist()

retriever = vectorstore.as_retriever()
print("Retriever created.")


prompt = PromptTemplate.from_template(
    """
{context}
{question}
"""
)

# LLM
llm = ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0)

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

temp_hour = []
with open("/kaggle/working/openai_setting22.txt", "w", encoding="utf-8") as file:
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

        formatted_prompt = custom_prompt_1.format(**params)
        respond = rag_chain.invoke(formatted_prompt)
        text = respond
        file.write(f"hour {i}————————————————————————————————————————————————————————————————\n")
        file.write(text + "\n")

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

