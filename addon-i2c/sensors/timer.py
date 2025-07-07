class Timer:
    @staticmethod
    def get_time():
        from datetime import datetime
        from zoneinfo import ZoneInfo
        now = datetime.now(ZoneInfo("Europe/Warsaw"))
        return "     " + now.strftime("%H:%M:%S")