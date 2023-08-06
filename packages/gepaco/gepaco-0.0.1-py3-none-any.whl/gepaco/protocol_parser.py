from yaml import safe_load
from yaml.scanner import ScannerError
import yaml

class ProtocolParser():
    def __init__(self):
        self.proto_dict = {}

    def parse(self, yaml_file_path):
        with open(yaml_file_path, "r") as yaml_file:
            self.proto_dict = safe_load(yaml_file)
                