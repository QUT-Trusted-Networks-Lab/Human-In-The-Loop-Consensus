#! python3
# app.py
# Launches the email-based consensus P.O.C

import tkinter as tk
from src import GUI, LocalBlockchain

BLOCKCHAIN_FILE = "local_chain.pkl"
CREDENTIALS_DIR = "."

def main():
    # Set up window
    root = tk.Tk()
    root.resizable(0, 0)
    root.title("Email Consensus")
    
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")
    
    # Load blockchain into the GUI
    blockchain = LocalBlockchain(BLOCKCHAIN_FILE)
    app = GUI(root, blockchain, CREDENTIALS_DIR)
    
    # Launch app
    root.mainloop()

if __name__ == "__main__":
    main()
