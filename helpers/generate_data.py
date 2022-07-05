import pandas as pd
from config.constants import REFERENCE_DATA_FILE
from helpers.generate_data_utils import input_file, joinValues, read_field_names
from helpers.output import printDataFrame, saveFile
from helpers.utils import reset_index


def generateReferenceData(
    input_df: pd.DataFrame, output_fields: list, field_names_map: dict
):
    filtered_df = pd.DataFrame()

    filtered_df = pd.DataFrame(columns=output_fields)
    input_df.fillna("", inplace=True)

    for (key, value) in field_names_map.items():
        if type(value) == str:
            filtered_df[key] = input_df[value]
        elif type(value) == list:
            filtered_df[key] = input_df[value].apply(joinValues, axis=1)

    return filtered_df


def generate_data(
    showSaveFile: bool = False,
    showPrintOption: bool = True,
):

    input_df = pd.DataFrame()
    output_fields = []
    for_reference_data = False
    field_names_map = {}

    input_df = input_file()
    if input_df.empty:
        return

    print("\n1. For Reference Data\t\t2. For Custom Data\n")
    choice = input("Enter your choice : ")

    match choice:
        case "1":
            for_reference_data = True

        case "2":
            return

        case _:
            return

    if for_reference_data:
        output_fields = ["Name", "Roll_no", "Email", "Contact"]

    field_names_map = read_field_names(input_df, output_fields=output_fields)
    if not field_names_map:
        return

    filtered_df = generateReferenceData(input_df, output_fields, field_names_map)

    # print(filtered_df)
    reset_index(filtered_df)

    if showPrintOption:
        printDataFrame(filtered_df)

    if not showSaveFile:
        return filtered_df

    if for_reference_data:
        saveFile(filtered_df, file_path=REFERENCE_DATA_FILE)
    else:
        saveFile(filtered_df)


def generate_data_from_extract(df: pd.DataFrame = pd.DataFrame()):
    if df.empty:
        return

    cols = df.columns.to_list()
    filtered_df = df[cols]
    reset_index(filtered_df)

    saveFile(filtered_df)
