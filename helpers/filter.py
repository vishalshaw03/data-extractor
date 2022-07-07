from itertools import repeat
import pandas as pd
from helpers.utils import reset_index


def matchNames(input_str: str, names: list, withSpace: bool = False):

    str_name = input_str.lower()
    if not input_str.isalpha():
        alpha_list = [i for i in str_name if i.isalpha() or i.isspace()]
        str_name = "".join(alpha_list)

    if withSpace:
        t = list(filter(None, str_name.split(" ")))
        str_name = " ".join(t)
    else:
        str_name = str_name.replace(" ", "")

    for i in range(0, len(names)):
        if names[i].strip().lower() == str_name:
            return i

    return -1


def matchTextInList(in_str: str, ref_list: list):
    for i in range(len(ref_list)):
        if "," in ref_list[i]:
            if matchTextInList(in_str, ref_list[i].split(",")) != -1:
                return i
        if in_str.strip().lower() == ref_list[i].lower().strip():
            return i

    return -1


def matchContact(in_no: str, ref_list: list):
    if len(in_no) > 10 and in_no.startswith("91"):
        in_no = in_no[2:]

    for i in range(len(ref_list)):
        ref = str(ref_list[i])
        if "," in ref:
            if matchContact(in_no, ref.split(",")) != -1:
                return i
        if in_no.strip().lower() == ref.lower().strip():
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


def filterByName(input_df: pd.DataFrame, reference_df: pd.DataFrame):
    temp = reference_df["Name"].tolist()
    ref_names = []

    for e in temp:
        ref_names.append(e.lower())

    drop_list = []

    filtered_df = input_df.reset_index(drop=True)
    filtered_df["Ref_row_no"] = [].extend(repeat("--", len(input_df)))

    for i in range(len(filtered_df)):

        idx = matchNames(filtered_df.iloc[i]["Name"], ref_names, withSpace=True)
        if idx == -1:
            drop_list.append(i)
            continue

        filtered_df.at[i, "Ref_row_no"] = idx

    filtered_df = filtered_df.drop(drop_list)
    filtered_df["Name_Match"] = "Yes"
    reset_index(filtered_df)

    return filtered_df


def filterByEmail(input_df: pd.DataFrame, reference_df: pd.DataFrame):

    emails = []
    for e in reference_df["Email"].tolist():
        if "," in e:
            emails.extend(e.split(","))
        emails.append(e)

    res = input_df.loc[input_df["Email"].isin(emails)]

    return res


def filterByContact(input_df: pd.DataFrame, reference_df: pd.DataFrame):

    contacts = reference_df["Contact"].tolist()
    match_list = []

    for i in range(len(input_df)):
        if matchContact(str(input_df.iloc[i]["Contact"]), contacts) != -1:
            match_list.append(input_df.iloc[i])

    res = pd.DataFrame(match_list)
    return res


def matchEmailAndContact(filtered_df: pd.DataFrame, reference_data_df: pd.DataFrame):

    cols = filtered_df.columns
    match_email = "Email" in cols
    match_contact = "Contact" in cols

    new_filtered_df = filtered_df.reset_index(drop=True)

    no_list = []
    roll_list = []
    no_list.extend(repeat("No", len(new_filtered_df)))
    roll_list.extend(repeat("--", len(new_filtered_df)))

    if match_email:
        new_filtered_df["Email_Match"] = no_list

    if match_contact:
        new_filtered_df["Contact_Match"] = no_list

    if match_contact or match_email:
        new_filtered_df["Roll_no"] = roll_list

    for i in range(len(filtered_df)):
        st = filtered_df.iloc[i]
        ref_st = reference_data_df.iloc[int(st["Ref_row_no"])]

        if match_email and matchTextInList(st["Email"], [ref_st["Email"]]) != -1:
            new_filtered_df.at[i, "Email_Match"] = "Yes"
            new_filtered_df.at[i, "Roll_no"] = ref_st["Roll_no"]

        if (
            match_contact
            and matchContact(str(st["Contact"]), [ref_st["Contact"]]) != -1
        ):
            new_filtered_df.at[i, "Contact_Match"] = "Yes"
            new_filtered_df.at[i, "Roll_no"] = ref_st["Roll_no"]

    reset_index(new_filtered_df)

    return new_filtered_df


def getSuggestions(
    input_df: pd.DataFrame,
    reference_data_df: pd.DataFrame,
    selected_data_df: pd.DataFrame,
):

    cols = input_df.columns.tolist()
    match_email = "Email" in cols
    match_contact = "Contact" in cols
    email_filtered_df = pd.DataFrame()
    contact_filtered_df = pd.DataFrame()

    complete_matched_df = selected_data_df[selected_data_df["Roll_no"] != "--"]
    complete_matched_df = complete_matched_df.sort_values("Roll_no")
    reset_index(complete_matched_df)

    unselected_df = selected_data_df[selected_data_df["Roll_no"] == "--"]

    selected_row_nos = selected_data_df["Row_no"]
    selected_indexes = selected_data_df.index.values.tolist()

    leftover = input_df.copy()
    leftover = leftover.drop(selected_indexes, errors="ignore")

    if match_email:
        email_filtered_df = filterByEmail(leftover, reference_data_df)
        email_filtered_df = email_filtered_df.drop(selected_row_nos, errors="ignore")
        email_filtered_df["Email_Match"] = "Yes"

    if match_contact:
        contact_filtered_df = filterByContact(leftover, reference_data_df)
        contact_filtered_df = contact_filtered_df.drop(
            selected_row_nos, errors="ignore"
        )
        contact_filtered_df["Contact_Match"] = "Yes"

    if not email_filtered_df.empty:
        reset_index(email_filtered_df, keepIndexRow=True)

    if not contact_filtered_df.empty:
        reset_index(contact_filtered_df, keepIndexRow=True)

    merged_df = pd.DataFrame()

    if not email_filtered_df.empty and not contact_filtered_df.empty:
        cols.append("Row_no")
        merged_df = pd.merge(
            left=email_filtered_df,
            right=contact_filtered_df,
            left_on=cols,
            right_on=cols,
            how="left",
        )
    else:
        merged_df = pd.concat([email_filtered_df, contact_filtered_df], join="inner")

    if not merged_df.empty:
        merged_df["Name_Match"] = "No"

    suggestions_df = pd.concat([unselected_df, merged_df], join="inner")
    suggestions_df = suggestions_df.drop_duplicates()
    suggestions_df["Ref_row_no"] = "--"
    suggestions_df["Roll_no"] = "--"

    reset_index(suggestions_df)

    return complete_matched_df, suggestions_df
