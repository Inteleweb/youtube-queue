# YouTube Queue

A simple web application to queue and download YouTube videos.

## Features

- Add YouTube videos to a queue.
- Videos are downloaded automatically in the background.
- View the current download queue.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Inteleweb/youtube-queue.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd youtube-queue
    ```
3.  Start the application using Docker Compose:
    ```bash
    docker-compose up -d
    ```
4.  The application will be available at [http://localhost:5000](http://localhost:5000).

## Technologies Used

- Python
- Flask
- yt-dlp
- Docker
- HTML/CSS
