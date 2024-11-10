
# TPL checker

This repo is an addendum to [LibAM](https://github.com/Siyuan-Li201/LibAM)

## How to use this repo
### Building the Docker Image
I use ivoryseeker/libam-img (from the paper repo) as the base image, then install CUDA based on that. You can refer to _Dockerfile_. 
To build your updated Docker image:
```bash
sudo docker build -t libam-cuda
```


### Running the Container
After successfully building the image, run it with:

```bash
sudo docker run --gpus all -e CUDA_VISIBLE_DEVICES=0 -it --rm libam-cuda bash
```

### Verifying CUDA Installation
Once inside the container, you can verify that CUDA is properly installed:

```bash
export PATH="/usr/local/cuda/bin:$PATH" 
nvcc --version
nvidia-smi
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```
## Error when running those pythons 
when running _python3 2_embedding.py_, this error occured mant times even all the dependency to CUDA are resolved.
```
RuntimeError('Attempting to deserialize object on a CUDA ' 
RuntimeError: Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False. 
If you are running on a CPU-only machine, 
please use torch.load with map_location=torch.device('cpu') to map your storages to the CPU.
```

To solve this, I add the following sanity check and Initialization to the **very beginning** of 2_embedding.py 
```python
import torch
torch.cuda.empty_cache()
torch.cuda.init()
print("CUDA available:", torch.cuda.is_available())
print("CUDA device count:", torch.cuda.device_count())
if  torch.cuda.is_available():
	print("CUDA current device:", torch.cuda.current_device())
	print("CUDA device name:", torch.cuda.get_device_name(torch.cuda.current_device()))
else:
	print("No CUDA devices found")
```
why? I guess it is because the repo **loads a PyTorch model that was saved with CUDA tensors** on the docker system where CUDA is not properly initialized

## How to save intermediate progress/final result to the image

If you have made changes inside a running container and want to save those changes for future use, you can commit the container to a new image.

1.  **Open a new terminal on your host system** (keep the container running) and find the container ID:
    ```bash
    docker ps
    ```
2.  **Commit the running container to a new image**:
    ```bash
    docker commit <container_id> libam-cuda-updated
    ```    
	   Replace `<container_id>` with your container's ID and `libam-cuda-updated` with the desired name for the new 	image.
    
3.  **Run the updated image**:
    ```bash
    docker run --gpus all -e CUDA_VISIBLE_DEVICES=0 -it --rm libam-cuda-updated bash
    ```



## Sidenotes: Solve the error when I try to run the docker image by original paper

```bash
$ sudo docker run -it --name libam --gpus all ivoryseeker/libam-img:latest /bin/bash
docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]].

```
```bash
# Add the package repositories
distribution=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Update the package lists
sudo apt-get update

# Install the NVIDIA Container Toolkit
sudo apt-get install -y nvidia-container-toolkit

# Restart the Docker daemon to apply changes
sudo systemctl restart docker
```
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
