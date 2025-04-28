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

def extract_port_directions(code):
    port_info = {}
    matches = re.findall(r'(input|output)\s+(\[.*?\])?\s*([^;]+);', code)
    for direction, width, signal_list in matches:
        width = width if width else ""
        signals = signal_list.replace(",", " ").split()
        for signal in signals:
            port_info[signal] = (direction, width)
    return port_info
