import sys
sys.path.append('../model')  # 将'model' 文件夹添加到系统路径

# from model import temp_hour  # 从 model.py 中导入 final_output 数组
temp_hour=[24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.2, 24.0, 23.8, 23.5, 23.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 25.5, 25.0, 24.8, 24.5, 24.0, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 25.0, 25.0, 25.0, 24.8, 24.5, 24.5, 26.1, 26.0, 25.9, 25.8, 25.7, 25.6, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 24.2, 24.2, 24.1, 24.1, 24.0, 24.0, 23.2, 23.2, 23.4, 23.5, 23.5, 23.5, 24.5, 24.5, 24.5, 24.0, 24.0, 24.0, 24.6, 24.6, 24.5, 24.5, 24.4, 24.4, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.1, 24.1, 24.1, 24.2, 24.2, 24.2, 23.2, 23.5, 23.8, 24.0, 24.3, 24.5, 22.9, 22.7, 22.5, 22.3, 22.1, 21.9, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 24.5, 24.4, 24.3, 24.2, 24.1, 24.0, 24.1, 24.1, 24.1, 24.1, 24.1, 24.1, 24.5, 24.5, 24.1, 23.8, 23.8, 23.8, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 22.7, 22.8, 23.0, 23.2, 23.3, 23.5, 23.5, 23.5, 23.5, 23.0, 23.0, 22.5, 24.5, 24.5, 24.6, 24.6, 24.7, 24.7, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 23.3, 23.3, 23.2, 23.2, 23.1, 23.1, 24.5, 24.5, 24.4, 24.4, 24.3, 24.3, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 23.7, 23.7, 23.6, 23.5, 23.5, 23.4, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 23.5, 23.4, 23.3, 23.2, 23.1, 23.0, 22.5, 22.5, 22.7, 22.7, 22.8, 22.8, 24.5, 24.5, 24.4, 24.4, 24.3, 24.3, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.4, 24.0, 24.0, 23.6, 23.5, 23.5, 24.6, 24.4, 24.2, 24.1, 24.0, 23.9, 23.5, 23.5, 23.5, 23.4, 23.4, 23.3, 24.6, 24.6, 24.5, 24.5, 24.4, 24.4, 23.3, 23.5, 23.7, 23.5, 23.2, 23.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.2, 24.2, 24.2, 24.2, 24.2, 24.2, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 23.8, 23.5, 23.7, 23.6, 23.4, 23.2, 25.5, 25.5, 25.5, 25.5, 25.5, 25.5, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 23.4, 23.4, 23.5, 23.5, 23.6, 23.6, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.4, 24.4, 24.3, 24.3, 24.2, 24.2, 24.5, 24.4, 24.3, 24.2, 24.1, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.3, 24.2, 24.1, 24.0, 23.9, 23.8, 23.0, 23.0, 23.5, 23.5, 24.0, 24.0, 23.5, 23.4, 23.3, 23.2, 23.1, 23.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 24.0, 24.0, 23.5, 23.5, 23.1, 23.1, 23.2, 23.2, 23.3, 23.3, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 22.0, 22.3, 22.6, 22.9, 23.2, 23.5, 24.6, 24.4, 24.2, 24.0, 23.8, 23.6, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.0, 24.0, 24.0, 24.0, 23.5, 23.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.2, 24.5, 24.3, 24.0, 23.8, 23.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 24.5, 24.0, 23.5, 23.0, 22.5, 22.0, 25.4, 25.3, 25.2, 25.1, 25.0, 24.9, 24.5, 24.3, 24.1, 24.0, 23.8, 23.7, 23.8, 23.8, 23.8, 23.8, 23.8, 23.8, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 23.9, 23.8, 23.7, 23.6, 23.5, 23.4, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 23.5, 23.3, 23.1, 22.9, 22.7, 22.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 27.0, 26.8, 26.6, 26.4, 26.2, 26.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 23.6, 23.6, 23.5, 23.5, 23.4, 23.4, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.5, 24.5, 24.0, 24.0, 23.5, 23.5, 24.5, 24.5, 24.3, 24.3, 24.0, 24.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.5, 24.5, 24.4, 24.4, 24.3, 24.3, 22.8, 22.5, 22.5, 22.4, 22.4, 22.3, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.6, 24.4, 24.1, 24.1, 24.3, 24.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.7, 24.5, 24.5, 24.3, 24.3, 24.0, 24.3, 24.0, 23.8, 23.5, 23.2, 23.0, 24.6, 24.6, 24.5, 24.5, 24.4, 24.4, 25.0, 25.0, 25.0, 25.0, 24.5, 24.5, 23.7, 23.5, 23.5, 23.3, 23.3, 23.0, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.4, 24.0, 23.6, 23.2, 23.0, 22.6, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.8, 24.5, 24.2, 24.0, 23.8, 23.5, 24.2, 24.2, 24.2, 24.2, 24.2, 24.2, 24.9, 24.8, 24.7, 24.6, 24.5, 24.4, 23.4, 23.4, 23.3, 23.3, 23.2, 23.1, 24.5, 24.5, 24.0, 24.0, 23.5, 23.5, 24.5, 24.5, 24.5, 24.0, 24.0, 24.0, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 22.5, 22.5, 23.0, 23.0, 23.5, 23.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 23.8, 23.7, 23.6, 23.5, 23.4, 23.3, 23.1, 23.3, 23.5, 23.7, 23.9, 24.1, 23.9, 23.8, 23.8, 23.7, 23.6, 23.6, 23.7, 23.6, 23.5, 23.5, 23.4, 23.3, 24.3, 24.1, 23.9, 24.0, 23.8, 23.5, 24.4, 24.2, 24.0, 23.8, 23.6, 23.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.5, 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 24.5, 24.5, 24.5, 24.0, 24.0, 23.5, 24.7, 24.7, 24.6, 24.6, 24.5, 24.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.6, 24.4, 24.2, 24.0, 23.8, 23.6, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0]
# 现在你可以使用 final_output 数组了
# print(temp_hour)


