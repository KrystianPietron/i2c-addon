import psutil
import time

class Networks:

    @staticmethod
    def network_usage(interval=1):
        net1 = psutil.net_io_counters()
        time.sleep(interval)
        net2 = psutil.net_io_counters()

        download = (net2.bytes_recv - net1.bytes_recv) / interval / 1024 / 1024  # MB/s
        upload = (net2.bytes_sent - net1.bytes_sent) / interval / 1024 / 1024  # MB/s

        return [f"↓{download:.2f}MB/s ↑{upload:.2f}MB/s"]