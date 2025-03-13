# Freezing's financial analysis script
import pandas as pd
import matplotlib.pyplot as plt
import socket
import sqlite3

# Attempt to read the Excel file
file_path = 'income.xlsx'  # Path to the Excel file
print(f"Attempting to read file: {file_path}")  # Print the file path being attempted to read

try:
    # Read the Excel file using the openpyxl engine
    income_df = pd.read_excel(file_path, engine='openpyxl')
    print("Income DataFrame info:")
    income_df.info()  # Print information about the DataFrame
except Exception as e:
    print(f"Failed to read Excel file: {e}")  # Print error message if file reading fails
    exit()  # Exit the script if an error occurs

# Read expense data
expenses_df = pd.read_csv(r'c:\Users\29832\Desktop\week4\expenses.txt', sep=' ', header=None, names=['Month', 'Expenses'])
expenses_df['Month'] = pd.to_datetime(expenses_df['Month'])  # Convert the 'Month' column to datetime format
print("Expenses DataFrame info:")
expenses_df.info()  # Print information about the DataFrame

# Merge data from income and expenses DataFrames
merged_df = pd.merge(income_df, expenses_df, on='Month', how='inner')  # Merge on the 'Month' column
print("Merged DataFrame info:")
merged_df.info()  # Print information about the merged DataFrame

# Calculate savings
merged_df['Savings'] = merged_df['Income'] - merged_df['Expenses']  # Calculate savings by subtracting expenses from income

# Save the merged DataFrame to a SQLite database
conn = sqlite3.connect('financial.db')  # Connect to a SQLite database
merged_df.to_sql('financial_data', conn, if_exists='replace', index=False)  # Save the DataFrame to a SQL table

# Define SQL query to filter data
sql_query = """
SELECT * 
FROM financial_data
WHERE Income > 7000 AND Savings > 400
ORDER BY Month;
"""
# SQL query to select records where income is greater than 7000 and savings are greater than 400, ordered by month

# Execute SQL query and load results into a DataFrame
filtered_df = pd.read_sql(sql_query, conn)  # Read SQL query results into a DataFrame

# Close the database connection
conn.close()  # Close the SQLite connection

print("Filtered DataFrame info:")
filtered_df.info()  # Print information about the filtered DataFrame

# Get the computer name and IP address
computer_name = socket.gethostname()
try:
    ip_address = socket.gethostbyname(computer_name)
except socket.gaierror:
    ip_address = "Unable to get IP address"

# Recalculate the percentages of filtered expenses and savings
filtered_expense_percentage = (filtered_df['Expenses'].sum() / filtered_df['Income'].sum()) * 100  # Calculate expense percentage
filtered_savings_percentage = 100 - filtered_expense_percentage  # Calculate savings percentage

# Redraw the pie chart
plt.figure(figsize=(8, 8))
plt.pie([filtered_expense_percentage, filtered_savings_percentage], labels=['Expenses', 'Savings'], autopct='%1.1f%%')  # Create a pie chart
plt.title('Freezing Expense vs Savings Distribution')  # Set the title of the chart
plt.text(-1.2, -1.2, f"Computer Name: {computer_name}\nIP Address: {ip_address}", fontsize=10)  # Add computer name and IP address to the chart

# Redraw the line chart
plt.figure(figsize=(10, 6))
plt.plot(filtered_df['Month'], filtered_df['Savings'], marker='o', linestyle='-', color='green')  # Create a line chart
plt.title('Freezing Monthly Savings Trends')  # Set the title of the chart
plt.xlabel('Month')  # Set the x-axis label
plt.ylabel('Savings ($)')  # Set the y-axis label
plt.grid(True)  # Enable grid

# Set the x-axis label to 12 degrees of tilt
plt.xticks(rotation=12)

plt.text(0.98, 0.02, f"Computer Name: {computer_name}\nIP Address: {ip_address}", fontsize=10, transform=plt.gca().transAxes, 
         horizontalalignment='right', verticalalignment='bottom')  # Add computer name and IP address to the chart

# Display the chart
plt.show()  # Show the charts