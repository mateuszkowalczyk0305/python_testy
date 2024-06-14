import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import os
from datetime import datetime
import csv

from module import AnalogInputAcquisition

class AIAcquisitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Acquisition App")
        
        self.device_name = 'myDAQ2'
        self.channel = 'ai0'
        self.sample_rate = tk.IntVar(value=1000)
        self.voltage_range = tk.DoubleVar(value=10)
        self.measurement_length = tk.DoubleVar(value=10)  # in seconds
        self.min_limit = tk.DoubleVar(value=-10)
        self.max_limit = tk.DoubleVar(value=10)
        self.auto_mode = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="Idle")
        
        self.ai_acquisition = None
        self.running = False
        self.measuring = False
        self.data = []
        
        self.create_widgets()
        self.update_status()

    def create_widgets(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Label(control_frame, text="Sample Rate (Hz):").grid(row=0, column=0)
        ttk.Entry(control_frame, textvariable=self.sample_rate).grid(row=0, column=1)
        
        ttk.Label(control_frame, text="Voltage Range (V):").grid(row=1, column=0)
        ttk.Entry(control_frame, textvariable=self.voltage_range).grid(row=1, column=1)
        
        ttk.Label(control_frame, text="Measurement Length (s):").grid(row=2, column=0)
        ttk.Entry(control_frame, textvariable=self.measurement_length).grid(row=2, column=1)
        
        ttk.Label(control_frame, text="Min Limit (V):").grid(row=3, column=0)
        ttk.Entry(control_frame, textvariable=self.min_limit).grid(row=3, column=1)
        
        ttk.Label(control_frame, text="Max Limit (V):").grid(row=4, column=0)
        ttk.Entry(control_frame, textvariable=self.max_limit).grid(row=4, column=1)
        
        ttk.Button(control_frame, text="Start Acquisition", command=self.start_acquisition).grid(row=5, column=0)
        ttk.Button(control_frame, text="Stop Acquisition", command=self.stop_acquisition).grid(row=5, column=1)
        
        ttk.Checkbutton(control_frame, text="Auto Mode", variable=self.auto_mode).grid(row=6, column=0, columnspan=2)
        
        self.status_label = ttk.Label(control_frame, textvariable=self.status)
        self.status_label.grid(row=7, column=0, columnspan=2)
        
        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.figure = Figure(figsize=(10, 5), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        ttk.Button(control_frame, text="Start Measurement", command=self.start_measurement).grid(row=8, column=0)
        ttk.Button(control_frame, text="Stop Measurement", command=self.stop_measurement).grid(row=8, column=1)

    def update_status(self):
        self.status.set(f"Status: {self.status}")
        self.root.after(1000, self.update_status)
    
    def start_acquisition(self):
        self.ai_acquisition = AnalogInputAcquisition(
            self.device_name, self.channel, self.sample_rate.get(), self.voltage_range.get()
        )
        self.ai_acquisition.start()
        self.running = True
        threading.Thread(target=self.acquire_data).start()
    
    def stop_acquisition(self):
        if self.ai_acquisition:
            self.ai_acquisition.stop()
        self.running = False
    
    def acquire_data(self):
        while self.running:
            samples = self.ai_acquisition.get_samples()
            if samples:
                self.data.extend(samples)
                self.update_plot()
            time.sleep(1)
    
    def update_plot(self):
        self.plot.clear()
        self.plot.plot(self.data, label='AI Data')
        self.plot.axhline(self.min_limit.get(), color='r', linestyle='--', label='Min Limit')
        self.plot.axhline(self.max_limit.get(), color='g', linestyle='--', label='Max Limit')
        self.plot.legend()
        self.canvas.draw()
    
    def start_measurement(self):
        self.measuring = True
        self.measurement_start_time = time.time()
        threading.Thread(target=self.measure).start()
    
    def stop_measurement(self):
        self.measuring = False
    
    def measure(self):
        while self.measuring:
            if time.time() - self.measurement_start_time > self.measurement_length.get():
                self.save_data()
                if self.auto_mode.get():
                    time.sleep(2)  # Wait time before new measurement in auto mode
                    self.measurement_start_time = time.time()
                    self.data = []
                else:
                    self.stop_measurement()
            time.sleep(1)
    
    def save_data(self):
        filename = f"measurement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Value'])
            for i, value in enumerate(self.data):
                writer.writerow([i / self.sample_rate.get(), value])
        messagebox.showinfo("Measurement Saved", f"Data saved to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AIAcquisitionApp(root)
    root.mainloop()
