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

def generate_testbench_skeleton(module_name, ports, port_info):
    tb = []
    tb.append("`timescale 1ns/1ns\n")
    tb.append(f"module {module_name}_tb;\n")

    for name in ports:
        direction, width = port_info.get(name, ('input', ''))
        dtype = 'reg' if direction == 'input' else 'wire'
        line = f"{dtype} {width} {name};" if width else f"{dtype} {name};"
        tb.append(line)

    for name in ports:
        if port_info.get(name, ('input',))[0] == 'output':
            tb.append(f"reg expected_{name};")

    tb.append("")
    tb.append(f"{module_name} dut (")
    for i, name in enumerate(ports):
        comma = "," if i < len(ports) - 1 else ""
        tb.append(f"    .{name}({name}){comma}")
    tb.append(");\n")

    tb.append("// USER TESTBENCH BLOCK START")
    tb.append("initial begin")
    tb.append("    // Your stimulus will be inserted here")
    tb.append("end")
    tb.append("// USER TESTBENCH BLOCK END\n")

    tb.append("initial begin")
    tb.append(f"    $dumpfile(\"{module_name}_KIT/{module_name}_vcd.vcd\");")
    tb.append(f"    $dumpvars(0, {module_name}_tb);")
    tb.append("end\n")

    tb.append("endmodule")
    return "\n".join(tb)

def insert_stimulus(tb_code, stimulus_txt):
    with open(stimulus_txt, 'r') as f:
        stimulus_code = f.read()
    return tb_code.replace(
        "// USER TESTBENCH BLOCK START\ninitial begin\n    // Your stimulus will be inserted here\nend\n// USER TESTBENCH BLOCK END",
        stimulus_code
    )

