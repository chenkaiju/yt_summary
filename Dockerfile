# FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu20.04

# ENV DEBIAN_FRONTEND=noninteractive
# USER root

# RUN apt-get update && \
#     apt-get install -y python3 \
#     python3-pip \
#     git \
#     ffmpeg
    
# RUN pip3 install --upgrade pip

# RUN pip install "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
# RUN pip install git+https://github.com/sanchit-gandhi/whisper-jax.git
# RUN pip install yt_dlp
# RUN pip install pydub
# RUN pip install openai


# Use the NVIDIA CUDA image as the base image
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu20.04

# Set non-interactive environment for apt and prevent Python from buffering output
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Install dependencies and clean up APT cache to reduce image size
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install all necessary Python packages in one step
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html && \
    pip install --no-cache-dir git+https://github.com/sanchit-gandhi/whisper-jax.git && \
    pip install --no-cache-dir yt_dlp pydub openai python-dotenv tiktoken

# Ensure the image is ready for use
CMD ["python3"]
