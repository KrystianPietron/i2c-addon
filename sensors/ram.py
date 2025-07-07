import psutil

class RamUsage:
    @staticmethod
    def get_ram_usage():
        mem = psutil.virtual_memory()
        used_mb = (mem.total - mem.available) / (1024 ** 2)
        total_mb = mem.total / (1024 ** 2)
        percent = mem.percent
        return [f"RAM: ({percent}%)",
                f"{used_mb:.0f}MB / {total_mb:.0f}MB"]