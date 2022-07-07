import pandas as pd
from config.constants import INSTITIUTES
from helpers.filter import (
    filterByEmail,
    filterByInstitutes,
    filterByName,
    getSuggestions,
    matchEmailAndContact,
)
from helpers.generate_data import generate_data_from_extract
from helpers.input import readInstitutes
from helpers.output import printList, showSuggestion
from helpers.user_filter import user_filter
from helpers.utils import coloredInput, infoMessage, printHeading, reset_index


def extractData(input_df: pd.DataFrame, ref_data_df: pd.DataFrame, institutes: list):
    filtered_df = None

    filtered_df = filterByInstitutes(input_df, institutes)

    reset_index(filtered_df, keepIndexRow=True)

    # print("\n\t\t\t--FILTERED BY INSTITIUTE--\n")
    # print(filtered_df)

    filtered_df = filterByName(filtered_df, ref_data_df)

    # print("\n\t\t\t--FILTERED BY NAMES--\n")
    # print(filtered_df)

    filtered_df = matchEmailAndContact(filtered_df, ref_data_df)

    # print("\n\t\t\t--MatchEmailAndContact--\n")
    # printList(filtered_df)

    final_df, suggestions_df = getSuggestions(input_df, ref_data_df, filtered_df)

    printHeading("FILTERED LIST", color="green-bg")
    printList(final_df)
    showSuggestion(suggestions_df)
    print("\n")

    final_df = user_filter(final_df, suggestions_df)

    generate_data_from_extract(final_df)


def filterByColumn(input_df: pd.DataFrame, ref_data_df: pd.DataFrame):
    print("\n1. NAME\n2. EMAIL\n3. INSTITUTES\n")
    choice = coloredInput("Filter By ? ")

    match choice:
        case "1":
            printHeading("FILTERED BY NAMES", color="green-bg")
            print(filterByName(input_df, ref_data_df).to_markdown(), end="\n\n")
            return

        case "2":
            printHeading("FILTERED BY EMAIL", color="blue-bg")
            print(filterByEmail(input_df, ref_data_df).to_markdown(), end="\n\n")
            return

        case "3":
            institutes = readInstitutes()

            if len(institutes) == 0:
                infoMessage(
                    "--Using default list of institutes--\n{}".format(INSTITIUTES)
                )
                institutes = INSTITIUTES

            printHeading("FILTERED BY INSTITIUTE", color="yellow-bg")
            print(filterByInstitutes(input_df, institutes).to_markdown(), end="\n\n")
