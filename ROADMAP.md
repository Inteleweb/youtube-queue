# Roadmap

This document outlines the planned improvements and new features for the YouTube Queue application.

## Stage 1: Improvements and Fixes

This stage focuses on improving the existing features and stability of the application.

-   **Enhanced Error Handling:**
    -   Implement more specific error handling for `yt_dlp` to gracefully handle cases like private, deleted, or unavailable videos.
    -   Provide clear feedback to the user when a download fails.

-   **UI/UX Enhancements:**
    -   Display video titles, thumbnails, and duration in the queue.
    -   Show real-time download progress for each video.
    -   Implement a feature to remove videos from the queue.
    -   Add user feedback on the UI for actions like adding a video or removing one.

-   **Configuration:**
    -   Use environment variables to configure the download directory, queue file location, and other settings.

-   **Logging:**
    -   Integrate a structured logging library to provide better insights into the application's behavior and for easier debugging.

-   **Dependency Management:**
    -   Create a `requirements.txt` file to manage Python dependencies explicitly.

## Stage 2: New Features

This stage focuses on adding new functionality to the application.

-   **Video Format and Quality Selection:**
    -   Allow users to choose the desired video format (e.g., mp4, webm) and quality (e.g., 1080p, 720p, audio only).

-   **Playlist Support:**
    -   Add the ability to download all videos from a YouTube playlist by providing the playlist URL.

-   **Authentication:**
    -   Implement a simple authentication mechanism (e.g., username/password) to secure the application.

-   **API Enhancements:**
    -   Develop a more comprehensive REST API for managing the queue, including endpoints for deleting, reordering, and viewing the status of downloads.

-   **Database Integration:**
    -   Replace the current JSON file-based queue with a more robust database system like SQLite or PostgreSQL to improve data integrity and performance.

-   **Real-time Updates with WebSockets:**
    -   Use WebSockets to provide real-time updates to the user interface, such as when a download starts, progresses, or completes.

-   **YouTube Search:**
    -   Integrate a search feature to allow users to search for YouTube videos directly within the application and add them to the queue.
