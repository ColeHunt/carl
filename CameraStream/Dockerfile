FROM alpine:latest AS run-env

WORKDIR /home

# Copy CameraStream.sh to the home directory of the container
COPY CameraStream.sh ./

# Install all the dependencies for mjpg-streamer
RUN apk update && \
    apk add git && \
    apk add make && \
    apk add cmake && \
    apk add gcc && \
    apk add musl-dev && \
    apk add linux-headers && \
    apk add jpeg-dev

# Get mjpg-streamer and install it
RUN git clone https://github.com/jacksonliam/mjpg-streamer.git
WORKDIR /home/mjpg-streamer/mjpg-streamer-experimental
RUN make
RUN make install

WORKDIR /home

# Run the camera stream script
RUN chmod +x ./CameraStream.sh
ENTRYPOINT [ "./CameraStream.sh" ]