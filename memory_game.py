import os
import random
import tkinter as tk
from tkinter import messagebox
# 1. NEW IMPORTS: This brings in Pillow to handle images seamlessly
from PIL import Image, ImageTk

# Theme Configuration - Make sure these match your exact file names!
THEMES = {
    "Animals": ["giraffe.png", "dog.png", "flamingo.png", "kangaroo.png", "sheep.png", "sloth.png", "tiger.png", "zebra.png"],
    "Fantasy": ["hardman.png", "gemini.png", "megaman.png", "needleman.png", "rush.png", "shadowman.png", "sparkman.png", "topman.png"]
}

HIDDEN_COLOR = "white"     
REVEALED_COLOR = "#F0F0F0" 

current_theme = "Animals"
card_images = []           
shuffled_indices = []      

first_clicked = None
buttons_clicked = []
matches_found = 0
matched_indices = []

def load_theme_assets(theme_name):
    global card_images, shuffled_indices
    
    theme_folder = os.path.join("assets", theme_name.lower())
    theme_files = THEMES[theme_name]
    
    card_images = []
    for f in theme_files:
        file_path = os.path.join(theme_folder, f)
        
        # Open the image file
        pil_img = Image.open(file_path)
        
        # FORCE RESAMPLING: This aggressively shrinks high-res images down to a flat 70x70 pixels
        pil_img = pil_img.resize((70, 70), Image.Resampling.LANCZOS) 
        
        tk_img = ImageTk.PhotoImage(pil_img)
        card_images.append(tk_img)
    
    # Duplicate to make pairs (16 total)
    card_images = card_images + card_images
    
    shuffled_indices = list(range(16))
    random.shuffle(shuffled_indices)

def card_clicked(index, btn):
    global first_clicked, buttons_clicked, matches_found, matched_indices
    
    # NEW GUARD: If this card index is in our matched list, ignore the click completely!
    if index in matched_indices:
        return
        
    # Guard: Ignore clicks if card is already flipped or 2 cards are showing
    if btn["image"] != str(pixel_placeholder) or len(buttons_clicked) >= 2:
        return
        
    actual_image_idx = shuffled_indices[index]
    btn.config(image=card_images[actual_image_idx], bg=REVEALED_COLOR)
    buttons_clicked.append((index, btn))
    
    if first_clicked is None:
        first_clicked = index
    else:
        idx1, btn1 = buttons_clicked[0]
        idx2, btn2 = buttons_clicked[1]
        
        if card_images[shuffled_indices[idx1]] == card_images[shuffled_indices[idx2]]:
            # REMOVED state="disabled". Instead, we save their indices to our lock list
            matched_indices.append(idx1)
            matched_indices.append(idx2)
            
            matches_found += 1
            reset_turn()
            
            if matches_found == 8:
                messagebox.showinfo("Victory!", "🎉 Outstanding! You found all the matches!")
        else:
            window.after(1000, hide_cards)

def hide_cards():
    _, btn1 = buttons_clicked[0]
    _, btn2 = buttons_clicked[1]
    
    # HIDE: Put the invisible pixel placeholder back on the button to hide the animal
    btn1.config(image=pixel_placeholder, bg=HIDDEN_COLOR)
    btn2.config(image=pixel_placeholder, bg=HIDDEN_COLOR)
    reset_turn()

def change_theme(theme_name):
    global current_theme, matches_found, matched_indices
    current_theme = theme_name
    matches_found = 0
    matched_indices = [] # Clear the locked list for the new game
    reset_turn()
    
    load_theme_assets(current_theme)
    for btn in game_buttons:
        # Keep state="normal" so they stay bright and vibrant
        btn.config(image=pixel_placeholder, bg=HIDDEN_COLOR, state="normal")

def reset_turn():
    global first_clicked, buttons_clicked
    first_clicked = None
    buttons_clicked = []

# UI Setup
window = tk.Tk()
window.title("Themed Memory Match")
window.geometry("450x550")  # Back to a great standard window size

# -----------------------------------------------------------------------------
# FIX: Create a tiny 1x1 transparent/blank image to force pixel-mode layout
# -----------------------------------------------------------------------------
pixel_placeholder = tk.PhotoImage(width=1, height=1)

frame_menu = tk.Frame(window, pady=10)
frame_menu.pack()

label_theme = tk.Label(frame_menu, text="Select Theme: ", font=("Arial", 11))
label_theme.pack(side="left")

theme_var = tk.StringVar(window)
theme_var.set(current_theme)

dropdown = tk.OptionMenu(frame_menu, theme_var, *THEMES.keys(), command=change_theme)
dropdown.pack(side="left")

load_theme_assets(current_theme)

grid_frame = tk.Frame(window)
grid_frame.pack(pady=10)

# 4. Generate the 4x4 Grid
game_buttons = []
for i in range(16):
    row = i // 4
    col = i % 4
    
    # We pass our 1x1 pixel placeholder image here. 
    # This instantly forces Tkinter to use PIXELS for width and height!
    btn = tk.Button(
        grid_frame, 
        image=pixel_placeholder, 
        bg=HIDDEN_COLOR, 
        width=70,           # This now means exactly 70 pixels wide!
        height=70,          # This now means exactly 70 pixels tall!
        compound="center"   # Tells Tkinter to center any future images on top of it
    )
    btn.config(command=lambda idx=i, b=btn: card_clicked(idx, b))
    btn.grid(row=row, column=col, padx=4, pady=4)
    game_buttons.append(btn)

window.mainloop()