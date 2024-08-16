FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
USER root

RUN apt-get update && \
    apt-get install -y python3 \
    python3-pip \
    git \
    ffmpeg
    
RUN pip3 install --upgrade pip

RUN pip install "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
RUN pip install git+https://github.com/sanchit-gandhi/whisper-jax.git
RUN pip install yt_dlp
RUN pip install pydub
RUN pip install openai