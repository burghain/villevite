# escape=\

# The base image provides the scanning Blender (4.4 + vLiDAR toolchain).
# The generation Blender (5.2.0) is downloaded by `dev.py build` inside the image.
ARG BASE_IMAGE=simonsose25/blender-scancam:4.4.0-alpha
FROM ${BASE_IMAGE}
ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu
# copy villevite into image
COPY . ./villevite

# copy vLidar addon into image
COPY pointCloudRender-bachelorThesis.zip pointCloudRender-bachelorThesis.zip

WORKDIR /home/ubuntu/villevite

RUN python3 dev.py build

ENTRYPOINT python3 prepare_scan.py