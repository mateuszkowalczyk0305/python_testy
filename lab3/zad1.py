import nidaqmx
from nidaqmx.constants import LineGrouping
import time

device_name = 'myDAQ2'

# Utworzenie taska
with nidaqmx.Task() as ai_task, nidaqmx.Task() as di_task:
    # Konfiguracja kanału wejścia analogowego (AI)
    ai_task.ai_channels.add_ai_voltage_chan(f"{device_name}/ai0")
    
    # Konfiguracja kanału wejścia cyfrowego (DI)
    di_task.di_channels.add_di_chan(f"{device_name}/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
    
    # Pobieranie próbek w pętli
    try:
        while True:
            # Odczyt próbek AI
            ai_data = ai_task.read()
            print(f"Analog Input (AI) value: {ai_data:.2f} V")
            
            # Odczyt próbek DI
            di_data = di_task.read()
            print(f"Digital Input (DI) value: {di_data}")
            
            # delay
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Zatrzymano pobieranie próbek.")




