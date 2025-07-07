import subprocess
import shutil

class Folders:
    @staticmethod
    def get_size(path):
        result = subprocess.run(['du', '-sb', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        size_str = result.stdout.split()[0]
        return int(size_str)

    @staticmethod
    def get_disk_usage():
        usage = shutil.disk_usage('/')
        free_gb = usage.free / (1024 ** 3)
        total_gb = usage.total / (1024 ** 3)
        return ["Miejsce na dysku:",
                f"{free_gb:.1f}GB / {total_gb:.1f}GB"]

    @staticmethod
    def get_disk_folder_usage(folder_name):
        folder_path = '/srv/samba/' + folder_name
        total_folder_size = Folders.get_size(folder_path) / (1024 ** 3)
        return [folder_name + f": {total_folder_size:.1f}GB"]