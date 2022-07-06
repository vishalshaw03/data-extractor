import pandas as pd
from helpers.output import printList, printMenuOptions, showSuggestion
from helpers.utils import (
    coloredInput,
    errorMessage,
    getChoice,
    getRowNos,
    infoMessage,
    printHeading,
)

basicModifyMenu = ["Back", "Remove rows"]
suggestionMenu = ["Add from suggestions"]


def print_modify_menu(showSuggestionOptions):
    menu = basicModifyMenu
    if showSuggestionOptions:
        menu = basicModifyMenu + suggestionMenu

    printMenuOptions(menu)


def printCurrentState(df: pd.DataFrame, suggestions_df: pd.DataFrame):
    printHeading("CURRENT LIST", color="green-bg")
    printList(df)
    showSuggestion(suggestions_df)
    print("\n")


def show_modifying_rows(df: pd.DataFrame, indexes: list, modify_type: str):

    items = df.loc[df.index.isin(indexes)]

    if items.empty:
        return

    if modify_type == "add":
        infoMessage("Adding....")
    else:
        infoMessage("\nRemoving....")

    print(items)
    print("-" * 45)


def modify_menu(cur_df: pd.DataFrame, cur_suggestions_df: pd.DataFrame):

    while True:
        showSuggestionOptions = False
        if not cur_suggestions_df.empty:
            showSuggestionOptions = True

        valid_range = cur_df.index.to_list()
        valid_range_suggestions = cur_suggestions_df.index.to_list()

        # print(valid_range, valid_range_suggestions)

        print_modify_menu(showSuggestionOptions)

        choice = coloredInput("Enter your choice : ")

        match choice:
            case "1":
                return cur_df

            case "2":
                input_str = coloredInput(
                    "\nEnter row nos. to be removed (comma separated): "
                )
                row_nos = getRowNos(input_str, valid_range)

                show_modifying_rows(cur_df, row_nos, "remove")
                cur_df = cur_df.drop(row_nos)

                print("\nRows removed successfully!\n")

            case "3":
                if showSuggestionOptions:
                    input_str = coloredInput(
                        "\nEnter row nos. to be add (comma separated): "
                    )
                    row_nos = getRowNos(input_str, valid_range_suggestions)

                    show_modifying_rows(cur_suggestions_df, row_nos, "add")
                    items = cur_suggestions_df.loc[
                        cur_suggestions_df.index.isin(row_nos)
                    ]
                    # items = items[["Name", "Email", "Email_Match", "Row_no"]]
                    cur_df = pd.concat([cur_df, items], ignore_index=True)

                    cur_suggestions_df = cur_suggestions_df.drop(row_nos)

                else:
                    errorMessage("Invalid choice!")

            case _:
                errorMessage("Invalid choice!")

        printCurrentState(cur_df, cur_suggestions_df)


def user_filter(df: pd.DataFrame, suggestions_df: pd.DataFrame = pd.DataFrame()):

    if df.empty:
        return df

    if not getChoice("Do you want to modify the DataFrame"):
        return df

    cur_df = df.copy()
    cur_suggestions_df = suggestions_df.copy()

    cur_df = modify_menu(cur_df, cur_suggestions_df)

    if not getChoice("\nSave changes"):
        return df

    return cur_df
