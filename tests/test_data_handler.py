"""
test_data_handler.py

Tests the DataHandler class in data_handler.py.
"""

from app.data_handler import DataHandler

def test_fetch_data():
    """
    Tests the fetch_data method of the DataHandler class.
    """
    # Create an instance of DataHandler
    dh = DataHandler()

    # Define the parameters (one year is fine)
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    # Fetch the data
    try:
        df = dh.fetch_data(ticker, start_date, end_date)
        print(df.head())  # Print the first 5 rows to verify
        print("\nDataHandler test passed successfully")

    except Exception as e:
        print(f"\nDataHandler test failed: {str(e)}")

# Ensures this test only runs when the script is executed directly
if __name__ == "__main__":
    test_fetch_data()