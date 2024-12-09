import subprocess
import os

def get_symbols(file_path, filter_undefined=False):
    """
    Extract symbols from a library or executable using nm.
    :param file_path: Path to the file to analyze.
    :param filter_undefined: If True, only return undefined symbols.
    :return: A set of symbols.
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
            return set()

        symbols = set()
        for line in result.stdout.splitlines():
            line = line.strip()
            parts = line.split()
            if len(parts) >= 2:
                # Filter undefined symbols if required
                if filter_undefined and parts[0] != "U":
                    continue
                # Exclude undefined symbols if not filtering
                if not filter_undefined and parts[0] == "U":
                    continue
                symbols.add(parts[-1])  # Add the symbol name
        return symbols
    except Exception as e:
        print(f"Error: {e}")
        return set()

def compare_symbols(lib_path, exe_path, lib_name):
    """
    Compare symbols between a library and an executable, ensuring only symbols
    that are undefined in the executable and defined in the library are counted.
    Undefined symbols in both are excluded.
    :param lib_path: Path to the library.
    :param exe_path: Path to the executable.
    :param lib_name: Name of the library for reporting.
    """
    print(f"Analyzing symbols for {lib_name}...")

    # Extract symbols for the library and executable
    lib_defined_symbols = get_symbols(lib_path, filter_undefined=False)
    lib_undefined_symbols = get_symbols(lib_path, filter_undefined=True)
    exe_undefined_symbols = get_symbols(exe_path, filter_undefined=True)

    # Remove symbols that are undefined in both
    filtered_exe_symbols = exe_undefined_symbols - lib_undefined_symbols

    # Keep only symbols that are defined in the library but undefined in the executable
    used_symbols = lib_defined_symbols & filtered_exe_symbols

    print(f"Found {len(used_symbols)} symbols from {lib_name} used in the executable:")
    for symbol in sorted(used_symbols):
        print(symbol)
    print("\n")

def main():
    # Paths to libraries and the executable
    libraries = [
        {"path": "/home/lizeren/Desktop/OpenLane-bin/nix/store/libedit-20230828-3.1/lib/libedit.so", "name": "libedit.so"},
    ]
    exe_path = "/home/lizeren/Desktop/OpenLane-bin/nix/target/abc"

    # Verify paths exist
    if not os.path.exists(exe_path):
        print(f"Error: {exe_path} does not exist.")
        return

    # Process each library
    for lib in libraries:
        if os.path.exists(lib["path"]):
            compare_symbols(lib["path"], exe_path, lib["name"])
        else:
            print(f"Error: {lib['path']} does not exist.")

if __name__ == "__main__":
    main()
