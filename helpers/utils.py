import pandas as pd

from helpers.colors import COLORS, NORMAL_TEXT, INPUT_TEXT


# color-utils


def getColorCode(color_name: str):
    if color_name in COLORS.keys():
        return COLORS[color_name]

    return COLORS["white"]


# input-utils


def coloredInput(message: str):
    print(message, end="")
    print("{}".format(INPUT_TEXT), end="")
    res = input()
    print("{}".format(NORMAL_TEXT), end="")

    return res


# output-utils


def coloredOutput(message: str, color: str):
    print("{}{}{}".format(getColorCode(color), message, NORMAL_TEXT))


def infoMessage(message: str):
    print("{}{}{}\n".format(COLORS["cyan"], message, NORMAL_TEXT))


def warningMessage(message: str):
    print("{}{}{}\n".format(COLORS["yellow"], message, NORMAL_TEXT))


def successMessage(message: str):
    print("{}{}{}\n".format(COLORS["green"], message, NORMAL_TEXT))


def errorMessage(message: str):
    print("{}{}{}\n".format(COLORS["red"], message, NORMAL_TEXT))


def printHeading(title: str, color: str):
    print("")
    print("\t" * 4, end="")
    print("-" * 5, end="")
    print("{}  {}  {}".format(getColorCode(color), title.upper(), NORMAL_TEXT), end="")
    print("-" * 5, end="\n\n")


def warnRefData(path: str):
    print("\n{} Note:{}".format(COLORS["yellow"], NORMAL_TEXT), end=" ")
    print("| Using reference data from", end="")
    print("{} {} {}\n".format(COLORS["green"], path, NORMAL_TEXT))


def exitMessage():
    print("\n{}Thank you! {}".format(COLORS["green"], NORMAL_TEXT))


# other-utils


def reset_index(input_df: pd.DataFrame, keepIndexRow=False):
    indexes = input_df.index.values.tolist()

    if keepIndexRow:
        input_df["Row_no"] = indexes

    input_df.reset_index(inplace=True, drop=True)
    input_df.index += 1


def checkFilePath(path: str):

    if not path.lower().endswith(".xlsx"):
        return path + ".xlsx"

    return path


def getChoice(message: str):
    choice = coloredInput(message + " (y/n) ? ")

    if not choice:
        return False

    if choice.lower() not in ["y", "n"] or choice.lower() == "n":
        return False

    return True
