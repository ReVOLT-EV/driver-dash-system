import tkinter as tk
from DataGenerator import get_speed, get_rpm, get_current, get_eng_temp

# ------------------------------------------------------------------------------
# 1) Start Screen
# ------------------------------------------------------------------------------
class StartFrame(tk.Frame):
    """
    A simple welcome screen with a button that leads to the main dashboard.
    """
    def __init__(self, root, on_start_callback):
        super().__init__(root)
        self.parent = root
        self.configure(bg="black")

        self.on_start_callback = on_start_callback

        # A big welcome label
        self.large_font = ("Arial", 30, "bold")
        welcome_label = tk.Label(
            self,
            text="Welcome to ReVOLT EV's Dashboard",
            font=self.large_font,
            fg="white",
            bg="black"
        )
        welcome_label.pack(pady=70)

        # A "Start" button
        start_button = tk.Button(
            self,
            text="Start",
            font=("Arial", 40, "bold"),
            command=self.handle_start_click
        )
        start_button.pack(pady=0)

        # displays ReVOLT's logo using built in PhotoImage class
        image = tk.PhotoImage(file="logo.png")
        my_label = tk.Label(self, image=image)
        my_label.image = image  # keep a reference
        my_label.pack(pady=50)

    def handle_start_click(self):
        """
        Called when the user clicks the 'Start' button.
        We trigger the callback to show the dashboard.
        """
        self.on_start_callback()


# ------------------------------------------------------------------------------
# 2) Dashboard Screen - main dashboard application
# ------------------------------------------------------------------------------
class DashboardApp(tk.Frame):
    """
    The main dashboard where speed, RPM, current, and engine temp are displayed.
    """
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.configure(bg="black")

        # Create font styles
        self.large_font = ("Arial", 50, "bold")  # Adjust as needed
        self.medium_font = ("Arial", 30, "bold")

        # Create labels for Speed, RPM, and Current
        self.speed_label = tk.Label(
            root,
            text="SPD: --- km/h",
            font=self.medium_font,
            fg="white",
            bg="black"
        )
        self.speed_label.pack(pady=20)

        self.rpm_label = tk.Label(
            root,
            text="RPM: -----",
            font=self.medium_font,
            fg="white",
            bg="black"
        )
        self.rpm_label.pack(pady=20)

        self.current_label = tk.Label(
            root,
            text="CURR: --.- A",
            font=self.medium_font,
            fg="white",
            bg="black"
        )
        self.current_label.pack(pady=20)

        self.eng_temp_label = tk.Label(
            root,
            text="ENGINE TEMP: --.- °c",
            font=self.medium_font,
            fg="white",
            bg="black"
        )
        self.eng_temp_label.pack(pady=20)

        """
        Update the label texts with live sensor data.
        This function calls itself periodically.
        """
        self.update_values()

    def update_values(self):
        """Update the label texts with live sensor data."""
        speed_val = get_speed() #call simulator.update() only in get_speed()
        rpm_val = get_rpm()
        current_val = get_current()
        eng_temp_val = get_eng_temp()

        # Update label text
        self.speed_label.config(text=f"SPD: {speed_val} km/h")
        self.rpm_label.config(text=f"RPM: {rpm_val}")
        self.current_label.config(text=f"CURR: {current_val:.1f} A")
        self.eng_temp_label.config(text=f"ENG TEMP: {eng_temp_val:.1f} °C")

        # Schedule next update (e.g. 10 times per second)
        self.root.after(100, self.update_values)

# ------------------------------------------------------------------------------
# 3) Main Application
# ------------------------------------------------------------------------------
class MainApp(tk.Tk):
    """
    The main Tk window that can display either the StartFrame or the DashboardFrame.
    """
    def __init__(self):
        super().__init__()
        self.title("Motorcycle Dash")
        self.geometry("800x480")
        self.configure(bg="black")

        # Optionally remove window decorations for kiosk mode:
        # self.attributes("-fullscreen", True)
        # self.bind("<Escape>", lambda e: self.destroy())  # Easy exit for dev

        # Initially show the start screen
        self.current_frame = None
        self.show_start_screen()

    def show_start_screen(self):
        """
        Hide any existing frame and show the StartFrame.
        """
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        self.start_screen = StartFrame(self, self.show_dashboard_screen)
        self.start_screen.pack(expand=True, fill="both")
        self.current_frame = self.start_screen

    def show_dashboard_screen(self):
        """
        Hide the start screen and show the dashboard.
        """
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        self.dashboard = DashboardApp(self)
        self.dashboard.pack(expand=True, fill="both")
        self.current_frame = self.dashboard

# ------------------------------------------------------------------------------
# 4) Entry point/ launcher
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
