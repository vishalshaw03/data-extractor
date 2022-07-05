import pandas as pd
from helpers.utils import (
    coloredInput,
    checkFilePath,
    errorMessage,
    getChoice,
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


def saveFile(df: pd.DataFrame, file_path: str = None):

    if not getChoice("\nDo you want to save the data in file"):
        return

    output_file_path = file_path

    if not output_file_path:
        output_file_path = coloredInput("Enter output file path : ")
        if not output_file_path:
            errorMessage("Invalid path! Using default settings")
            return
            # output_file_path = "output.xlsx"

    output_file_path = checkFilePath(output_file_path)

    # saving the excel
    df.to_excel(r"{}".format(output_file_path))

    successMessage("DataFrame is written to Excel File successfully.")


def showSuggestion(suggestions_df: pd.DataFrame):
    if not suggestions_df.empty:

        cols = suggestions_df.columns.to_list()
        show_fields = ["Name", "Email"]

        if "Contact" in cols:
            show_fields = show_fields + ["Contact"]

        if "Row_no" in cols:
            show_fields = show_fields + ["Row_no"]

        print("--" * 50)
        infoMessage("\n--Suggestions--")
        print(suggestions_df[show_fields].to_markdown())


def printList(df: pd.DataFrame):
    if df.empty:
        warningMessage("Empty List")

    cols = df.columns.to_list()
    show_fields = ["Name", "Roll_no", "Email", "Email_Match"]

    if "Contact" in cols and "Contact_Match" in cols:
        show_fields = show_fields + ["Contact", "Contact_Match"]

    print(df[show_fields].to_markdown())
