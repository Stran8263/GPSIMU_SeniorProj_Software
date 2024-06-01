import serial
import csv

ser = serial.Serial('COM3', 9600)  # Read COM Port
ser.flushInput()

# Open csv
with open('data4.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write columns
    csvwriter.writerow(["dTime_IMU(ms)", "Acc X[mg]", "Acc Y[mg]", "Acc Z[mg]", "Gyr X[mdps]", "Gyr Y[mdps]", "Gyr Z[mdps]", "Time_GPS(ms)", "Lat(degrees*10^-7)", "Long(degrees*10^-7)","Alt(mm)", "SIV"])

    try:
        while True:
            # Read data line from port
            line = ser.readline().decode().strip()

            # Split the data
            values = line.split()

            # Check the number of values
            if len(values) == 7:
                # Write the first six values to the first 7 columns
                csvwriter.writerow(values)
            elif len(values) == 5:
                #skip first 7 columns
                csvwriter.writerow([""] * 7 + values)
            else:
                # Do nothing if else
                pass

            print("Data written to CSV:", values)

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Closing CSV file.")
        csvfile.close()
        ser.close()
