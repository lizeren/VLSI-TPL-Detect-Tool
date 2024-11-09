
### Build the Docker image:
```bash
sudo docker build -t cuda-python .
```

To start your Docker container with a `bash` shell, use the following command:

```bash
sudo docker run --gpus all -it --rm cuda-python bash
```
Test if PyTorch and CUDA are Available. Once inside the container, test:
```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```