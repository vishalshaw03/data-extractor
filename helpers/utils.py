import pandas as pd

# input-utils


def coloredInput(message: str):
    print(message, end="")
    print("\033[1;36;40m", end="")
    res = input()
    print("\033[0;37;40m", end="")

    return res


# output-utils


def warnRefData(path: str):
    print("\n\033[1;33;40m Note:\033[0;37;40m", end=" ")
    print("| Using reference data from", end="")
    print("\033[1;32;40m {} \033[0;37;40m\n".format(path))


def exitMessage():
    green = "\033[1;32;40m"
    normal = "\033[0;37;40m"
    print("\n{}Thank you! {}".format(green, normal))


def errorMessage(message: str):
    print("\033[1;31;40m{}\033[0;37;40m\n".format(message))


def printHeading(title: str):
    print("")
    print("\t" * 4, end="")
    print("-" * 5, end="")
    print("\033[1;37;42m  {}  \033[0;37;40m".format(title.upper()), end="")
    print("-" * 5, end="\n\n")


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
