import tkinter as tk
from tkinter import ttk
import threading
import serial
import time
from datetime import datetime

# Configure your serial port
SERIAL_PORT = "COM3"  # Replace with your serial port (e.g., "COM3" on Windows or "/dev/ttyUSB0" on Linux)
BAUD_RATE = 115200      # Set this to match your device's baud rate

# Global variables
is_reading = False
file_handles = {}
ser = None

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT}")
except serial.SerialException:
    print(f"Failed to connect to {SERIAL_PORT}")

# Function to read data from the serial port and display it
def read_serial():
    global is_reading, file_handles
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")  # Unique ID for each session

    # Create separate files for Voltage, mA, and uA
    file_handles = {
        'V': open(f"Voltage_{session_id}.txt", "a"),
        'mA': open(f"Current_mA_{session_id}.txt", "a"),
        'uA': open(f"Current_uA_{session_id}.txt", "a"),
    }

    while is_reading:
        try:
            if ser and ser.is_open:
                # Read data from serial port
                line = ser.readline().decode("utf-8").strip()
                if line:
                    # Parse the value and unit
                    numerical_value = line[:-1]  # Remove the last character (unit)
                    unit = line[-1].lower()      # Extract the unit and make it lowercase

                    if unit == 'v':
                        unit_display = "V"
                        title_label.config(text="Voltage Measurement")
                        unit_label.config(text=unit_display)
                    elif unit == 'm':
                        unit_display = "mA"
                        title_label.config(text="Current Measurement")
                        unit_label.config(text=unit_display)
                    elif unit == 'u':
                        unit_display = "uA"
                        title_label.config(text="Current Measurement")
                        unit_label.config(text=unit_display)
                    else:
                        continue  # Ignore invalid data

                    # Display numerical value
                    truncated_number_entry.config(state="normal")
                    truncated_number_entry.delete(0, tk.END)
                    truncated_number_entry.insert(0, numerical_value)
                    truncated_number_entry.config(state="readonly")

                    # Save data to the appropriate file
                    if unit_display in file_handles:
                        file_handles[unit_display].write(f"{numerical_value}{unit_display}\n")
                        file_handles[unit_display].flush()  # Ensure data is written immediately
            time.sleep(0.1)
        except Exception as e:
            print(f"Error during reading: {e}")
            break

# Function to start serial reading
def start_reading():
    global is_reading
    is_reading = True
    start_stop_button.config(text="Stop", command=stop_reading)
    threading.Thread(target=read_serial, daemon=True).start()

# Function to stop serial reading
def stop_reading():
    global is_reading, file_handles
    is_reading = False
    start_stop_button.config(text="Start", command=start_reading)

    # Close all file handles
    for handle in file_handles.values():
        handle.close()
    file_handles.clear()

# Create the main tkinter window
root = tk.Tk()
root.title("LUMAST Instruments")
root.geometry("460x220")  # Keep the window size as before
root.config(bg="black")  # Set the background color to black
root.resizable(False, False)

# Title label
title_label = tk.Label(
    root,
    text="Voltage Measurement",
    font=("Segoe UI", 24, "bold"),  # Increased font size
    fg="white",  # Set the font color to white
    bg="black"   # Set background to black
)
title_label.pack(pady=12)

# Frame for truncated number and unit (centered)
truncated_frame = tk.Frame(root, bg="black")  # Set background to black
truncated_frame.pack(pady=12)

# Entry for truncated number (further reduced size)
truncated_number_entry = ttk.Entry(
    truncated_frame,
    font=("Segoe UI", 18),  # Increased font size
    width=7,  # Further reduced width
    justify="center",
    state="readonly"
)
truncated_number_entry.grid(row=0, column=0, padx=5)

# Unit label (left of the entry box)
unit_label = tk.Label(
    truncated_frame,
    text="V",  # Default unit
    font=("Segoe UI", 18),  # Increased font size
    fg="white",  # Set font color to white
    bg="black"   # Set background to black
)
unit_label.grid(row=0, column=1, padx=5)

# Start/Stop button
start_stop_button = ttk.Button(
    root,
    text="Start",
    command=start_reading
)
start_stop_button.pack(pady=18)

# Customize the style for the Entry widget in the "readonly" state
style = ttk.Style()
style.configure(
    "CustomReadonly.TEntry",
    background="#333333",  # Dark background color
    fieldbackground="#333333",  # Dark field background
    foreground="#000000"   # Black text color
)
truncated_number_entry.config(style="CustomReadonly.TEntry")

# Customize the Start/Stop button style
style.configure(
    "Custom.TButton",
    background="#444444",  # Dark background
    foreground="#000000",  # Black text
    font=("Segoe UI", 18, "bold")  # Increased font size for button
)
start_stop_button.config(style="Custom.TButton", width=10)  # Reduced button width

# Run the tkinter event loop
root.mainloop()

# Close the serial connection and file handles when the program exits
if ser and ser.is_open:
    ser.close()
if file_handles:
    for handle in file_handles.values():
        handle.close()
