import pandas as pd

from helpers.utils import reset_index


def matchNames(input_str: str, names: list, withSpace=False):
    for i in range(0, len(names)):
        ref_name = names[i]

        str_name = input_str.lower()
        if not withSpace:
            str_name = str_name.replace(" ", "")

        if ref_name in str_name:
            return i

    return -1


def filterByInstitutes(input_df: pd.DataFrame, institutes: list):

    filtered = []
    institutes_names = []

    for name in institutes:
        t = name.replace(" ", "")
        institutes_names.append(t.lower())

    for i in range(0, len(input_df)):
        if matchNames(input_df.iloc[i]["Institute"], institutes_names) != -1:
            filtered.append(input_df.iloc[i])

    filtered_df = pd.DataFrame(filtered)

    return filtered_df


def filterByName(input_df: pd.DataFrame, reference_df: pd.DataFrame, matchEmail=False):
    input_names = input_df["Name"].tolist()

    temp = reference_df["Name"].tolist()
    ref_names = []

    for e in temp:
        ref_names.append(e.lower())

    newList = []

    for i in range(0, len(input_names)):

        idx = matchNames(input_names[i].lower(), ref_names, withSpace=True)

        if idx == -1:
            continue

        if not matchEmail:
            newList.append(input_df.iloc[i])
            continue

        newList.append(input_df.iloc[i][["Name", "Email"]])

        if (
            input_df.iloc[i]["Email"] == reference_df.iloc[idx]["Email_Address_1"]
            or input_df.iloc[i]["Email"] == reference_df.iloc[idx]["Email_Address_2"]
        ):
            newList[-1]["Email_Match"] = "Yes"
            newList[-1]["Roll_no"] = reference_df.iloc[idx]["Roll_no"]
        else:
            newList[-1]["Email_Match"] = "No"
            newList[-1]["Roll_no"] = "--"

    matched_list_df = pd.DataFrame(newList)

    return matched_list_df


def filterByEmail(input_df: pd.DataFrame, reference_df: pd.DataFrame, withRollNo=False):

    emails = (
        reference_df["Email_Address_1"].tolist()
        + reference_df["Email_Address_2"].tolist()
    )

    res = input_df.loc[input_df["Email"].isin(emails)]

    if not withRollNo:
        return res

    complete_matched = []
    filtered = []

    for i in range(0, len(res)):

        input_st = res.iloc[i]
        ref_st = reference_df.loc[
            (reference_df["Email_Address_1"] == input_st["Email"])
            | (reference_df["Email_Address_2"] == input_st["Email"])
        ]

        t = input_st[["Name", "Email"]]
        t["Email_Match"] = "Yes"

        temp = matchNames(
            input_st["Name"], [ref_st.iloc[0]["Name"].lower()], withSpace=True
        )

        if temp == -1:
            t["Name_in_ref_db"] = ref_st.iloc[0]["Name"]
            filtered.append(t)
        else:
            t["Roll_no"] = ref_st.iloc[0]["Roll_no"]
            complete_matched.append(t)

    complete_matched_df = pd.DataFrame(complete_matched)
    filtered_df = pd.DataFrame(filtered)

    # print(complete_matched_df)
    # print(filtered_df)

    return complete_matched_df, filtered_df


def getSuggestions(
    input_df: pd.DataFrame,
    reference_data_df: pd.DataFrame,
    selected_data_df: pd.DataFrame,
):
    selected_indexes = selected_data_df.index.values.tolist()
    leftover = input_df.copy()
    leftover = leftover.drop(selected_indexes)

    complete_matched_df, suggestions_df = filterByEmail(
        leftover, reference_data_df, withRollNo=True
    )

    reset_index(suggestions_df, keepIndexRow=True)

    return complete_matched_df, suggestions_df
