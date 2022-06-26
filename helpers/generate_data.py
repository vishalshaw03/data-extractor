import pandas as pd
from config.constants import REFERENCE_DATA_FILE
from helpers.output import printDataFrame, saveFile
from helpers.utils import (
    coloredInput,
    checkFilePath,
    errorMessage,
    infoMessage,
    reset_index,
)


def printInstructions():
    print("")
    print("-" * 30, end="")
    infoMessage(
        "\n1. Enter '-1' anytime to exit\n2. You can also use column no as input like 1, 2"
    )
    print("-" * 30)


def input_file():

    df = pd.DataFrame()

    input_file_path = coloredInput("Enter the input_file_path : ")
    if not input_file_path:
        errorMessage("Invalid path!")
    else:
        input_file_path = checkFilePath(input_file_path)

        sheet_name = coloredInput("Enter the sheet_name ('Enter' for default) : ")

        if sheet_name:
            df = pd.read_excel(input_file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(r"{}".format(input_file_path))

    return df


def column_no_exists(field_no: str, valid_range: range):
    if not field_no.isdigit():
        return False

    if (int(field_no) - 1) in valid_range:
        return True

    return False


def read_input_field_name(message: str, columns: list, output_field_name: str = None):
    valid_range = range(0, len(columns))

    while True:
        input_field_name = coloredInput(message)

        if input_field_name == "-1":
            return None

        if not input_field_name and output_field_name:
            input_field_name = output_field_name

        if column_no_exists(input_field_name, valid_range):
            field_name = columns[int(input_field_name) - 1]
            return field_name
        elif input_field_name in columns:
            return input_field_name
        else:
            errorMessage("No such columns present!")


def read_field_names(input_df: pd.DataFrame, output_fields: list = []):
    input_field_only = False

    printInstructions()

    input_df_columns = input_df.columns.to_list()
    infoMessage("\n--Available Columns--")
    print(input_df_columns, end="\n\n")

    if len(output_fields) > 0:
        input_field_only = True
        n = len(output_fields)
    else:
        n = int(coloredInput("\nEnter no. of fields : "))

    input_field_names = []
    output_field_names = output_fields

    if input_field_only:
        infoMessage("\n--You can use 'Enter' for default--\n")

        for field_name in output_field_names:
            msg = "\nEnter input field-name for {} (default {}) : ".format(
                field_name, field_name
            )

            name = read_input_field_name(
                msg,
                input_df_columns,
                field_name,
            )

            if not name:
                return None

            input_field_names.append(name)

            infoMessage("{} ----> {}\n".format(name, field_name))

    else:
        for i in range(0, n):
            input_field_name = read_input_field_name(
                "\nEnter Name of field no {} : ".format(str(i + 1)), input_df_columns
            )

            if not input_field_name:
                return None

            output_field_name = coloredInput("Enter output field name : ")

            if not output_field_name:
                output_field_name = input_field_name

            input_field_names.append(input_field_name)
            output_field_names.append(output_field_name)

            infoMessage("{} ----> {}\n".format(input_field_name, output_field_name))

    return (
        input_field_names,
        output_field_names,
    )


def generate_data(
    df: pd.DataFrame = pd.DataFrame(),
    for_extract: bool = False,
    showSaveFile: bool = False,
    showPrintOption: bool = True,
):

    input_df = pd.DataFrame()
    output_fields = []
    for_reference_data = False
    input_field_names = []
    output_field_names = []

    if for_extract:
        if df.empty:
            return

        input_df = df
        cols = df.columns.to_list()
        input_field_names = cols
        output_field_names = cols

    else:
        input_df = input_file()
        if input_df.empty:
            return

        print("\n1. For Reference Data\t\t2. For Custom Data\n")
        choice = input("Enter your choice : ")

        match choice:
            case "1":
                for_reference_data = True

            case "2":
                pass

            case _:
                return

        if for_reference_data:
            output_fields = ["Name", "Roll_no", "Email_Address_1", "Email_Address_2"]

        res = read_field_names(input_df, output_fields=output_fields)
        if not res:
            return
        input_field_names, output_field_names = res

    filtered_df = input_df[input_field_names]
    filtered_df.columns = output_field_names
    reset_index(filtered_df)

    if showPrintOption:
        printDataFrame(filtered_df)

    if not showSaveFile:
        return filtered_df

    if for_reference_data:
        saveFile(filtered_df, file_path=REFERENCE_DATA_FILE)
    else:
        saveFile(filtered_df)
