import tkinter as tk
import tkinter.messagebox  # Import messagebox for user feedback
from tkinter import font as tkfont  # for better control over typography
from abc import ABC, abstractmethod
import json

# Motorcycle base class with abstract methods
class Motorcycle(ABC):
    def __init__(self):
        self.speed = 0
        self.rpm = 1000
        self.gear = 1

    @abstractmethod
    def accelerate(self):
        pass

    @abstractmethod
    def brake(self):
        pass

    def update_gear_and_rpm_on_accelerate(self):
        gear_speed_ranges = [(0, 60), (60, 90), (90, 110), (110, 130), (130, 150), (150, 170)]
        gear_rpm_start = [1000, 5000, 5000, 5000, 5000, 5000]
        rpm_increment = 100
        max_rpm = 9000

        if self.gear <= len(gear_speed_ranges) and self.speed >= gear_speed_ranges[self.gear - 1][1]:
            if self.gear < len(gear_speed_ranges):
                self.gear += 1
                self.rpm = gear_rpm_start[self.gear - 1]
        elif self.rpm < max_rpm:
            self.rpm += rpm_increment
        else:
            if self.gear < len(gear_speed_ranges):
                self.gear += 1
                self.rpm = gear_rpm_start[self.gear - 1]

    def update_gear_and_rpm_on_brake(self):
        gear_speed_ranges = [(0, 60), (60, 90), (90, 110), (110, 130), (130, 150), (150, 170)]
        if self.gear > 1 and self.speed < gear_speed_ranges[self.gear - 1][0]:
            self.gear -= 1
            self.rpm = 9000
        elif self.rpm > 1000:
            self.rpm -= 100

    def toggle_cruise_control(self):
        self.speed = 50
        self.update_gear_and_rpm_on_accelerate()

# Specific motorcycle implementations
class SuzukiGSX(Motorcycle):
    def accelerate(self):
        if self.speed < 170:
            self.speed += 5
            self.update_gear_and_rpm_on_accelerate()

    def brake(self):
        self.speed = max(0, self.speed - 5)
        self.update_gear_and_rpm_on_brake()

class HondaHornet(Motorcycle):
    def accelerate(self):
        if self.speed < 170:
            self.speed += 3
            self.update_gear_and_rpm_on_accelerate()

    def brake(self):
        self.speed = max(0, self.speed - 3)
        self.update_gear_and_rpm_on_brake()

class HondaCBR(Motorcycle):
    def accelerate(self):
        if self.speed < 170:
            self.speed += 7
            self.update_gear_and_rpm_on_accelerate()

    def brake(self):
        self.speed = max(0, self.speed - 7)
        self.update_gear_and_rpm_on_brake()

# Factory to create motorcycle instances
def motorcycle_factory(model):
    if model == "Suzuki GSX":
        return SuzukiGSX()
    elif model == "Honda Hornet":
        return HondaHornet()
    elif model == "Honda CBR":
        return HondaCBR()
    else:
        return None

def save_state(motorcycle):
    if motorcycle:
        state = {
            'model': motorcycle.__class__.__name__,
            'speed': motorcycle.speed,
            'rpm': motorcycle.rpm,
            'gear': motorcycle.gear
        }
        with open('motorcycle_state.json', 'w') as f:
            json.dump(state, f)

def load_state():
    try:
        with open('motorcycle_state.json', 'r') as f:
            state = json.load(f)
            motorcycle = motorcycle_factory(state['model'])
            if motorcycle:
                motorcycle.speed = state['speed']
                motorcycle.rpm = state['rpm']
                motorcycle.gear = state['gear']
                return motorcycle
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None
    return None

