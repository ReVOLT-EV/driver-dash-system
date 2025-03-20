import tkinter as tk
import time

# === Placeholder sensor-reading functions ===
def get_speed():
    """Retrieve speed from your sensor or GPS module."""
    # TODO: replace with real sensor reading
    return 123

def get_rpm():
    """Retrieve RPM from your ECU, coil tap, or CAN bus."""
    # TODO: replace with real sensor reading
    return 4567

def get_current():
    """Retrieve current usage from your Hall effect sensor + ADC."""
    # TODO: replace with real sensor reading
    return 4.8

def get_eng_temp(): 
     # TODO: replace with real sensor reading
     return 50.6

# === Main Dashboard Application ===
class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Motorcycle Dash")

        # 1) Optionally remove window decorations for a more "kiosk" style
        # self.root.attributes("-fullscreen", True)
        # If you want an easy way to exit, do something like:
        # self.root.bind("<Escape>", lambda e: self.root.destroy())

        # 2) Set window size (if not fullscreen)
        # e.g. 800x480 is common for a 5" or 7" Pi display
        self.root.geometry("800x480")
        
        # 3) Set background color to black
        self.root.configure(bg="Black")

        # 4) Create font styles
        self.large_font = ("Arial", 50, "bold")  # Adjust as needed
        self.medium_font = ("Arial", 40, "bold")

        # 5) Create labels for Speed, RPM, and Current
        self.speed_label = tk.Label(
            root,
            text="SPD: --- km/h",
            font=self.large_font,
            fg="white",
            bg="black"
        )
        self.speed_label.pack(pady=20)

        self.rpm_label = tk.Label(
            root,
            text="RPM: -----",
            font=self.large_font,
            fg="white",
            bg="black"
        )
        self.rpm_label.pack(pady=20)

        self.current_label = tk.Label(
            root,
            text="CURR: --.- A",
            font=self.large_font,
            fg="white",
            bg="black"
        )
        self.current_label.pack(pady=20)

        self.eng_temp_label = tk.Label(
            root,
            text="ENGINE TEMP: --.- °c",
            font=self.large_font,
            fg="white",
            bg="black"
        )
        self.eng_temp_label.pack(pady=20)

        # Start the update loop
        self.update_values()

    def update_values(self):
        """Update the label texts with live sensor data."""
        speed_val = get_speed()
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

# === Launcher ===
if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
