#! /bin/python3

# op-1 glitter! :sparkles:

import os
import re
import shutil
import subprocess
import json
import argparse
from lxml import etree

HEX_COLOR_REGEX = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")


def verbose_print(text):
    if args.verbose:
        print("[OP1-G] " + text)

parser = argparse.ArgumentParser(prog="op1-glitter", description="OP-1 firmware color scheme patcher.")
parser.add_argument("theme", help="op-1 theme .json file", type=str)
parser.add_argument("firmware", help="op-1 firmware file (op1_[num].op1)", type=str)
parser.add_argument("-k", "--keep-unpacked", help="keep unpacked firmware folder", action="store_true")
parser.add_argument("-o", "--output", help="output filename")
parser.add_argument("-v", "--verbose", help="verbose mode", action="store_true")

args = parser.parse_args()

if not os.path.isfile(args.theme):
    print(f"error: file {args.theme} does not exist")
    quit()

if not os.path.isfile(args.firmware):
    print(f"error: file {args.firmware} does not exist")
    quit()

cs = open(args.theme)

try:
    csjson = json.loads(cs.read())
except json.decoder.JSONDecodeError:
    print(f"error: file {args.theme} is not a valid json file")
    quit()

cs.close()

print("unpacking op-1 firmware with op1repacker...")

try:
    subprocess.run(["op1repacker", "unpack", args.firmware], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
except FileNotFoundError:
    print("error: op1repacker not found. please install it with pip: `pip install op1repacker`!")
    quit()

print("patching SVGs...")

dirname = os.path.splitext(args.firmware.split("/")[0])[0]
dirname_display = dirname + "/content/display/"

for file in os.listdir(dirname_display):
    if file.endswith(".svg"):
        verbose_print(f"checking {file}")

        f = open(dirname_display + file)
        dat = f.read()
        f.close()

        tree = etree.fromstring(dat.encode())

        colors = csjson["global"].copy()

        fname = os.path.splitext(file)[0]

        if fname in csjson.keys(): # merge file-specific stuff with global keys
            verbose_print("filename is in theme keys, merging with global...")
            for k, v in csjson[fname].items():
                if v != "": 
                    colors[k] = v

        for orig, repl in colors.items():
            if orig and repl:
                if re.search(HEX_COLOR_REGEX, orig) and re.search(HEX_COLOR_REGEX, repl):            
                    verbose_print(f"key-value pair {orig}: {repl} are valid hex colors, replacing...")

                    dat = dat.replace(orig.upper(), repl.upper())

                    tree = etree.fromstring(dat.encode()) # inefficient but who cares lol
                else:
                    verbose_print(f"assuming key {orig} is SVG ID...")

                    if type(repl) is str:
                        repl = [["stroke", repl]]

                    if type(repl[0]) is not list:
                        repl = [repl]

                    for currentRepl in repl:
                        for element in tree.iter():
                            if element.get("id") == orig:
                                if element.tag.split("}")[1] == "g":
                                    verbose_print("key is an SVG group, replacing all colors in this group...")
                                    for e in element.iter():
                                        if e.get(currentRepl[0]):
                                            e.set(currentRepl[0], currentRepl[1].upper())

                                if element.get(currentRepl[0]):
                                    element.set(currentRepl[0], currentRepl[1].upper())

                    dat = etree.tostring(tree).decode()

        f = open(dirname_display + file, "w+")
        f.write(dat)
 
        verbose_print(f"wrote to SVG {file}")

        f.close()

print("patched.")

print("repacking firmware...")

subprocess.run(["op1repacker", "repack", dirname], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

if not args.output:
    args.output = dirname + "-" + os.path.splitext(args.theme.split("/")[-1])[0] + ".op1"

os.rename(dirname + "-repacked.op1", args.output)

if not args.keep_unpacked:
    shutil.rmtree(dirname)

print("done.")
