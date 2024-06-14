import threading
import time
import nidaqmx
from nidaqmx.constants import AcquisitionType

class AnalogInputAcquisition:
    def __init__(self, device_name, channel, sample_rate, voltage_range):
        self.device_name = device_name
        self.channel = channel
        self.sample_rate = sample_rate
        self.voltage_range = voltage_range
        self.task = None
        self.samples_buffer = []
        self.running = False
        self.lock = threading.Lock()
    
    def start(self):
        self.running = True
        self.task = nidaqmx.Task()
        self.task.ai_channels.add_ai_voltage_chan(
            f"{self.device_name}/{self.channel}",
            min_val=-self.voltage_range,
            max_val=self.voltage_range
        )
        self.task.timing.cfg_samp_clk_timing(
            self.sample_rate,
            sample_mode=AcquisitionType.CONTINUOUS
        )
        self.thread = threading.Thread(target=self._acquire)
        self.thread.start()
    
    def stop(self):
        self.running = False
        self.thread.join()
        self.task.close()
    
    def _acquire(self):
        while self.running:
            samples = self.task.read(number_of_samples_per_channel=int(self.sample_rate * 0.1))
            with self.lock:
                self.samples_buffer.extend(samples)
            time.sleep(0.1)
    
    def get_samples(self):
        with self.lock:
            samples = self.samples_buffer.copy()
            self.samples_buffer = []
        return samples





