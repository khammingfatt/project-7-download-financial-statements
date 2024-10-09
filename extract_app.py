import streamlit as st
import yfinance as yf
import pandas as pd

# Function to get financial statements from Yahoo Finance
def get_financial_statements(ticker):
    company = yf.Ticker(ticker)
    income_statement = company.financials
    balance_sheet = company.balance_sheet
    cash_flow_statement = company.cashflow
    return income_statement, balance_sheet, cash_flow_statement

# Function to save financial statements to an Excel file
def save_statements_to_excel(ticker, income_statement, balance_sheet, cash_flow_statement):
    # Save the data to an Excel file
    with pd.ExcelWriter(f"{ticker}_financial_statements.xlsx") as writer:
        income_statement.to_excel(writer, sheet_name='Income Statement')
        balance_sheet.to_excel(writer, sheet_name='Balance Sheet')
        cash_flow_statement.to_excel(writer, sheet_name='Cash Flow Statement')

    # Download the Excel file
    return f"{ticker}_financial_statements.xlsx"

# Streamlit app interface
st.title("Financial Statement ETL from Yahoo Finance")

# Text input for ticker symbol
ticker = st.text_input("Enter the company's stock ticker symbol (e.g., AAPL for Apple):").upper()

if ticker:
    # Fetch and display financial statements when ticker is entered
    income_statement, balance_sheet, cash_flow_statement = get_financial_statements(ticker)

    st.subheader(f"Income Statement for {ticker}")
    st.write(income_statement)

    st.subheader(f"Balance Sheet for {ticker}")
    st.write(balance_sheet)

    st.subheader(f"Cash Flow Statement for {ticker}")
    st.write(cash_flow_statement)

    # Button to download the Excel file
    if st.button("Download Financial Statements as Excel"):
        excel_file = save_statements_to_excel(ticker, income_statement, balance_sheet, cash_flow_statement)
        with open(excel_file, "rb") as file:
            btn = st.download_button(
                label="Download Excel",
                data=file,
                file_name=f"{ticker}_financial_statements.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
