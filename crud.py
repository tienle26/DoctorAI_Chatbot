from connect import get_sheet, get_data
import pandas as pd
import bcrypt


######################## Account ########################
def create_account(id, email, password) -> None:
    account_sheet = get_sheet("Account")

    idx = len(account_sheet.get_all_values()) + 1
    account_sheet.insert_row([id, email, password, 1], idx)


def update_account(id, email="", password="") -> None:
    account_sheet = get_sheet("Account")

    if len(account_sheet.get_all_values()) > 1:
        row_idx = account_sheet.find(id).row

        if email != "":
            account_sheet.update_cell(row_idx, 2, email)

        if password != "":
            account_sheet.update_cell(row_idx, 3, password)


def find_accountID(email):
    df = get_data("Account")
    return df[df["Email"] == email].iloc[0]["ID"]


def is_existed(email, df=pd.DataFrame()):
    df = get_data("Account") if df.empty else df
    return email in df["Email"].values


def get_password(email):
    df = get_data("Account")
    if not is_existed(email, df):
        return 0
    else:
        return bcrypt.hashpw(
            df[df["Email"] == email].iloc[0]["Password"].encode("utf-8"),
            bcrypt.gensalt(),
        )


######################## Patient ########################
def create_patient_record(
    id, email, name, age="", phone="", gender="Male", image=""
) -> None:
    patient_sheet = get_sheet("Patient")
    idx = len(patient_sheet.get_all_values()) + 1
    patient_sheet.insert_row([id, email, name, age, phone, gender, image], idx)


def update_patient_record(
    id, email="", name="", age="", phone="", gender="", image=""
) -> None:
    patient_sheet = get_sheet("Patient")

    if len(patient_sheet.get_all_values()) > 1:
        row_idx = patient_sheet.find(id).row

        if email != "":
            patient_sheet.update_cell(row_idx, 2, email)
        if name != "":
            patient_sheet.update_cell(row_idx, 3, name)
        if age != "":
            patient_sheet.update_cell(row_idx, 4, age)
        if phone != "":
            patient_sheet.update_cell(row_idx, 5, phone)
        if gender != "":
            patient_sheet.update_cell(row_idx, 6, gender)
        if image != "":
            patient_sheet.update_cell(row_idx, 7, image)


######################## Appointment ########################
def create_appointment(ID, PatientID, DoctorID, Time, Description="") -> None:
    appointment_sheet = get_sheet("Appointment")
    idx = len(appointment_sheet.get_all_values()) + 1
    appointment_sheet.insert_row([ID, PatientID, DoctorID, Time, Description], idx)


def filter_appointment(PatientID: str) -> pd.DataFrame:
    appointment = get_data("Appointment")
    if not appointment.empty:
        patient_app = appointment[appointment["PatientID"] == PatientID]
        if not patient_app.empty:
            return patient_app

    return pd.DataFrame()


def update_appointment(id, DoctorID="", Time="", Description="") -> None:
    appointment_sheet = get_sheet("Appointment")

    if len(appointment_sheet.get_all_values()) > 1:
        row_idx = appointment_sheet.find(id).row

        if DoctorID != "":
            appointment_sheet.update_cell(row_idx, 3, DoctorID)
        if Time != "":
            appointment_sheet.update_cell(row_idx, 4, Time)
        if Description != "":
            appointment_sheet.update_cell(row_idx, 5, Description)


def cancel_appointment(ID: str) -> None:
    appointment_sheet = get_sheet("Appointment")
    if len(appointment_sheet.get_all_values()) > 1:
        row_idx = appointment_sheet.find(ID).row
        if row_idx != None:
            appointment_sheet.delete_rows(row_idx)


######################## Doctor ########################


######################## Drug ########################
