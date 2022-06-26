import pandas as pd
from helpers.filter import (
    filterByEmail,
    filterByInstitutes,
    filterByName,
    getSuggestions,
)
from helpers.generate_data import generate_data
from helpers.input import readInstitutes
from helpers.output import showSuggestion
from helpers.user_filter import user_filter
from helpers.utils import coloredInput, printHeading, reset_index


def extractData(input_df: pd.DataFrame, ref_data_df: pd.DataFrame, institutes: list):
    filtered_df = None

    filtered_df = filterByInstitutes(input_df, institutes)

    # print("\n\t\t\t--FILTERED BY INSTITIUTE--\n")
    # print(filtered_df)

    filtered_df = filterByName(filtered_df, ref_data_df, matchEmail=True)

    # print("\n\t\t\t--FILTERED BY NAMES--\n")
    # print(filtered_df)

    complete_matched_df, suggestions_df = getSuggestions(
        input_df, ref_data_df, filtered_df
    )

    # print("\n\t\t\t--FILTERED BY EMAIL--\n")
    # print(complete_matched_df)
    # print("--Suggestions--")
    # print(suggestions_df)

    final_df = filtered_df
    if not complete_matched_df.empty:
        final_df = pd.concat([filtered_df, complete_matched_df], join="inner")

    reset_index(final_df, keepIndexRow=True)

    printHeading("FILTERED LIST")
    print(final_df.to_markdown())
    showSuggestion(suggestions_df)
    print("\n")

    final_df = user_filter(final_df, suggestions_df)

    generate_data(final_df, for_extract=True, showPrintOption=False, showSaveFile=True)


def filterByColumn(input_df: pd.DataFrame, ref_data_df: pd.DataFrame):
    print("\n1. NAME\n2. EMAIL\n3. INSTITUTES\n")
    choice = coloredInput("Filter By ? ")

    match choice:
        case "1":
            print("\n\t\t\t\t--FILTERED BY NAMES--\n")
            print(filterByName(input_df, ref_data_df), end="\n\n")
            return

        case "2":
            print("\n\t\t\t\t--FILTERED BY EMAIL--\n")
            print(filterByEmail(input_df, ref_data_df), end="\n\n")
            return

        case "3":

            print("\n\t\t\t\t--FILTERED BY INSTITIUTE--\n")

            institutes = readInstitutes()
            print(filterByInstitutes(input_df, institutes), end="\n\n")
