import streamlit as st
import pandas as pd
import plotly.express as px

def expense_recorder():
    st.title('Expense Recorder')

    st.write("Enter your expenses here:")
    date = st.date_input("Date:")
    store = st.text_input("Expense Store:")
    
    categories = ['Car', 'House', 'Food', 'Travel', 'Subscription', 'Tech', 'Credit Card']
    category = st.selectbox("Expense Category:", categories)

    amount = st.number_input("Amount Spent:", step=0.01)
    notes = st.text_area("Notes:", "")

    if st.button("Record Expense"):
        with open('expenses.csv', 'a') as file:
            file.write(f"{date},{store},{category},{amount},{notes}\n")
        st.success("Expense recorded successfully!")

def total_expenses():
    st.title('Total Expenses')
    st.write("Here are your recorded expenses:")

    try:
        expenses_df = pd.read_csv('expenses.csv', names=['Date', 'Store', 'Category', 'Amount', 'Notes'])
        if not expenses_df.empty:
            st.write(expenses_df)

            # Visualization: Expenses by Category colored by Store
            fig = px.bar(expenses_df, x='Category', y='Amount', 
                         color='Store',  # Color by Store
                         title='Expenses by Category (Colored by Store)', 
                         labels={'Amount': 'Total Amount'},
                         width=800, height=600)
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)

            # Visualization: Expenses Over Time (Daily)
            expenses_df['Date'] = pd.to_datetime(expenses_df['Date'])
            expenses_df.set_index('Date', inplace=True)
            expenses_over_time = expenses_df['Amount'].resample('D').sum()  # Change resampling to 'D' for daily

            fig = px.line(x=expenses_over_time.index, y=expenses_over_time.values,
                          title='Expenses Over Time (Daily)', 
                          labels={'x': 'Date', 'y': 'Total Expenses'})
            fig.update_traces(mode='markers+lines')
            st.plotly_chart(fig)

        else:
            st.write("No expenses recorded yet.")
    except FileNotFoundError:
        st.error("No expenses recorded yet.")


def main():
    st.sidebar.title('Navigation')
    selected_page = st.sidebar.radio("Go to", ['Expense Recorder', 'Total Expenses', 'Clear Data'])

    if selected_page == 'Expense Recorder':
        expense_recorder()
    elif selected_page == 'Total Expenses':
        total_expenses()
    elif selected_page == 'Clear Data':
        clear_data()

if __name__ == '__main__':
    main()

#git remote add origin https://github.com/raianrith/Finance.git