from pathlib import Path
import pygsheets
from google.oauth2.gdch_credentials import ServiceAccountCredentials

'''
Depend on the API permission granted, you may need to add the virtual sheet to the virtual-user, 
the permission could be found within JSON credential, named client_email. 
Generated after generated service account > key
'''


class GoogleSheetHelper:

    def __init__(self, credential_path: str = "python-chatgtp-d3c7f6081456.json",
                 sheet_link: str = 'https://docs.google.com/spreadsheets/d/1srTSpamIOQAk8lNwT5_OOHVyhlnsgmH79k7ZS-pCZzQ/edit'):
        """
        :param str credential_path: the path to the service account json credentials, refer to 0530_金融研訓院day2-m(學員下載版)
        :param str sheet_link: the URL of the google sheet
        """
        self.__credential_path = Path(credential_path).resolve()
        self._sheet_link = sheet_link
        self._google_sheet = pygsheets.authorize(service_file=self.__credential_path)

    @property
    def google_sheet(self):
        return self._google_sheet

    @property
    def sheet(self):
        return self._google_sheet.open_by_url(self._sheet_link)

    @property
    def worksheets(self):
        return self.sheet.worksheets()


# google_sheet = GoogleSheetHelper()
# for s in google_sheet.worksheets():
#     print(s)


google_sheet = pygsheets.authorize(service_file='python-chatgtp-d3c7f6081456.json')
sheet = google_sheet.open_by_url(
    'https://docs.google.com/spreadsheets/d/1srTSpamIOQAk8lNwT5_OOHVyhlnsgmH79k7ZS-pCZzQ/edit')

# for s in sheet.worksheets():
#     print(s.title)


def get_data():
    ans = sheet[0].cell("B2")
    print(ans.value)


def get_receiver_info():
    # sheet[0].update_value('A1', "Update by Python")
    data = sheet[1].get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas="matrix")
    receiver_name, receiver_email = list(), list()
    for i in enumerate(data):
        if i[0] == 0:
            continue
        receiver_name.append(i[1][0])
        receiver_email.append(i[1][1])
    return receiver_name, receiver_email
# data.remove(["Name, Email"])
# zip(data, receiver_name, receiver_email)
#     receiver_name.append(i[1][0])
#     receiver_email.append(i[1][1])
# print(receiver_name, receiver_email)
#
# print(receiver_name, receiver_email)

