FROM node:10-alpine

# Install dependencies
RUN apk add --no-cache libshout libshout-dev ffmpeg python3
RUN apk add --no-cache make automake gcc g++ subversion python3-dev

# Install pip
RUN python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel

# Copy app files
COPY . /opt/

# Build web assets
WORKDIR /opt/app/
RUN yarn install
RUN yarn build

# Install python dependencies
WORKDIR /opt/
RUN pip3 install -r requirements.txt

# Set config
ENV NITRO_ICECAST_HOST "icecast"
ENV NITRO_ICECAST_PORT "8000"
ENV NITRO_ICECAST_PASSWORD "password"
ENV NITRO_YOUTUBE_KEY "12345"

# Set persistant volumes
VOLUME ["/opt/songs"]

# Start
CMD ["python3", "index.py"]