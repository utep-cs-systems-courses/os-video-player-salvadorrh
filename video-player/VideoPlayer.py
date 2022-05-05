#! /usr/bin/env python3

from threading import Thread
from PCQueue import PCQueue
import cv2
import base64
import os

frame_delay = 24

# Iterates through frames of a video, by extracting them
def extract_frames(video_name, frames_queue):
    # Open video clip and get first frame
    video_capture = cv2.VideoCapture(video_name)
    success, frame = video_capture.read()

    num_frame = 0
    print("EXTRACTING FRAMES")
    while success and num_frame < 72:
        # Gets a jpg encoded frame
        success, jpg_image = cv2.imencode('.jpg', frame)

        # Encode the frame as base 64 to make debugging easier
        jpg_as_text = base64.b64encode(jpg_image)

        # Add frame to queue of frames. (Instead of buffer in Freudenthal's code)
        frames_queue.enqueue(frame)

        # Get next frame
        success, frame = video_capture.read()
        print(f'Reading frame: {num_frame} {success}')
        num_frame += 1

    print("FINISHED EXTRACTING FRAMES")
    frames_queue.kill()


# Iterates through frames of a video, and converts them to grayscale
def convert_grayscale(extract_queue, grayscale_queue):
    num_frame = 0
    print("CONVERTING TO GRAYSCALE")

    while extract_queue.is_active() or not extract_queue.is_empty():
        original_frame = extract_queue.dequeue()
        print(f'Converting frame: {num_frame}')

        grayscale_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)

        grayscale_queue.enqueue(grayscale_frame)
        num_frame += 1

    print('FINISHED CONVERTING TO GRAYSCALE')
    grayscale_queue.kill()


# Displays all frames of video
def displaying_frames(grayscale_queue):
    num_frame = 0
    print("DISPLAYING FRAMES")

    while grayscale_queue.is_active() or not grayscale_queue.is_empty():
        # Get frame
        frame = grayscale_queue.dequeue()
        print(f'Displaying frame: {num_frame}')

        # Display the frame in a window called "Video"
        cv2.imshow('Video Grayscale', frame)

        # Wait for 24 ms and check if the user wants to quit
        if cv2.waitKey(frame_delay) and 0xFF == ord("q"):
            break

        num_frame += 1

    print("FINISHED DISPLAYING ALL FRAMES")
    cv2.destroyAllWindows()


def main():
    # Asks user for video
    video_name = ""
    #while not os.path.exists(video_name):
    #    video_name = input("What video do you want to see? ")

    video_name = "../clip.mp4"

    extract_queue = PCQueue()    # Original frames Queue
    grayscale_queue = PCQueue()  # Grayscale frames Queue

    # Concurrently produce and consume.
    extraction_thread = Thread(target=extract_frames, args=(video_name, extract_queue))
    extraction_thread.start()
    convert_grayscale_thread = Thread(target=convert_grayscale, args=(extract_queue, grayscale_queue))
    convert_grayscale_thread.start()
    display_thread = Thread(target=displaying_frames, args=(grayscale_queue,))
    display_thread.start()
    display_thread.join()


if __name__ == "__main__":
    main()
