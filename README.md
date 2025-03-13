

### 项目名称：大语言模型在建筑物HVAC系统上能耗控制的研究

#### 项目简介
本项目主要围绕 LLM（大语言模型）在 HVAC（暖通空调）领域的应用展开。代码实现了一系列与 HVAC 系统分析、模型调用等相关的功能，但部分环境代码和数据因未开源存在使用限制。


#### 安装依赖
项目依赖的 Python 包可以通过 `requirements.txt` 文件进行安装，在终端中执行以下命令：
```bash
pip install -r requirements.txt
```


#### 注意事项
1. **部分代码未开源**：项目中 `try` 文件夹相关内容因未开源，无法直接提供全部代码。如果你有相关需求，可联系项目维护者进一步咨询。目前无法进行对energyplus的交互。
2. **部分数据未开源**：`data` 文件夹中的部分数据涉及建筑物信息，出于保密原因未进行开源。若你有合适的使用场景和权限，可以自行准备相关数据进行替换。
3. **API 调用**：你可以自己添加 API 密钥进行模型调用。在代码中找到需要输入 API 密钥的位置，将你自己的有效 API 密钥填入，即可正常使用模型调用功能。

#### 代码使用说明


本项目代码主要包含以下几个部分：
- **数据处理模块**：负责读取和处理 `data` 文件夹中的数据。
- **模型调用模块**：通过添加的 API 密钥调用大语言模型进行相关计算。
- **结果展示模块**：将模型计算的结果进行可视化展示或保存到文件中。

运行代码的步骤如下：
1. 确保已经安装了所有依赖项。
2. 添加有效的 API 密钥到代码中指定的位置。
3. 打开终端，进入代码所在的目录。
4. 运行主程序文件，例如：
```bash
python model.py
```

#### 贡献与反馈
如果你对本项目感兴趣，可以通过以下方式进行贡献：
- 提交代码改进建议或 bug 报告。
- 提供新的功能需求或想法。

若你有任何问题或建议，欢迎在项目的 [https://github.com/vogtsw/llm-building/issues] 中提出。

