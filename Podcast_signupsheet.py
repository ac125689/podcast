import streamlit as st
from pandas import DataFrame
from google.oauth2 import service_account
from gspread_pandas import Spread,Client

# Create a connection object.
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "podcast test"
spread = Spread(spreadsheetname,client = client)
# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()


def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df
def update_the_signup_spreadsheet(spreadsheetname,dataframe):
    col = ['Block 1', 'Block 2', 'Block 3', 'Lunch A', 'Lunch B', 'Block 5', 'Block 6']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
def update_the_nameOfPeople_spreadsheet(spreadsheetname,dataframe):
    col = ['Name of the person who regster', 'Other 1', 'Other 2', 'Other 3']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)

def main():
    st.title('Podcast Sign-up Form')
    firstLastName = st.text_input("your first and last name")
    block = st.selectbox("Select a Block", ('Block 1', 'Block 2', 'Block 3', 'Lunch A', 'Lunch B', 'Block 5', 'Block6'))
    if block == 'Block 1':
        block1 = firstLastName
    else:
        block1 = 'na'
    if block == 'Block 2':
        block2 = firstLastName
    else:
        block2 = 'na'
    if block == 'Block 3':
        block3 = firstLastName
    else:
        block3 = 'na'
    if block == 'Lunch A':
        lunchA = firstLastName
    else:
        lunchA = 'na'
    if block == 'Lunch B':
        lunchB = firstLastName
    else:
        lunchB = 'na'
    if block == 'Block 5':
        block5 = firstLastName
    else:
        block5 = 'na'
    if block == 'Block 6':
        block6 = firstLastName
    else:
        block6 = 'na'
    st.write("Now please write three other name your go to do podcast with. If there is less than ")
    name2_1 = st.text_input("name of person one")
    name3_1 = st.text_input("name of person two")
    name4_1 = st.text_input("name of person three")
    if st.button("Submit"):
        opt = { 'Block 1' : [block1],
        'Block 2': [block2], 
        'Block 3': [block3], 
        'Lunch A': [lunchA], 
        'Lunch B': [lunchB], 
        'Block 5': [block5], 
        'Block 6': [block6]}
        opt_df = DataFrame(opt)
        df = load_the_spreadsheet('Sign-up name')
        new_df = df.append(opt_df,ignore_index=True)
        update_the_signup_spreadsheet('Sign-up name',new_df)
        opt2 = { 'Name of the person who regster' : [firstLastName],
        'Other 1': [name2_1], 
        'Other 2': [name3_1],
        'Other 3': [name4_1]}
        opt2_df = DataFrame(opt2)
        df2 = load_the_spreadsheet('name of people recording')
        new_df2 = df2.append(opt2_df,ignore_index=True)
        update_the_nameOfPeople_spreadsheet('name of people recording',new_df2)
        st.balloons()
        st.success("You are good to go.")


if __name__ == "__main__":
  main()