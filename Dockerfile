# escape=\

FROM simonsose25/blender-scancam:4.4.0-alpha
ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu
# copy villevite into image
COPY . ./villevite

# copy vLidar addon into image
COPY pointCloudRender-bachelorThesis.zip pointCloudRender-bachelorThesis.zip

WORKDIR /home/ubuntu/villevite

RUN python3 dev.py build

ENTRYPOINT python3 prepare_scan.py