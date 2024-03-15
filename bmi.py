import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

class BMIApp:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")
        self.master.geometry("400x300")

        self.label_weight = tk.Label(master, text="Weight (kg):")
        self.label_weight.grid(row=0, column=0, padx=10, pady=10)
        self.entry_weight = tk.Entry(master)
        self.entry_weight.grid(row=0, column=1, padx=10, pady=10)

        self.label_height = tk.Label(master, text="Height (cm):")
        self.label_height.grid(row=1, column=0, padx=10, pady=10)
        self.entry_height = tk.Entry(master)
        self.entry_height.grid(row=1, column=1, padx=10, pady=10)

        self.btn_calculate = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.btn_calculate.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.bmi_label = tk.Label(master, text="BMI:")
        self.bmi_label.grid(row=3, column=0, padx=10, pady=10)

        self.bmi_result = tk.Label(master, text="")
        self.bmi_result.grid(row=3, column=1, padx=10, pady=10)

        self.load_data()

    def calculate_bmi(self):
        weight = float(self.entry_weight.get())
        height = float(self.entry_height.get()) / 100  # Convert to meters
        bmi = weight / (height ** 2)
        self.bmi_result.config(text=str(round(bmi, 2)))

        self.save_data(weight, height, bmi)

    def save_data(self, weight, height, bmi):
        if not os.path.exists("data.json"):
            data = []
        else:
            with open("data.json", "r") as file:
                data = json.load(file)
        
        data.append({"weight": weight, "height": height, "bmi": bmi})
        
        with open("data.json", "w") as file:
            json.dump(data, file)

    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as file:
                data = json.load(file)
                if data:
                    last_entry = data[-1]
                    self.entry_weight.insert(0, str(last_entry["weight"]))
                    self.entry_height.insert(0, str(last_entry["height"]))

    def show_history(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as file:
                data = json.load(file)
                weights = [entry["weight"] for entry in data]
                heights = [entry["height"] for entry in data]
                bmis = [entry["bmi"] for entry in data]

                plt.plot(weights, bmis, marker='o', linestyle='-')
                plt.xlabel('Weight (kg)')
                plt.ylabel('BMI')
                plt.title('BMI Trend')
                plt.show()


def main():
    root = tk.Tk()
    app = BMIApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
