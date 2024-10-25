from flask import Flask, render_template, flash
import pandas as pd

app = Flask(__name__)

# Google Sheet URLs (replace with your own)
SHEET_URL_RECEIPT = 'https://docs.google.com/spreadsheets/d/11MoQLWYJd5CdWG2Z67IQ8b0uvdwZ1-tKnmGI2W9Tcp8/export?gid=228565080&format=csv'  # Update with Receipt sheet tab ID
SHEET_URL_PAYMENT = 'https://docs.google.com/spreadsheets/d/11MoQLWYJd5CdWG2Z67IQ8b0uvdwZ1-tKnmGI2W9Tcp8/export?gid=1089383297&format=csv'  # Update with Payment sheet tab ID

def get_data_from_google_sheet(url):
    # Read data from Google Sheets as CSV
    df = pd.read_csv(url)
    # Convert the DataFrame to a list of dictionaries for easy template access
    return df.to_dict(orient='records')

def calculate_total(data):
    total_cash = total_bank = 0
    for index, row in enumerate(data):
        total_cash += row['Cash']
        total_bank += row['Bank']
    return [total_cash, total_bank]


@app.route('/')
def display_receipts_payments():
    receipt_data = get_data_from_google_sheet(SHEET_URL_RECEIPT)
    payment_data = get_data_from_google_sheet(SHEET_URL_PAYMENT)
    
    receipt_data_total = calculate_total(receipt_data)
    payment_data_total = calculate_total(payment_data)

    return render_template('index.html', receipts=receipt_data, payments=payment_data, total_receipts_cash=receipt_data_total[0],
                            total_receipts_bank=receipt_data_total[1], total_payments_cash=payment_data_total[0], total_payments_bank=payment_data_total[1])

if __name__ == '__main__':
    app.run()
