from cProfile import label
from cgitb import text
import sqlite3
from tkinter import messagebox, Menu
from tkinter import *
import requests
import json
import time



pycrypto = Tk()
pycrypto.title("CryptoFolio")
pycrypto.iconbitmap('D:\\PythonBasics\\Applications\\cryptoFolio\\favicon.ico')

con = sqlite3.connect("coin.db")
curr = con.cursor()
curr.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()
    app_nav() 
    app_header()
    portfolio()

def app_nav():
    def clear_all():
        curr.execute("DELETE FROM coin")
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Portfolio Cleared - Please Add new coins")
        reset()
    
    def about():
        messagebox.showinfo("Portfolio Notification", "An app to store and update you with the latest Crypto changes in your invested Assets.")
    
    
    def close_app():
        pycrypto.destroy()

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label = 'Clear Portfolio', command=clear_all)
    file_item.add_command(label='Close App', command = close_app)
    menu.add_cascade(label="File", menu = file_item)

    help_item = Menu(menu)
    help_item.add_command(label="About App", command=(about))
    menu.add_cascade(label="Help", menu = help_item)
    pycrypto.config(menu=menu)



def portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=200&convert=INR&CMC_PRO_API_KEY=8f78df3e-0156-43ee-92ec-d0d9e7df7834")

    api = json.loads(api_request.content)

    curr.execute("SELECT * FROM coin")
    coins = curr.fetchall()

    def font_color(amount):
        if amount > 0:
            return "green"
        elif amount==0:
            return "black"
        else:
            return "red"
    
    def insert_coin():
        curr.execute("INSERT INTO coin(symbol, price, amount) VALUES(?,?,?)",(symbol_txt.get(), price_txt.get(), amount_txt.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin Added to your portfolio successfully!")
        reset()

    def update_coin():
        curr.execute("UPDATE coin SET symbol = ?, price = ?, amount = ? WHERE id = ?", (symbol_update.get(), price_update.get(), amount_update.get(), portid_update.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin Updated to your portfolio successfully!")
        reset()

    def delete_coin():
        curr.execute("DELETE FROM coin WHERE id=?",(portid_delete.get(),))
        messagebox.showinfo("Portfolio Notification", "Coin Deleted from portfolio successfully!")
        reset()

    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(200):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["INR"]["price"]
                pl_percoin = api["data"][i]["quote"]["INR"]["price"] - coin[3]
                total_pl_coin = pl_percoin * coin[2]

                total_pl += total_pl_coin
                total_current_value+=current_value
                total_amount_paid += total_paid

                portfolio_id = Label(pycrypto, text = coin[0], bg = "#AAB1C1", fg="black", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
                portfolio_id.grid(row = coin_row, column = 0, sticky=NSEW)

                name = Label(pycrypto, text = api["data"][i]["symbol"], bg = "#AAB1C1", fg="black", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
                name.grid(row = coin_row, column = 1, sticky=NSEW)

                price = Label(pycrypto, text = "Rs.{0:.2f}".format(api["data"][i]["quote"]["INR"]["price"]), bg = "white", fg="black", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
                price.grid(row = coin_row, column = 2, sticky=NSEW)

                no_coins = Label(pycrypto, text = coin[2], bg = "white", fg="black", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
                no_coins.grid(row = coin_row, column = 3, sticky=NSEW)

                amount_paid = Label(pycrypto, text = "Rs.{0:.2f}".format(total_paid), bg = "white", fg="black", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
                amount_paid.grid(row = coin_row, column = 4, sticky=NSEW)

                current_val = Label(pycrypto, text = "Rs.{0:.2f}".format(current_value), bg = "white", fg="black", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
                current_val.grid(row = coin_row, column = 5, sticky=NSEW)

                pl_coin = Label(pycrypto, text = "Rs.{0:.2f}".format(pl_percoin), bg = "white", fg=font_color(pl_percoin), font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
                pl_coin.grid(row = coin_row, column = 6, sticky=NSEW)

                totalpl = Label(pycrypto, text = "Rs.{0:.2f}".format(total_pl_coin), bg = "white", fg=font_color(total_pl_coin), font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
                totalpl.grid(row = coin_row, column = 7, sticky=NSEW)

                coin_row+=1
    #insert/add coin Entry points

    symbol_txt = Entry(pycrypto, borderwidth=2, relief="ridge")
    symbol_txt.insert(0, "Coin Symbol?")
    symbol_txt.grid(row=coin_row+1, column=1)

    price_txt = Entry(pycrypto, borderwidth=2, relief="ridge")
    price_txt.insert(0, "Coin purchased for?")
    price_txt.grid(row=coin_row+1, column=2)

    amount_txt = Entry(pycrypto, borderwidth=2, relief="ridge")
    amount_txt.insert(0, "Coins you have?")
    amount_txt.grid(row=coin_row+1, column=3)

    add_coin = Button(pycrypto, text="Add coin", command=insert_coin, bg="#16337E", fg="white", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
    add_coin.grid(row=coin_row+1, column=4, sticky=NSEW)

    #Update coin
    portid_update = Entry(pycrypto, borderwidth=2, relief="ridge")
    portid_update.insert(0, " Coin ID")
    portid_update.grid(row=coin_row+2, column=0)
    
    symbol_update = Entry(pycrypto, borderwidth=2, relief="ridge")
    symbol_update.insert(0, "Coin Symbol?")
    symbol_update.grid(row=coin_row+2, column=1)

    price_update = Entry(pycrypto, borderwidth=2, relief="ridge")
    price_update.insert(0, "Purchased for?")
    price_update.grid(row=coin_row+2, column=2)

    amount_update = Entry(pycrypto, borderwidth=2, relief="ridge")
    amount_update.insert(0, "units purchased?")
    amount_update.grid(row=coin_row+2, column=3)

    update_coin_txt = Button(pycrypto, text="Update Coin", command=update_coin, bg="#16337E", fg="white", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
    update_coin_txt.grid(row=coin_row+2, column=4, sticky=NSEW)

    #Delete coin
    portid_delete = Entry(pycrypto, borderwidth=2, relief="ridge")
    portid_delete.insert(0, " Coin ID")
    portid_delete.grid(row=coin_row+3, column=0)

    delete_coin_txt = Button(pycrypto, text="Delete Coin", command=delete_coin, bg="#16337E", fg="white", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
    delete_coin_txt.grid(row=coin_row+3, column=4, sticky=NSEW)
    

    totalap = Label(pycrypto, text = "Rs.{0:.2f} ".format(total_amount_paid), bg = "white", fg="black", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
    totalap.grid(row = coin_row, column = 4, sticky=NSEW)

    totalcv = Label(pycrypto, text = "Rs.{0:.2f} ".format(total_current_value), bg = "white", fg="black", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
    totalcv.grid(row = coin_row, column = 5, sticky=NSEW)

    totalpl = Label(pycrypto, text = "Rs.{0:.2f} ".format(total_pl), bg = "white", fg=font_color(total_pl), font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
    totalpl.grid(row = coin_row, column = 7, sticky=NSEW)

    api = ""

    refresh = Button(pycrypto, text="Refresh", command=reset, bg="#16337E", fg="white", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="ridge")
    refresh.grid(row=coin_row+1, column=7, sticky=NSEW)
                            


def app_header():
    portfolio_id = Label(pycrypto, text = "PortFolio ID", bg = "#16337E", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="ridge")
    portfolio_id.grid(row = 0, column = 0, sticky=NSEW)

    name = Label(pycrypto, text = "Coin Name", bg = "#16337E", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="ridge")
    name.grid(row = 0, column = 1, sticky=NSEW)

    price = Label(pycrypto, text = "Current Price", bg = "#16337E", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="ridge")
    price.grid(row = 0, column = 2, sticky=NSEW)

    no_coins = Label(pycrypto, text = "Coins owned", bg = "#16337E", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="ridge")
    no_coins.grid(row = 0, column = 3, sticky=NSEW)

    amount_paid = Label(pycrypto, text = "Total Amount Paid", bg = "#16337E", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="ridge")
    amount_paid.grid(row = 0, column = 4, sticky=NSEW)

    current_val = Label(pycrypto, text = "Current Value", bg = "#16337E", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="ridge")
    current_val.grid(row = 0, column = 5, sticky=NSEW)

    pl_coin = Label(pycrypto, text = "P/L per Coin", bg = "#16337E", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="ridge")
    pl_coin.grid(row = 0, column = 6, sticky=NSEW)

    totalpl = Label(pycrypto, text = "Total P/L with Coin", bg = "#16337E", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="ridge")
    totalpl.grid(row = 0, column = 7, sticky=NSEW)

app_nav()
app_header()
portfolio()

pycrypto.mainloop()

curr.close()
con.close()

print("program Completed")
