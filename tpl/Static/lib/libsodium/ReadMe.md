
# Build LibSodium


## Generate  Dynamic link library
To install the `libsodium` output binaries into a specific directory(local `output` folder within the current directory) rather than the default /bin,  you can use the `--prefix` option when running the `configure` script.
```bash
./configure --prefix=$(pwd)/output --enable-static --enable-shared
make && make check
sudo make install
```

#Notes

```bash
export LD_LIBRARY_PATH=/home/lizeren/Desktop/VLSI-TPL-Detect-Tool/Shared/tpl/lib/libsodium:$LD_LIBRARY_PATH
```