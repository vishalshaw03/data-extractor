import pandas as pd
from config.constants import REFERENCE_DATA_FILE
from helpers.utils import checkFilePath, coloredInput, errorMessage, warnRefData


def readData():

    input_file_path = coloredInput("Enter the input_file_path : ")
    if not input_file_path:
        errorMessage("Invalid path!")
        return pd.DataFrame(), pd.DataFrame()

    input_file_path = checkFilePath(input_file_path)

    sheet_name = input("Enter the sheet_name ('Enter' for default) : ")

    input_df = pd.DataFrame()

    if sheet_name:
        input_df = pd.read_excel(r"{}".format(input_file_path), sheet_name=sheet_name)
    else:
        input_df = pd.read_excel(r"{}".format(input_file_path))

    # print(input_df.to_markdown())
    # print(input_df)

    warnRefData(REFERENCE_DATA_FILE)
    ref_data_df = pd.read_excel(r"{}".format(REFERENCE_DATA_FILE))

    # print(ref_data_df)

    return input_df, ref_data_df


def readInstitutes():
    inst = input("Enter the Institutes (comma ',' separated) : \n")
    if not inst:
        return []

    temp = inst.split(",")
    institutes = list(map(lambda x: x.strip(), temp))

    return institutes
