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
            line = line.strip()  # Remove leading/trailing whitespace
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

def compare_symbols(libz_path, sta_path):
    """
    Compare symbols between libz.so and sta, ensuring only symbols
    that are undefined in sta and defined in libz.so are counted.
    Undefined symbols in both are excluded.
    :param libz_path: Path to libz.so.
    :param sta_path: Path to sta executable.
    """
    print("Extracting defined symbols from libz.so...")
    libz_defined_symbols = get_symbols(libz_path, filter_undefined=False)
    print(f"Found {len(libz_defined_symbols)} defined symbols in libz.so.")

    print("Extracting undefined symbols from libz.so...")
    libz_undefined_symbols = get_symbols(libz_path, filter_undefined=True)
    print(f"Found {len(libz_undefined_symbols)} undefined symbols in libz.so.")

    print("Extracting undefined symbols from sta...")
    sta_undefined_symbols = get_symbols(sta_path, filter_undefined=True)
    print(f"Found {len(sta_undefined_symbols)} undefined symbols in sta.")

    print("Filtering symbols that are undefined in both...")
    # Remove symbols that are undefined in libz.so
    filtered_sta_symbols = sta_undefined_symbols - libz_undefined_symbols

    # Keep only symbols that are defined in libz.so but undefined in sta
    used_symbols = libz_defined_symbols & filtered_sta_symbols

    print(f"Found {len(used_symbols)} symbols from libz.so used in sta:")
    for symbol in sorted(used_symbols):
        print(symbol)

if __name__ == "__main__":
    # Paths to libz.so and sta
    libz_path = "/home/lizeren/Desktop/OpenLane-bin/nix/store/zlib-1.3.1/lib/libz.so"
    sta_path = "/home/lizeren/Desktop/VLSI-TPL-Detect-Tool/result/OpenSTA/Target/sta"

    # Verify paths exist
    if not os.path.exists(libz_path):
        print(f"Error: {libz_path} does not exist.")
    elif not os.path.exists(sta_path):
        print(f"Error: {sta_path} does not exist.")
    else:
        compare_symbols(libz_path, sta_path)
