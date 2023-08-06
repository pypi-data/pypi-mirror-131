import psutil
import urllib.request


class CPUInfo:
    """
    {'Physical cores': 2, 'Total cores': 4, 'Max Frequency': '1800.0Mhz', 'Min Frequency': '800.0Mhz',
    'Current Frequency': '1704.576Mhz', 'Core 1': '22.4%', 'Total CPU Usage': 0.0, 'Core 2': '14.7%',
    'Core 3': '100.0%', 'Core 4': '21.2%'}
    """
    details = {}
    cpu_freq = psutil.cpu_freq()

    def get_cpu_details(self):
        try:
            # let's print CPU information
            print("=" * 40, "CPU Info", "=" * 40)
            # number of cores
            self.details['Physical cores'] = psutil.cpu_count(logical=False)
            self.details['Total cores'] = psutil.cpu_count(logical=True)
            # CPU frequencies
            self.details["Max Frequency"] = str(self.cpu_freq.max) + "Mhz"
            self.details["Min Frequency"] = str(self.cpu_freq.min) + "Mhz"
            self.details["Current Frequency"] = str(self.cpu_freq.current) + "Mhz"
            # CPU usage
            print("CPU Usage Per Core:")
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                self.details["Core " + str(int(i) + 1)] = str(percentage) + "%"
                self.details["Total CPU Usage"] = psutil.cpu_percent()
        except Exception as e:
            print(e)
        finally:
            return self.details


# TODO: make the return type more decent. each dictionary item can be split in list and then use that list.

class DiskInfo:
    partitions = psutil.disk_partitions()
    details = {}
    factor = 1024

    def get_size(self, custom_bytes, suffix="B"):
        """
    Scale bytes to its proper format
    e.g:
        1253656 => ' 1.20 MB '
        1253656678 => ' 1.17 GB '
    """
        for unit in ["", "K", "M", "G", "T", "P"]:
            if custom_bytes < self.factor:
                return f"{custom_bytes:.2f}{unit}{suffix}"
            custom_bytes /= self.factor

    def get_disk_info(self):
        try:
            for partition in self.partitions:
                self.details[str(partition.device)+'device'] = partition.device
                self.details[str(partition.device)+'mount point'] = partition.mountpoint
                self.details[str(partition.device)+'file system type'] = partition.fstype
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                except PermissionError:
                    continue
                self.details[str(partition.device)+'Total Size'] = self.get_size(partition_usage.total)
                self.details[str(partition.device)+'Used'] = self.get_size(partition_usage.used)
                self.details[str(partition.device)+'Free'] = self.get_size(partition_usage.free)
                self.details[str(partition.device)+'Percentage'] = self.get_size(partition_usage.percent)
        except Exception as e:
            print(e)
        finally:
            return self.details


class MemoryInfo:
    system_memory = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()
    details = {}
    factor = 1024

    def get_memory_info(self):
        try:
            self.details["Total Virtual"] = self.get_size(self.system_memory.total)
            self.details["Available Virtual"] = self.get_size(self.system_memory.available)
            self.details["Used Virtual"] = self.get_size(self.system_memory.used)
            self.details["Percentage Virtual"] = self.get_size(self.system_memory.percent)
            self.details["Total swap_memory"] = self.get_size(self.swap_memory.total)
            self.details["Free swap_memory"] = self.get_size(self.swap_memory.free)
            self.details["Used swap_memory"] = self.get_size(self.swap_memory.used)
            self.details["Percentage swap_memory"] = self.get_size(self.swap_memory.percent)
        except Exception as e:
            print(e)
        finally:
            return self.details

    def get_size(self, convert_bytes, suffix="B"):
        """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20 MB'
        1253656678 => '1.17 GB'
    """
        for unit in ["", "K", "M", "G", "T", "P"]:
            if convert_bytes < self.factor:
                return f"{convert_bytes:.2f}{unit}{suffix}"
            convert_bytes /= self.factor


class CheckOnline:
    """Open the url and check for the received byte. if bytes are there then it returns Pass otherwise Fail
    make object of CheckOnline and call test_connection method. True and False are self-explanatory.
    """
    result = ""

    def open_url(self):
        try:
            x = urllib.request.urlopen(url='https://www.google.com', timeout=2)
            response = x.read()
            if response == b'':
                self.result = "Fail"
            else:
                self.result = "Pass"
        except Exception as e:
            print(e)
            self.result = "Fail"
        finally:
            print("Internet Connection", self.result)
            return self.result

    def test_connection(self):
        test_connection = False
        try:
            if str(self.open_url()) == "Fail":
                test_connection = False
            else:
                test_connection = True
        except Exception as e:
            test_connection = False
            print(e)
        finally:
            return test_connection