from controllables.energyplus import (
    System,
    # WeatherModel,
    # Report,
    Actuator,
    OutputVariable,
)

# from energyplus.dataset.basic import dataset as _epds_
from controllables.energyplus.events import Event

from controllables.core import TemporaryUnavailableError

from controllables.core.tools.gymnasium import (
    DictSpace,
    BoxSpace,
    Agent,
)

import gymnasium as _gymnasium_
import numpy as _numpy_

import os
resolve = lambda *xs: os.path.join(
    os.path.dirname(__file__),
    *xs,
)


class my_env():
    def __init__(self) -> None:
        self.world = world = System(
            building='Small office-1A-Long.idf',
            # world='tmp_timestep 10 min.idf',
            weather='USA_FL_Miami.722020_TMY2.epw',
            repeat=False,

        ).add('logging:progress')

        env = Agent(dict(
            action_space=DictSpace({
                'Thermostat': BoxSpace(
                    low=22., high=30.,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[Actuator.Ref(
                    type='Schedule:Compact',
                    control_type='Schedule Value',
                    key='Always 26',
                )])
            }),
            observation_space=DictSpace({
                'temperature:drybulb': BoxSpace(
                    low=-_numpy_.inf, high=+_numpy_.inf,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[OutputVariable.Ref(
                    type='Zone Mean Air Temperature',
                    key='Perimeter_ZN_1 ZN',
                )]),
                't_out': BoxSpace(
                    low=-_numpy_.inf, high=+_numpy_.inf,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[OutputVariable.Ref(
                    type='Site Outdoor Air Drybulb Temperature',
                    key='Environment',
                )]),
                'occ': BoxSpace(
                    low=-_numpy_.inf, high=+_numpy_.inf,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[OutputVariable.Ref(
                    type='Schedule Value',
                    key='Small Office Bldg Occ',
                )]),
                'light': BoxSpace(
                    low=-_numpy_.inf, high=+_numpy_.inf,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[OutputVariable.Ref(
                    type='Schedule Value',
                    key='Office Bldg Light',
                )]),
                'Equip': BoxSpace(
                    low=-_numpy_.inf, high=+_numpy_.inf,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[OutputVariable.Ref(
                    type='Schedule Value',
                    key='Small Office Bldg Equip',
                )]),
                'Energy_1': BoxSpace(
                    low=-_numpy_.inf, high=+_numpy_.inf,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[OutputVariable.Ref(
                    type='Cooling Coil Total Cooling Rate',
                    key='CORE_ZN ZN PSZ-AC-1 1SPD DX AC CLG COIL 34KBTU/HR 9.7SEER',
                )]),
                'Energy_2': BoxSpace(
                    low=-_numpy_.inf, high=+_numpy_.inf,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[OutputVariable.Ref(
                    type='Cooling Coil Total Cooling Rate',
                    key='PERIMETER_ZN_1 ZN PSZ-AC-2 1SPD DX AC CLG COIL 33KBTU/HR 9.7SEER',
                )]),
                'Energy_3': BoxSpace(
                    low=-_numpy_.inf, high=+_numpy_.inf,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[OutputVariable.Ref(
                    type='Cooling Coil Total Cooling Rate',
                    key='PERIMETER_ZN_2 ZN PSZ-AC-3 1SPD DX AC CLG COIL 23KBTU/HR 9.7SEER',
                )]),
                'Energy_4': BoxSpace(
                    low=-_numpy_.inf, high=+_numpy_.inf,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[OutputVariable.Ref(
                    type='Cooling Coil Total Cooling Rate',
                    key='PERIMETER_ZN_3 ZN PSZ-AC-4 1SPD DX AC CLG COIL 33KBTU/HR 9.7SEER',
                )]),
                'Energy_5': BoxSpace(
                    low=-_numpy_.inf, high=+_numpy_.inf,
                    dtype=_numpy_.float32,
                    shape=(),
                ).bind(world[OutputVariable.Ref(
                    type='Cooling Coil Total Cooling Rate',
                    key='PERIMETER_ZN_4 ZN PSZ-AC-5 1SPD DX AC CLG COIL 25KBTU/HR 9.7SEER',
                )]),
            }),
        ))
        self.data = []
        self.value = []

        ################################################# 新增一个列表来存储需要依次读取的数字
        self.temp_values =temp_hour

        #################################################
        self.current_index = 0

        @self.world.on(Event.Ref('end_zone_timestep_after_zone_reporting', include_warmup=False))
        def _(_):
            try:

                self.data.append(self.world['wallclock:calendar'].value)
                self.value.append(env.observe())
                env.action.value = {
                    'Thermostat': self.p(),

                }



            except TemporaryUnavailableError:
                pass

            # except Exception:
            #     # TODO
            #     pass

            try:
                # self.value.append(env.observe())
                ddd = 1
                # self.col = list(env.observe())
            except TemporaryUnavailableError:
                pass

    def p(self):
        # 获取当前索引对应的数字
        result = self.temp_values[self.current_index]
        # 更新索引，当索引超出列表长度时，再从头开始循环
        self.current_index = (self.current_index + 1) % len(self.temp_values)
        return result


