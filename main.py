import serial
import matplotlib.pyplot as plt

# Serial port initialization
port = serial.Serial('/dev/cu.usbmodem1301', 2000000)  # Replace with your port name

# Buffer initialization
buffer_size = 500
data_buffer = [0] * buffer_size

# Plot initialization
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

# Adjust x-axis range
x_range = 100  # Adjust this value to set the desired x-axis range
x_values = list(range(x_range))  # Create a list with the desired range

# Initialize the data buffer with zeros
data_buffer = [0] * x_range

# Plot setup
line, = ax.plot(x_values, data_buffer)

# Set plot labels and limits
ax.set_xlim(0, x_range)  # Set the x-axis limit to the desired range
ax.set_ylim(0, 300)
ax.set_xlabel('Index')
ax.set_ylabel('Value')

# Main loop
while True:
    # Read data from serial port
    data = port.readline().strip().decode('utf-8')
    try:
        val = int(data)
        # Shift buffer
        data_buffer.pop(0)
        data_buffer.append(val)
        # Update plot
        line.set_ydata(data_buffer)
        plt.draw()
        plt.pause(0.001)
    except ValueError:
        print("Invalid data received from serial port:", data)

# Close serial port
port.close()
