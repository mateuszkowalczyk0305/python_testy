from module import AnalogInputAcquisition
import time

device_name = 'myDAQ2'
channel = 'ai0'
sample_rate = 1000  # w Hz
voltage_range = 10  # w Volt

ai_acquisition = AnalogInputAcquisition(device_name, channel, sample_rate, voltage_range)

# Start akwizycji
ai_acquisition.start()

try:
    while True:
        # Pobierz próbki
        samples = ai_acquisition.get_samples()
        if samples:
            print(f"Pobrano {len(samples)} próbek: {samples}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Zatrzymano akwizycję.")

# Stop akwizycji
ai_acquisition.stop()




