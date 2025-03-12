# FinancialPy

FinancialPy is an interactive web application that simulates a trading platform, allowing users to invest in a virtual environment using a paper account. This application is designed to provide an educational and realistic experience, making it an ideal tool for those who want to learn and practice stock market investing.

## Features

- **Stock Search & Exploration**: Users can search for and explore various stocks.
- **Dedicated Stock Pages**: Each stock has a dedicated page displaying:
  - A price trend chart.
  - A table with current prices.
  - Personalized predictions and recommendations from the integrated bot.
- **Virtual Portfolio**: Users can track the performance of purchased stocks and view profit margins.
- **Transaction Management**:
  - Buy and sell stocks using a virtual balance.
  - The account balance updates automatically after each transaction.

## Technologies Used

- **Backend**: Flask, SQLite3
- **Frontend**: Jinja, HTML, CSS
- **API Integration**: AlpacaAPI

## How to Use the Application

### Setup & Running the Application
1. Update the path to the virtual environment.
2. Run the `run_all.py` script to initialize the database and launch the application.
3. Access the application at: `http://127.0.0.1:5000/`

### Usage Guide
1. **Search for a Stock**: Enter the stock name or symbol in the search bar and press `Enter`.
2. **View Stock Details**: Click the blue `View` button to access the stock’s dedicated page.
3. **Analyze Data**:
   - Examine the price trend chart and current price table.
   - Get stock predictions and recommendations from the bot.
4. **Buy Stocks**:
   - Select a quantity (within your available virtual balance).
   - Confirm the purchase to be redirected to your portfolio.
5. **Sell Stocks**:
   - Navigate to the portfolio page.
   - Go back to the stock's dedicated page.
   - Use the `Sell` option under the buy section.
   - Your balance updates automatically after selling.

## Contributors

- **Bănilă Rareș** - Developed the stock portfolio and backend.
- **Rizea Eduard** - Developed the bot and contributed to the database.
- **Manda Ștefan** - Implemented the frontend.
