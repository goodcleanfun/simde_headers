import glob
import re
import os
from collections.abc import Sequence


local_include_pattern = re.compile(r"^#include \"(.*)\"$")

def get_simde_headers(dir, start):
    seen = set()
    base_dir = os.path.abspath(dir)

    if isinstance(start, Sequence) and not isinstance(start, (str, bytes)):
        queue = [(os.path.dirname(d), os.path.basename(d)) for d in start]
    elif isinstance(start, (str, bytes)):
        queue = [(os.path.dirname(start), os.path.basename(start))]
    else:
        raise ValueError(f"Invalid start: {start}")

    needed = []

    while queue:
        current_dir, header = queue.pop(0)
        rel_path = os.path.relpath(os.path.join(base_dir, current_dir, header), base_dir)
        if rel_path in seen:
            continue
        seen.add(rel_path)
        if rel_path == "x86/ssse3.h":
            breakpoint()
        needed.append(rel_path)

        for line in open(os.path.join(dir, current_dir, header)):
            match = local_include_pattern.match(line)
            if match:
                filename = match.group(1)
                new_dir = os.path.abspath(os.path.join(dir, current_dir, os.path.dirname(filename)))
                queue.append((new_dir, os.path.basename(filename)))
    return needed

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="The directory to search for headers")
    parser.add_argument("start", help="The starting header(s)", nargs="+")
    args = parser.parse_args()
    print("\n".join(get_simde_headers(args.dir, args.start)))

