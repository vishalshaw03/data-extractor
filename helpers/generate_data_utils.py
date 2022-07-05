import pandas as pd
from helpers.output import printMenuOptions
from helpers.utils import (
    coloredInput,
    checkFilePath,
    errorMessage,
    infoMessage,
)


def printInstructions():
    print("")
    print("-" * 30, end="")
    infoMessage(
        "\n1. Enter '-1' anytime to exit\n2. You can also use column no as input like 1, 2\n Use ',' separated values to have multiple column values"
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

        if "," in input_field_name:
            f_names = input_field_name.split(",")
            f_names = [s.strip() for s in f_names]  # trimming spaces

            allColumnsExists = True
            f_list = []

            for e in f_names:
                if e.isnumeric():
                    if column_no_exists(e, valid_range):
                        f_list.append(columns[int(e) - 1])
                    else:
                        errorMessage("{} | No such columns present!".format(str(e)))
                        allColumnsExists = False
                        break

                elif e in columns:
                    f_list.append(e)
                else:
                    errorMessage("No such columns present!")
                    allColumnsExists = False
                    break
            if allColumnsExists:
                return f_list

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
    # print(input_df_columns, end="\n\n")
    printMenuOptions(input_df_columns)

    if len(output_fields) > 0:
        input_field_only = True
        n = len(output_fields)
    else:
        n = int(coloredInput("\nEnter no. of fields : "))

    field_names_map = {key: None for key in output_fields}

    if input_field_only:
        infoMessage("\n--You can use 'Enter' for default--\n")

        for field_name in output_fields:
            msg = "\nEnter input field-name(s) for {} (default {}) : ".format(
                field_name, field_name
            )

            name = read_input_field_name(
                msg,
                input_df_columns,
                field_name,
            )

            if not name:
                return None

            field_names_map[field_name] = name

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

            field_names_map[input_field_name] = output_field_name

            infoMessage("{} ----> {}\n".format(input_field_name, output_field_name))

    return field_names_map


def joinValues(x: pd.Series):
    values = x.values
    values = list(filter(None, values))
    values = [int(x) if type(x) == float else x for x in values]

    return ",".join(map(str, values))
