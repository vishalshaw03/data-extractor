import pandas as pd
from config.constants import INSTITIUTES
from helpers.extract import extractData, filterByColumn
from helpers.generate_data import generate_data
from helpers.input import readData, readInstitutes
from helpers.output import printMenuOptions
from helpers.utils import coloredInput, errorMessage, exitMessage, getChoice

menu = ["Extract Data", "Filter By Column", "Generate Data", "Exit"]

input_df = pd.DataFrame()
ref_data_df = pd.DataFrame()


def inputData():
    global input_df
    global ref_data_df

    if input_df.empty or ref_data_df.empty:
        input_df, ref_data_df = readData()
        return

    if not getChoice("Use current data-sets"):
        input_df, ref_data_df = readData()


def showMenu():
    printMenuOptions(menu)
    choice = coloredInput("Enter your choice : ")

    match choice:
        case "1":

            inputData()
            if input_df.empty and ref_data_df.empty:
                return

            institutes = []

            default = getChoice("Use Default options")
            if default:
                institutes = INSTITIUTES
            else:
                institutes = readInstitutes()

            extractData(input_df, ref_data_df, institutes)

        case "2":
            inputData()

            if not input_df.empty and not ref_data_df.empty:
                filterByColumn(input_df, ref_data_df)

        case "3":
            generate_data(showSaveFile=True)

        case "4":
            exitMessage()
            return "exit"

        case _:
            errorMessage("Invalid chocie!")
