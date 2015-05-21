#!/usr/bin/python

# To use with mutt, add:
# message-hook . "unset display_filter"
# message-hook "~s ^\\\\[(rtc-linux\\\\]\\ \\\\[)*PATCH" "set display_filter=~/bin/Mcheckpatch.py"

import sys
import subprocess

def write_result(file):
    sys.stdout.write("> Output from checkpatch:\n")
    for l in file:
        sys.stdout.write("> " + l)
        if l.startswith("total:"):
            break

patch = sys.stdin.read()

checkpatch = subprocess.Popen(['/home/alex/M/linux/scripts/checkpatch.pl', '--strict', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
checkpatch.stdin.write(patch)
checkpatch.stdin.close()
checkpatch.wait()

done = 0
for l in patch.splitlines(True):
    sys.stdout.write(l)
    if done == 0 and l == "---\n":
        done = 1;
        write_result(checkpatch.stdout)

if done == 0:
    write_result(checkpatch.stdout)
