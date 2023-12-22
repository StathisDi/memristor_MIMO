import json


class device_info:
    @staticmethod
    def read_device_info(json_file_path):
        with open(json_file_path) as json_file:
            info = json.load(json_file)
        return info

    def __init__(self, json_file_path):
        self.info = device_info.read_device_info(json_file_path)


if __name__ == "__main__":
    my_device_info = device_info(
        r"C:\Users\Dimitris\Documents\github\memristor_MIMO\memristor_device_info.json"
    )
    a = 1
