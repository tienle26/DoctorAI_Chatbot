import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import os


def get_sheet(sheetname: str):
    # Define the scope
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    # Load the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    # Authorize the client
    client = gspread.authorize(creds)

    spreadsheet = client.open(sheetname)
    sheet = spreadsheet.worksheets()[0]

    return sheet


def get_data(sheetname: str) -> pd.DataFrame:
    # Define the scope
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    # Load the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    # Authorize the client
    client = gspread.authorize(creds)
    spreadsheet = client.open(sheetname)

    sheet = spreadsheet.worksheets()[0]

    # Get all values from the worksheet
    data = sheet.get_all_values()

    # Convert to DataFrame
    return pd.DataFrame(data[1:], columns=data[0])


def create_credentials():
    if not os.path.isfile("credentials.json"):
        data = {
            "type": "service_account",
            "project_id": "chatbot80664",
            "private_key_id": "c49c59e4f3cd0c62c7012e92702fcf91fbf34ea6",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCu96PeeQIGZ1z2\n/h2/fAeYM4FnRD0SA99m/ZQIn6wmuqIaVz/sTOSmNEVeHh927QbrasEAIIUZmB+L\nbcLogLuxKPQ0beHMvQPqxUYe2Q4tNXuOIj/4X9cdJYjGqugSQG6pMbhzzu7iLmk2\noS60j97xnYApcZU0SBBvxSXwrMPzaZDphc+nYUM7FYisOQ3nu+EWnkO0wLQqKsYT\n+kkzSeDiDHXTyrjcPXuAOm8BxUYxcC/VCUdOKw/kIRSMFpguYUTgN/O6zg8Cbdrb\nUi3Cf8YBZJ9o/jExYXoxwL63DFncy+f435xz6UirompCwYugFnWZspn6mx3Xc6WA\nKHk3oUCRAgMBAAECggEAAPHFwOrqy6GNsyiafQDcoqHuiiHoaXs7XrkyLhy8h2X8\n/4Lmja45krsX/8LOXSw43BbyrT8/sKxtSSmhwnMFcFaeANVyAVKo3YDMmNiHls9h\n2BnPuhW8WcQs2ZOtFoIiBshFrFxa1j41Y63ZjHB1Xd0Bhte93C8iZZQNGSA5m4v9\nR4h/tvI3TjN19MpFb0WgVUq/oiiONz2AlG4MGIAqZbd80WMJFzym6mEI1DAFIOeS\nP55CUZ29HSLEPXl9y98TLhBfHI58En2kEnfJJDCTSn+Ysm+Q4T6Z78J90rr3pFhX\nB5OgQ1D2AA/mBAwrOEmIrBgwkJfnZS7AQgyoK6jzgQKBgQDsV9G9DwmV37mR0Fyz\naOoXDWPfGcyuSyEFbXeUWrnTTsflDg6JCAQ3eeYn8/ECU5PForgGNuu6M90GsnXM\nXb9qViAlm7WFjjToMDZhD6usKlpY9r1OtI++sPdfKcCaQNTFuXrO3L8XXkmwhrGJ\n5Ip7wHwXVyeAzRqOvo255DVDMQKBgQC9hQTDksjADTDKtsnrBKe9bk1xhJA/MHmC\ndqf1CZVfndgrjH1smfkcMzuz/MBQ8oWk26bf2Mnu1ioXcfmcscnMsGkXchFjTEQe\njYpxWjPSJI4GBBCIKlV9uruQPUztJ9QgUV992Ntx35opZokHX3TZAmGidMwXR2SH\nnPCGSb67YQKBgQCkVGuBCPOhQe3FdRr/o/MgFC9c8JNgnNxY6cQ7YtnSEvTqTtvM\na8aCzD87iGILPBGDWaCasZU14tnLzkoZzxVI2pl/jMSqGDaxOtSUqFC1ZL1tHiKC\nlwlbjbByepVwq6NF17GMI/C6TtTt6LmJJ18irLObhv3wkKvmlJf2qLZgAQKBgEe+\nGByU70vMcoD6ixtdisYqAEUNwrE4/3aExnX7J8GndhKeP0iiTOwA9QPglUjPVgof\nYF9yqJayGgMAEVbg8px6132Zn71wPIU4XYUleWJ+lgju9vck13IeAyzKF9na7vFA\n/J4ePowv8iLj/tF8sDYKMb2W6z+QthykK2Uae4phAoGALVtARFNu7FzlmU+BHL3J\n2rq+ERNyShULgdY68iWrmVT9fRM+QQ17bkuhU5WKeXjv76WAK6rNkkkQlznY82XZ\nhmmAEjGLaRrmJA6rCNUVQKmFBoSY1Rz/xIE2NVXs1ZK+NolJbfr9IU5Z3EJdNsVT\niIv7jjmUEzMFRquEv7fXvVU=\n-----END PRIVATE KEY-----\n",
            "client_email": "chatbot@chatbot80664.iam.gserviceaccount.com",
            "client_id": "101513212830103974760",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/chatbot%40chatbot80664.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com",
        }

        with open("credentials.json", "w") as file:
            json.dump(data, file)
