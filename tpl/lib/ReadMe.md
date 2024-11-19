
# Build LibSodium


## Generate  Dynamic link library
To install the `libsodium` output binaries into a specific directory(local `output` folder within the current directory) rather than the default /bin,  you can use the `--prefix` option when running the `configure` script.
```bash
./configure --enable-shared --disable-static --prefix=$(pwd)/output
make && make check
sudo make install
```