a = my_env()
a.world.start().wait()
import pandas as pd

# out = pd.DataFrame(a.data, columns=['Time'])
# out.to_csv(resolve('result-2.csv'))
# out = pd.DataFrame(a.value)
# out.to_csv(resolve('result-deepseek_llama test.csv'))


# import os
# import pandas as pd

# 获取当前脚本所在目录（即 try 文件夹路径）
try_folder = os.path.dirname(os.path.abspath(__file__))

# 获取与 try 文件夹平行的 result 文件夹路径
result_folder = os.path.join(os.path.dirname(try_folder), 'result')

# 检查 result 文件夹是否存在，如果不存在则创建
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# 假设 a 是一个包含 data 和 value 属性的对象
# 这里假设 a 已经正确定义，若实际代码中未定义，需要先定义它


data_to_save = a.data[:len(temp_hour)]
value_to_save = a.value[:len(temp_hour)]

# 保存 a.data 到 result-2.csv
out1 = pd.DataFrame(data_to_save, columns=['Time'])
out1_path = os.path.join(result_folder, 'result-2.csv')
out1.to_csv(out1_path)

# 保存 a.value 到 result-deepseek_llama test.csv
out2 = pd.DataFrame(value_to_save)
out2_path = os.path.join(result_folder, 'result-openai-rag-15% test.csv')
out2.to_csv(out2_path)