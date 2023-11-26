import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

import csv

def expense_recorder():
    st.title('Expense Recorder')

    st.write("Enter your expenses here:")
    date = st.date_input("Date:")
    store = st.text_input("Expense Source:")
    
    categories = ['Car', 'House', 'Food', 'Travel', 'Subscription', 'Tech', 'Credit Card', 'Grocery', 'Clothing']
    category = st.selectbox("Expense Category:", categories)

    amount = st.number_input("Amount Spent:", step=0.01)
    notes = st.text_area("Notes:", "")

    if st.button("Record Expense"):
        with open('expenses.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, store, category, amount, notes])
        st.success("Expense recorded successfully!")



def total_expenses():
    st.title('Total Expenses by Date Range')

    # Filter by date range
    date_range = st.date_input("Select Date Range", [pd.to_datetime('2023-11-01'), pd.to_datetime('2023-11-30')])

    try:
        expenses_df = pd.read_csv('expenses.csv', names=['Date', 'Store', 'Category', 'Amount', 'Notes'])

        # Convert 'Date' column to datetime format
        expenses_df['Date'] = pd.to_datetime(expenses_df['Date'])

        # Filter expenses based on the date range
        filtered_expenses = expenses_df[
            (expenses_df['Date'] >= pd.Timestamp(date_range[0])) &
            (expenses_df['Date'] <= pd.Timestamp(date_range[1]))
        ]

        st.write("Here are your recorded expenses:")
        st.write(filtered_expenses)

        # Download button to export filtered expenses to CSV
        if not filtered_expenses.empty:
            csv = filtered_expenses.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to bytes
            href = f'<a href="data:file/csv;base64,{b64}" download="filtered_expenses.csv">Download Data for Filtered Date Range</a>'
            st.markdown(href, unsafe_allow_html=True)

            # Visualization: Expenses by Category colored by Store
            fig = px.bar(filtered_expenses, x='Category', y='Amount',
                         color='Store',  # Color by Store
                         title='Expenses by Category (Colored by Store)',
                         labels={'Amount': 'Total Amount'},
                         width=800, height=600)
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)

            # Visualization: Expenses Over Time by Category
            expenses_over_time_by_category = filtered_expenses.groupby(['Date', 'Category'])['Amount'].sum().reset_index()
            fig_category = px.line(expenses_over_time_by_category, x='Date', y='Amount', color='Category',
                                   title='Expenses Over Time by Category',
                                   labels={'Date': 'Date', 'Amount': 'Total Expenses'})
            fig_category.update_traces(mode='markers+lines')
            st.plotly_chart(fig_category)

            # Visualization: Expenses Over Time (Combined)
            expenses_over_time = filtered_expenses.groupby(pd.Grouper(key='Date', freq='D'))['Amount'].sum().reset_index()
            fig_combined = px.line(expenses_over_time, x='Date', y='Amount',
                                   title='Total Expenses Over Time',
                                   labels={'Date': 'Date', 'Amount': 'Total Expenses'})
            fig_combined.update_traces(mode='markers+lines')
            st.plotly_chart(fig_combined)

        else:
            st.write("No expenses recorded yet.")
    except FileNotFoundError:
        st.error("No expenses recorded yet.")

def all_transactions():
    st.title('All Recorded Transactions')
    
    try:
        expenses_df = pd.read_csv('expenses.csv', names=['Date', 'Store', 'Category', 'Amount', 'Notes'])
        st.write("Here is a table of all recorded transactions:")
        st.write(expenses_df)

    except FileNotFoundError:
        st.error("No expenses recorded yet.")

def main():
    st.sidebar.title('Navigation')
    selected_page = st.sidebar.radio("Go to", ['Expense Recorder', 'Total Expenses', 'All Transactions'])

    if selected_page == 'Expense Recorder':
        expense_recorder()
    elif selected_page == 'Total Expenses':
        total_expenses()
    elif selected_page == 'All Transactions':
        all_transactions()

if __name__ == '__main__':
    main()
