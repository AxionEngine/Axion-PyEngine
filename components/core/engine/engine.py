import customtkinter as ctk

def run():
    """Run the game engine directly"""
    app = ctk.CTk()
    app.title("Game Engine")
    
    # 16:9 aspect ratio (smaller size)
    window_width = 800
    window_height = 450
    
    # Center the window
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    
    app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    app.mainloop()