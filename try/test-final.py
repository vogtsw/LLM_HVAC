import sys
sys.path.append('../model')

from model import temp_hour  # 从 model.py 中导入 final_output 数组

print(temp_hour)


from controllables.energyplus import (
    System,
    # WeatherModel,
    # Report,
    Actuator,
    OutputVariable,
)


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

try_folder = os.path.dirname(os.path.abspath(__file__))


result_folder = os.path.join(os.path.dirname(try_folder), 'result')


if not os.path.exists(result_folder):
    os.makedirs(result_folder)



data_to_save = a.data[:len(temp_hour)]
value_to_save = a.value[:len(temp_hour)]


out1 = pd.DataFrame(data_to_save, columns=['Time'])
out1_path = os.path.join(result_folder, 'result-2.csv')
out1.to_csv(out1_path)


out2 = pd.DataFrame(value_to_save)
out2_path = os.path.join(result_folder, 'result-openai-rag-15% test.csv')
out2.to_csv(out2_path)