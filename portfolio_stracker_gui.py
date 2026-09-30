import csv
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# 1. Hardcoded Stock Prices
STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 140.00,
    "AMZN": 175.00,
    "MSFT": 410.00,
    "NVDA": 120.00
}

class PortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("550x550")
        self.root.resizable(False, False)
        
        self.portfolio = {}

        # Title Label
        title = tk.Label(root, text="📈 Stock Portfolio Tracker", font=("Arial", 16, "bold"), fg="#1A365D")
        title.pack(pady=10)

        # Input Frame
        frame = tk.Frame(root)
        frame.pack(pady=5)

        tk.Label(frame, text="Select Stock:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.stock_var = tk.StringVar()
        self.stock_dropdown = ttk.Combobox(frame, textvariable=self.stock_var, values=list(STOCK_PRICES.keys()), state="readonly", width=12)
        self.stock_dropdown.grid(row=0, column=1, padx=5, pady=5)
        if list(STOCK_PRICES.keys()):
            self.stock_dropdown.current(0)

        tk.Label(frame, text="Quantity:", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        self.qty_entry = tk.Entry(frame, width=10)
        self.qty_entry.grid(row=0, column=3, padx=5, pady=5)

        # Add Button
        add_btn = tk.Button(frame, text="Add Stock", command=self.add_stock, bg="#2B6CB0", fg="white", font=("Arial", 9, "bold"))
        add_btn.grid(row=0, column=4, padx=10, pady=5)

        # Table Display
        self.tree = ttk.Treeview(root, columns=("Ticker", "Quantity", "Price", "Total"), show="headings", height=10)
        self.tree.heading("Ticker", text="Ticker")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price ($)")
        self.tree.heading("Total", text="Total Value ($)")

        self.tree.column("Ticker", width=100, anchor="center")
        self.tree.column("Quantity", width=100, anchor="center")
        self.tree.column("Price", width=120, anchor="center")
        self.tree.column("Total", width=140, anchor="center")
        self.tree.pack(pady=10, padx=15)

        # Total Value Label
        self.total_label = tk.Label(root, text="Total Portfolio Value: $0.00", font=("Arial", 12, "bold"), fg="#2F855A")
        self.total_label.pack(pady=5)

        # Action Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        save_btn = tk.Button(btn_frame, text="💾 Save to CSV & TXT", command=self.save_portfolio, bg="#276749", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        save_btn.grid(row=0, column=0, padx=10)

        reset_btn = tk.Button(btn_frame, text="🔄 Reset", command=self.reset_portfolio, bg="#C53030", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        reset_btn.grid(row=0, column=1, padx=10)

    def add_stock(self):
        symbol = self.stock_var.get()
        qty_text = self.qty_entry.get().strip()

        if not qty_text.isdigit() or int(qty_text) <= 0:
            messagebox.showerror("Error", "Please enter a valid positive integer for quantity.")
            return

        qty = int(qty_text)
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + qty
        self.qty_entry.delete(0, tk.END)
        self.update_display()

    def update_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_value = 0.0
        for symbol, qty in self.portfolio.items():
            price = STOCK_PRICES[symbol]
            total_price = price * qty
            total_value += total_price
            self.tree.insert("", tk.END, values=(symbol, qty, f"${price:.2f}", f"${total_price:.2f}"))

        self.total_label.config(text=f"Total Portfolio Value: ${total_value:.2f}")

    def save_portfolio(self):
        if not self.portfolio:
            messagebox.showwarning("Warning", "Portfolio is empty! Add some stocks first.")
            return

        total_value = sum(STOCK_PRICES[s] * q for s, q in self.portfolio.items())

        # Save CSV
        with open("portfolio_summary.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Ticker", "Quantity", "Price ($)", "Total Value ($)"])
            for symbol, qty in self.portfolio.items():
                writer.writerow([symbol, qty, f"{STOCK_PRICES[symbol]:.2f}", f"{STOCK_PRICES[symbol]*qty:.2f}"])
            writer.writerow([])
            writer.writerow(["TOTAL VALUE", "", "", f"${total_value:.2f}"])

        # Save TXT
        with open("portfolio_summary.txt", mode="w") as file:
            file.write("="*45 + "\n")
            file.write(f"     STOCK PORTFOLIO SUMMARY ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
            file.write("="*45 + "\n\n")
            file.write(f"{'Ticker':<10}{'Quantity':<10}{'Price ($)':<12}{'Total ($)':<12}\n")
            file.write("-" * 45 + "\n")
            for symbol, qty in self.portfolio.items():
                p = STOCK_PRICES[symbol]
                file.write(f"{symbol:<10}{qty:<10}{p:<12.2f}{p*qty:<12.2f}\n")
            file.write("-" * 45 + "\n")
            file.write(f"TOTAL INVESTMENT VALUE: ${total_value:.2f}\n")
            file.write("="*45 + "\n")

        messagebox.showinfo("Success", "Portfolio summary saved successfully to CSV and TXT files!")

    def reset_portfolio(self):
        self.portfolio.clear()
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioApp(root)
    root.mainloop()