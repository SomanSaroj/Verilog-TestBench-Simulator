import os
import re
import subprocess
import shutil
import time

def parse_verilog_header(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    match = re.search(r'module\s+(\w+)\s*\((.*?)\);', code, re.S)
    if match:
        module_name = match.group(1)
        port_list = match.group(2).replace("\n", "").replace("\t", "")
        ports = [p.strip() for p in port_list.split(',')]
        return module_name, ports, code
    else:
        print(" No module declaration found.")
        return None, [], ""