# Main application class with GUI
class MotorcycleDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Motorcycle Dashboard Simulator")
        self.motorcycle = load_state()  # Load state at start-up if available, will be None if load fails
        self.updating = False

        # Set up fonts and colors
        self.label_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=16)
        self.bg_color = "#333333"
        self.fg_color = "#FFFFFF"
        self.button_color = "#555555"
        self.root.configure(bg=self.bg_color)

        # Dropdown to select motorcycle model
        self.motorcycle_var = tk.StringVar(self.root)
        self.motorcycle_var.set(self.motorcycle.__class__.__name__ if self.motorcycle else "Choose a motorcycle")
        models = ["Suzuki GSX", "Honda Hornet", "Honda CBR"]
        self.dropdown = tk.OptionMenu(self.root, self.motorcycle_var, *models, command=self.setup_motorcycle)
        self.dropdown.config(font=self.button_font, bg=self.button_color, fg=self.fg_color)
        self.dropdown.pack(pady=20)

        # Display labels for speed, RPM, and gear
        self.speed_label = tk.Label(self.root, text="Speed: 0 km/h", font=self.label_font, bg=self.bg_color, fg=self.fg_color)
        self.speed_label.pack(pady=5)

        self.rpm_label = tk.Label(self.root, text="RPM: 1000", font=self.label_font, bg=self.bg_color, fg=self.fg_color)
        self.rpm_label.pack(pady=5)

        self.gear_label = tk.Label(self.root, text="Gear: 1", font=self.label_font, bg=self.bg_color, fg=self.fg_color)
        self.gear_label.pack(pady=5)

        # Buttons for acceleration, braking, and cruise control
        self.accelerate_button = tk.Button(self.root, text="Accelerate", font=self.button_font, bg=self.button_color, fg=self.fg_color)
        self.accelerate_button.pack(pady=10)
        self.accelerate_button.bind("<ButtonPress>", self.start_accelerate)
        self.accelerate_button.bind("<ButtonRelease>", self.stop_update)

        self.brake_button = tk.Button(self.root, text="Brake", font=self.button_font, bg=self.button_color, fg=self.fg_color)
        self.brake_button.pack(pady=10)
        self.brake_button.bind("<ButtonPress>", self.start_brake)
        self.brake_button.bind("<ButtonRelease>", self.stop_update)

        self.cruise_control_button = tk.Button(self.root, text="Toggle Cruise Control", font=self.button_font, bg=self.button_color, fg=self.fg_color)
        self.cruise_control_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save State", font=self.button_font, bg=self.button_color, fg=self.fg_color, command=self.save_current_state)
        self.save_button.pack(pady=10)

    def setup_motorcycle(self, model):
        self.motorcycle = motorcycle_factory(model)
        self.update_dashboard()

    def update_dashboard(self):
        if self.motorcycle:
            self.speed_label.config(text=f"Speed: {self.motorcycle.speed} km/h")
            self.rpm_label.config(text=f"RPM: {self.motorcycle.rpm}")
            self.gear_label.config(text=f"Gear: {self.motorcycle.gear}")
        else:
            # Update the dashboard to show no motorcycle loaded or incorrect model
            self.speed_label.config(text="Speed: -- km/h")
            self.rpm_label.config(text="RPM: --")
            self.gear_label.config(text="Gear: --")
            self.motorcycle_var.set("Choose a motorcycle")

    def start_accelerate(self, event):
        if self.motorcycle and not self.updating:
            self.updating = True
            self.continuous_update(self.motorcycle.accelerate)

    def start_brake(self, event):
        if self.motorcycle and not self.updating:
            self.updating = True
            self.continuous_update(self.motorcycle.brake)

    def stop_update(self, event):
        self.updating = False

    def continuous_update(self, action):
        if self.updating:
            action()
            self.update_dashboard()
            self.root.after(100, lambda: self.continuous_update(action))

    def toggle_cruise_control(self):
        if self.motorcycle:
            self.motorcycle.toggle_cruise_control()
            self.update_dashboard()

    def save_current_state(self):
        save_state(self.motorcycle)
        tkinter.messagebox.showinfo("Save State", "Motorcycle state saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorcycleDashboard(root)
    root.mainloop()
