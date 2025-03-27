# Project Introduction
This project mainly focuses on the application of LLM (Large Language Model) in the HVAC (Heating, Ventilation, and Air Conditioning) field. The code has implemented a series of functions related to HVAC system analysis, model calling, etc. However, due to some environmental codes and data not being open-sourced, there are usage limitations.

# Installation of Dependencies
The Python packages that the project depends on can be installed through the `requirements.txt` file. Execute the following command in the terminal:
```bash
pip install -r requirements.txt
```

# Notes
1. **Some Code Not Open-Sourced**: The relevant content in the `try` folder of the project cannot provide all the code directly because it is not open-sourced. If you have relevant requirements, you can contact the project maintainer for further consultation. Currently, interaction with EnergyPlus is not possible.
2. **API Calling**: You can add your own API key for model calling. Find the position in the code where the API key needs to be entered, fill in your own valid API key, and then you can use the model calling function normally.

# Instructions for Using the Code
The steps to run the code are as follows:
1. Ensure that all dependencies have been installed.
2. Add a valid API key to the specified position in the code.
3. Open the terminal and navigate to the directory where the code is located.
4. Perform tasks on the `prompt` in the `py` files of `model` or `model_rag`; and select whether to use RAG in the `import` statement in `test_final`.
5. Run the main program file, for example:
```bash
python test_final.py
```

# If you have any questions or suggestions, you are welcome to raise them in the [https://github.com/vogtsw/llm-building/issues](https://github.com/vogtsw/llm-building/issues) of the project. 
