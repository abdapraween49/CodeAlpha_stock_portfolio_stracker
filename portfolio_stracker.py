import csv
from datetime import datetime

# 1. Hardcoded Stock Prices (Market Data)
STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 140.00,
    "AMZN": 175.00,
    "MSFT": 410.00,
    "NVDA": 120.00
}

def display_available_stocks():
    """Available stocks aur unke prices display karne ke liye function"""
    print("\n" + "="*40)
    print("      AVAILABLE STOCKS & PRICES")
    print("="*40)
    for ticker, price in STOCK_PRICES.items():
        print(f"  {ticker:<6} : ${price:.2f}")
    print("="*40 + "\n")

def get_user_portfolio():
    """User se stocks aur unki quantity input lene ke liye function"""
    portfolio = {}
    print("Enter the stocks you own. Type 'DONE' when finished.\n")
    
    while True:
        symbol = input("Enter Stock Ticker (e.g., AAPL): ").strip().upper()
        
        if symbol == "DONE":
            break
            
        if symbol not in STOCK_PRICES:
            print(f"❌ '{symbol}' is not in our database. Please choose from available stocks.\n")
            continue
            
        try:
            quantity = int(input(f"Enter quantity for {symbol}: "))
            if quantity <= 0:
                print("❌ Quantity must be greater than 0.\n")
                continue
                
            # Agar stock pehle se added hai, toh quantity add kar do
            portfolio[symbol] = portfolio.get(symbol, 0) + quantity
            print(f"✅ Added {quantity} shares of {symbol}.\n")
            
        except ValueError:
            print("❌ Invalid input! Please enter a valid number for quantity.\n")
            
    return portfolio

def calculate_portfolio_value(portfolio):
    """Portfolio ki breakdown aur total investment value calculate karna"""
    detailed_list = []
    total_value = 0.0
    
    for symbol, quantity in portfolio.items():
        price = STOCK_PRICES[symbol]
        total_price = price * quantity
        total_value += total_price
        
        detailed_list.append({
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "total_price": total_price
        })
        
    return detailed_list, total_value

def save_to_csv(detailed_list, total_value, filename="portfolio_summary.csv"):
    """Portfolio details ko CSV file me save karna"""
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Ticker", "Quantity", "Price per Share ($)", "Total Value ($)"])
        
        for item in detailed_list:
            writer.writerow([item['symbol'], item['quantity'], f"{item['price']:.2f}", f"{item['total_price']:.2f}"])
            
        writer.writerow([])
        writer.writerow(["TOTAL PORTFOLIO VALUE", "", "", f"${total_value:.2f}"])
        
    print(f"📁 Summary saved successfully to '{filename}'")

def save_to_txt(detailed_list, total_value, filename="portfolio_summary.txt"):
    """Portfolio details ko Text file me report format me save karna"""
    with open(filename, mode="w") as file:
        file.write("="*45 + "\n")
        file.write(f"     STOCK PORTFOLIO SUMMARY ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
        file.write("="*45 + "\n\n")
        file.write(f"{'Ticker':<10}{'Quantity':<10}{'Price ($)':<12}{'Total ($)':<12}\n")
        file.write("-" * 45 + "\n")
        
        for item in detailed_list:
            file.write(f"{item['symbol']:<10}{item['quantity']:<10}{item['price']:<12.2f}{item['total_price']:<12.2f}\n")
            
        file.write("-" * 45 + "\n")
        file.write(f"TOTAL INVESTMENT VALUE: ${total_value:.2f}\n")
        file.write("="*45 + "\n")
        
    print(f"📁 Summary saved successfully to '{filename}'")

def main():
    print("Welcome to Stock Portfolio Tracker!")
    display_available_stocks()
    
    user_portfolio = get_user_portfolio()
    
    if not user_portfolio:
        print("\nNo stocks added. Exiting program.")
        return
        
    detailed_list, total_value = calculate_portfolio_value(user_portfolio)
    
    # Summary Display
    print("\n" + "="*45)
    print("           PORTFOLIO SUMMARY")
    print("="*45)
    print(f"{'Ticker':<10}{'Quantity':<10}{'Price ($)':<12}{'Total ($)':<12}")
    print("-" * 45)
    for item in detailed_list:
        print(f"{item['symbol']:<10}{item['quantity']:<10}{item['price']:<12.2f}{item['total_price']:<12.2f}")
    print("-" * 45)
    print(f"TOTAL INVESTMENT VALUE: ${total_value:.2f}")
    print("="*45 + "\n")
    
    # Save option
    save_choice = input("Do you want to save the result to files? (y/n): ").strip().lower()
    if save_choice == 'y':
        save_to_csv(detailed_list, total_value)
        save_to_txt(detailed_list, total_value)
        
    print("\nThank you for using Stock Portfolio Tracker!")

if __name__ == "__main__":
    main()