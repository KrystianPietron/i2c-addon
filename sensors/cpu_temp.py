import psutil

class Cpu:
    @staticmethod
    def get_cpu_temp():
        with open("/sys/class/thermal/thermal_zone0/temp") as temp_file:
            temp = int(temp_file.read()) / 1000.0
        return temp

    @staticmethod
    def get_cpu_usage():
        return [f"CPU: {psutil.cpu_percent()}%",
                f"CPU temp.: {Cpu.get_cpu_temp()}°C"]
