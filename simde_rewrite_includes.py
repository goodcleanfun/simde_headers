import glob
import re
import os
from collections.abc import Sequence


local_include_pattern = re.compile(r"#[ ]*include \"(.*)\"")

def package_header_replace(package_name, base_dir, filename):
    current_dir = os.path.dirname(filename)
    def replace(match):
        include_path = match.group(1)
        include_filename = os.path.basename(include_path)
        rel_path = os.path.relpath(os.path.join(base_dir, current_dir, include_filename), base_dir)
        return f"#include \"{include_filename}\""
    return replace

def rewrite_simde_headers(package_name, dir, filenames, out_dir=None):
    base_dir = os.path.abspath(dir)
    if out_dir is None:
        out_dir = os.path.join(os.path.curdir, f"{package_name}")
    else:
        out_dir = os.path.abspath(out_dir)
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for filename in filenames:
        with open(os.path.join(base_dir, filename), "r") as f:
            content = f.read()
        
        include_replacement_func = package_header_replace(package_name, base_dir, filename)
        content = re.sub(local_include_pattern, include_replacement_func, content)

        with open(os.path.join(out_dir, os.path.basename(filename)), "w") as f:            
            f.write(content)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("package_name", help="The name of the package")
    parser.add_argument("dir", help="The directory to search for headers")
    parser.add_argument("filenames", help="The starting file(s)", nargs="+")
    parser.add_argument("--out-dir", help="The directory to write the rewritten headers")
    args = parser.parse_args()

    rewrite_simde_headers(args.package_name, args.dir, args.filenames, args.out_dir)



