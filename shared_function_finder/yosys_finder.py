import subprocess
import os

def get_symbols(file_path):
    """
    Extract symbols from a library or executable using nm.
    :param file_path: Path to the file to analyze.
    :return: A dictionary with 'defined' and 'undefined' symbol sets.
    """
    try:
        result = subprocess.run(
            ["nm", "-D", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(f"Error running nm on {file_path}: {result.stderr}")
            return {"defined": set(), "undefined": set()}

        defined_symbols = set()
        undefined_symbols = set()

        for line in result.stdout.splitlines():
            line = line.strip()
            parts = line.split()
            if len(parts) >= 2:
                symbol = parts[-1]  # Symbol name
                if parts[0] == "U":  # Undefined symbol
                    undefined_symbols.add(symbol)
                else:  # Defined symbol
                    defined_symbols.add(symbol)
        
        return {"defined": defined_symbols, "undefined": undefined_symbols}
    except Exception as e:
        print(f"Error: {e}")
        return {"defined": set(), "undefined": set()}

def compare_symbols(lib_path, yosys_path, lib_name):
    """
    Compare symbols between a library and yosys, ensuring only symbols
    that are undefined in yosys and defined in the library are counted.
    Undefined symbols in both are excluded.
    :param lib_path: Path to the library.
    :param yosys_path: Path to yosys executable.
    :param lib_name: Name of the library for reporting.
    """
    print(f"Analyzing symbols for {lib_name}...")

    # Extract symbols for library and yosys
    lib_symbols = get_symbols(lib_path)
    sta_symbols = get_symbols(yosys_path)

    # Filter symbols
    lib_defined_symbols = lib_symbols["defined"]
    lib_undefined_symbols = lib_symbols["undefined"]
    sta_undefined_symbols = sta_symbols["undefined"]

    # Remove symbols undefined in both
    filtered_sta_symbols = sta_undefined_symbols - lib_undefined_symbols

    # Keep only symbols that are defined in the library and used by yosys
    used_symbols = lib_defined_symbols & filtered_sta_symbols

    print(f"Found {len(used_symbols)} symbols from {lib_name} used in yosys:")
    for symbol in sorted(used_symbols):
        print(symbol)
    print("\n")

def main():
    # Paths to libraries and yosys
    libraries = [
        {"path": "/lib/x86_64-linux-gnu/libncursesw.so.6", "name": "libncursesw.so.6"},
        {"path": "/home/lizeren/Desktop/OpenLane-bin/nix/store/libedit-20230828-3.1/lib/libedit.so", "name": "libedit.so"},
        {"path": "/home/lizeren/Desktop/OpenLane-bin/nix/store/libffi-3.4.6/lib/libffi.so", "name": "libffi.so"},
        {"path": "/home/lizeren/Desktop/OpenLane-bin/nix/store/zlib-1.3.1/lib/libz.so", "name": "libz.so"},
        {"path": "/usr/lib/x86_64-linux-gnu/libtcl8.6.so", "name": "ibtcl8.6.so"},
        {"path": "/usr/lib/x86_64-linux-gnu/libbsd.so.0", "name": "libbsd.so.0"},
    ]
    yosys_path = "/home/lizeren/Desktop/OpenLane-bin/nix/target/yosys"

    # Verify paths exist
    if not os.path.exists(yosys_path):
        print(f"Error: {yosys_path} does not exist.")
        return

    # Sequentially analyze each library
    for lib in libraries:
        if os.path.exists(lib["path"]):
            compare_symbols(lib["path"], yosys_path, lib["name"])
        else:
            print(f"Error: {lib['path']} does not exist.")

if __name__ == "__main__":
    main()
