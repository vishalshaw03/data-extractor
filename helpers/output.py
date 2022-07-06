import pandas as pd
from helpers.utils import (
    coloredInput,
    checkFilePath,
    errorMessage,
    getChoice,
    getRowNos,
    infoMessage,
    successMessage,
    warningMessage,
)

printDataMenu = ["Default", "Long", "Back"]


def printMenuOptions(menu: list):
    print("")
    for i in range(0, len(menu)):
        print("{}. {}".format(str(i + 1), menu[i]))

    print("")


def printDataFrame(df: pd.DataFrame):

    if not getChoice("Print DataFrame"):
        return

    printMenuOptions(printDataMenu)

    choice = coloredInput("Enter your choice : ")

    match choice:
        case "1":
            print(df)
        case "2":
            print(df.to_markdown())


def getColumnsToSave(df: pd.DataFrame):
    cols = df.columns.tolist()
    filtered_columns = []
    infoMessage("--SELECT COLUMNS TO BE PRESENT IN THE EXCEL--")
    printMenuOptions(cols)

    input_str = coloredInput("\nEnter column nos. (comma separated): ")

    if input_str.lower() == "all":
        return cols

    valid_range = df.index.to_list()
    row_nos = getRowNos(input_str, valid_range)

    for i in row_nos:
        filtered_columns.append(cols[i])

    return filtered_columns


def saveFile(df: pd.DataFrame, file_path: str = None):

    if not getChoice("\nDo you want to save the data in file"):
        return

    cols = df.columns.tolist()
    if not file_path:
        cols = getColumnsToSave(df)

    output_file_path = file_path

    if not output_file_path:
        output_file_path = coloredInput("Enter output file path : ")
        if not output_file_path:
            errorMessage("Invalid path! Using default settings")
            return
            # output_file_path = "output.xlsx"

    output_file_path = checkFilePath(output_file_path)

    filtered_df = df[cols]

    # saving the excel
    filtered_df.to_excel(r"{}".format(output_file_path))

    successMessage("DataFrame is written to Excel File successfully.")


def showSuggestion(suggestions_df: pd.DataFrame):
    if not suggestions_df.empty:

        cols = suggestions_df.columns.to_list()
        fields = ["Name"]
        match_fields = ["Name_Match"]

        if "Email" in cols:
            fields.append("Email")
            match_fields.append("Email_Match")

        if "Contact" in cols:
            fields.append("Contact")
            match_fields.append("Contact_Match")

        if "Row_no" in cols:
            fields.append("Row_no")

        show_fields = fields + match_fields

        print("--" * 50)
        infoMessage("\n--Suggestions--")
        print(suggestions_df[show_fields].to_markdown())


def printList(df: pd.DataFrame):
    if df.empty:
        warningMessage("Empty List")

    df.Roll_no = df.Roll_no.map(lambda x: x if type(x) == str else "{:.0f}".format(x))

    cols = df.columns.to_list()
    show_fields = ["Name", "Roll_no", "Email", "Email_Match"]

    if "Contact" in cols and "Contact_Match" in cols:
        show_fields = show_fields + ["Contact", "Contact_Match"]

    print(df[show_fields].to_markdown())
