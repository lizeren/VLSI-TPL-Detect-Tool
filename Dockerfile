# Use ivoryseeker/libam-img as the base image
FROM ivoryseeker/libam-img:latest

# Install CUDA 12.1 dependencies
RUN apt update && apt install -y wget gnupg software-properties-common curl

# Add the NVIDIA CUDA repository for CUDA 12.1
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin -O /etc/apt/preferences.d/cuda-repository-pin-600 && \
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub | apt-key add - && \
    add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /"

# Install CUDA toolkit 12.1
RUN apt update && apt install -y cuda-toolkit-12-1

# Clean up
RUN rm -rf /var/lib/apt/lists/*

# Set the PATH to include CUDA binaries
ENV PATH="/usr/local/cuda/bin:$PATH"

ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH


CMD ["/bin/bash"]
