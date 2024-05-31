import serial
import matplotlib.pyplot as plt
import csv
import time
from scipy.signal import butter, filtfilt
import numpy as np

# Function to create a bandpass filter
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def round_value(value, decimals=4):
    rounded = round(value, decimals)
    return rounded if rounded != 0 else abs(rounded)

# Serial port initialization
port = serial.Serial('COM3', 2000000)  # Replace with your port name

# Plot initialization
plt.ion()  # Turn on interactive mode
fig, axs = plt.subplots(5, 1, figsize=(10, 8))

# Define sampling frequency (adjust based on your device)
fs = 2000

# Define frequency bands and their amplitude ranges
bands = {
    'Delta': (0.5, 4, 200),
    'Theta': (4, 8, 100),
    'Alpha': (8, 13, 60),
    'Beta': (13, 30, 30),
    'Gamma': (30, 100, 20)
}

# Initialize data buffers for each band
buffer_size = 600
data_buffers = {band: np.zeros(buffer_size) for band in bands.keys()}

# Initialize plot lines for each band
lines = {}
for ax, (band, (_, _, amp_range)) in zip(axs, bands.items()):
    ax.set_xlim(0, buffer_size)
    ax.set_ylim(-amp_range, amp_range)  # Adjust based on expected signal range
    ax.set_ylabel(band)
    line, = ax.plot(range(buffer_size), data_buffers[band])
    lines[band] = line
axs[-1].set_xlabel('Sample')

# Open CSV file
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp'] + list(bands.keys()))  # Write header

    start_time = time.time()

    # Main loop
    while True:
        # Read data from serial port
        data = port.readline().strip().decode('utf-8')
        try:
            timestamp = time.time() - start_time
            val = int(data)

            # Debug: Print raw data value
            print(f"Raw data: {val}")

            csv_row = [round(timestamp, 2)]  # Initialize CSV row with rounded timestamp

            for band, (lowcut, highcut, _) in bands.items():
                # Shift data buffer and add new value
                data_buffers[band] = np.roll(data_buffers[band], -1)
                data_buffers[band][-1] = val

                # Apply bandpass filter
                filtered_data = bandpass_filter(data_buffers[band], lowcut, highcut, fs)

                # Update plot
                lines[band].set_ydata(filtered_data)

                # Add rounded filtered data to CSV row
                
            csv_row.append(round(data_buffers["+"][0], 4))  # Append the latest filtered value
            # Write CSV row
            writer.writerow(csv_row)

            plt.draw()
            plt.pause(0.001)

        except ValueError:
            print("Invalid data received from serial port:", data)
            data = None

    # Close serial port
    port.close()
