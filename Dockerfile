# YOLOv5 🚀 by Ultralytics, GPL-3.0 license

# Start FROM Nvidia PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch
FROM nvcr.io/nvidia/pytorch:21.10-py3

ENV TZ=Asia/Kolkata \
    DEBIAN_FRONTEND=noninteractive
# Install linux packages
RUN apt update && apt install -y zip htop screen libgl1-mesa-glx\
&& apt-get install ffmpeg libsm6 libxext6  -y

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
RUN python -m pip install --upgrade pip
RUN pip uninstall -y torch torchvision torchtext
RUN pip install --no-cache albumentations wandb gsutil notebook \
    torch==1.11.0+cu113 torchvision==0.12.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
# RUN pip install --no-cache -U torch torchvision
COPY yolov5/requirements.txt .
RUN pip install --no-cache -r requirements.txt
RUN pip uninstall opencv-python-headless -y
RUN pip uninstall opencv-python -y
RUN pip uninstall opencv-contrib-python -y
RUN pip install -U opencv-python==4.5.5.62
RUN pip install -U opencv-contrib-python==4.5.5.62
# RUN pip install pyarmor
# RUN pip install paddleocr paddlepaddle
# RUN pip install -U celery[redis]
# RUN pip install celery-singleton
# Create working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy contents
COPY . /usr/src/app/
RUN pyarmor -d obfuscate --recursive app/__init__.py
RUN rm -rf app
RUN mv dist app
# COPY ./trained_models/ /usr/src/app/
# COPY ./yolov5/ /usr/src/app/
# COPY ./config/ /usr/src/app/
# RUN git clone https://github.com/ultralytics/yolov5 /usr/src/yolov5

# Downloads to user config dir
ADD https://ultralytics.com/assets/Arial.ttf /root/.config/Ultralytics/

# Set environment variables
ENV OMP_NUM_THREADS=8

EXPOSE 5000
CMD uvicorn app.main:app --host 0.0.0.0 --port 5000