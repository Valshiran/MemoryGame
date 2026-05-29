import random
import tkinter as tk
from tkinter import messagebox

# 1. Game Setup
# We use letters as placeholders for card values (A-H, two of each)
card_values = list("AABBCCDDEEFFGGHH")
random.shuffle(card_values)  # Shuffle them randomly

# Trackers (Our Game States)
first_clicked = None
buttons_clicked = []
matches_found = 0

def card_clicked(index, btn):
    global first_clicked, buttons_clicked, matches_found
    
    # State Guard: Ignore if card is already matched or 2 cards are already showing
    if btn["text"] != "?" or len(buttons_clicked) >= 2:
        return
        
    # Reveal the card value
    btn.config(text=card_values[index], bg="white")
    buttons_clicked.append((index, btn))
    
    # State Check: Is this the first card clicked in this turn?
    if first_clicked is None:
        first_clicked = index
    else:
        # This is the second card clicked, compare them
        idx1, btn1 = buttons_clicked[0]
        idx2, btn2 = buttons_clicked[1]
        
        if card_values[idx1] == card_values[idx2]:
            # State: MATCH! Keep them revealed and disable them
            btn1.config(bg="lightgreen", state="disabled")
            btn2.config(bg="lightgreen", state="disabled")
            matches_found += 1
            reset_turn()
            
            # Win condition state check
            if matches_found == 8:
                messagebox.showinfo("Victory!", "🎉 Outstanding! You found all the matches!")
        else:
            # State: MISMATCH! Wait 1 second (1000ms), then flip them back over
            window.after(1000, hide_cards)

def hide_cards():
    _, btn1 = buttons_clicked[0]
    _, btn2 = buttons_clicked[1]
    btn1.config(text="?", bg="#2196F3")
    btn2.config(text="?", bg="#2196F3")
    reset_turn()

def reset_turn():
    global first_clicked, buttons_clicked
    first_clicked = None
    buttons_clicked = []

# 2. UI Setup
window = tk.Tk()
window.title("Memory Match Game")
window.geometry("400x450")

label_title = tk.Label(window, text="Find the Pairs!", font=("Arial", 16, "bold"), pady=10)
label_title.pack()

# Create a frame to hold our grid of buttons
grid_frame = tk.Frame(window)
grid_frame.pack()

# 3. Build the 4x4 Grid
for i in range(16):
    # Calculate row and column positions using math
    row = i // 4
    col = i % 4
    
    # Create the button representing a hidden card
    btn = tk.Button(grid_frame, text="?", font=("Arial", 14, "bold"), 
                    width=6, height=3, bg="#2196F3", fg="black")
    
    # Connect the button to the click function, passing its specific index
    btn.config(command=lambda idx=i, b=btn: card_clicked(idx, b))
    
    # Place it dynamically into the grid layout
    btn.grid(row=row, column=col, padx=5, pady=5)

window.mainloop()