FROM alpine:latest AS run-env

WORKDIR /home

RUN apk update && \
    apk add git && \
    apk add make && \
    apk add cmake && \
    apk add gcc && \
    apk add musl-dev && \
    apk add linux-headers && \
    apk add jpeg-dev

RUN git clone https://github.com/jacksonliam/mjpg-streamer.git

WORKDIR /home/mjpg-streamer/mjpg-streamer-experimental

RUN make
RUN make install

WORKDIR /home

ENTRYPOINT [ mjpg_streamer -i "input_uvc.so -d /dev/video0" -o "output_http.so -w ./www" ]