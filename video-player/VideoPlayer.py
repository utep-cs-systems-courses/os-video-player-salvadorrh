#! /usr/bin/env python3

from threading import Thread
from PCQueue import PCQueue
import cv2
import os


# Iterates through frames of a video, by extracting them
def extract_frames(file_name, queue):
    print("Extracting frames")


# Iterates through frames of a video, and converts them to grayscale
def convert_grayscale(queue1, queue2):
    print("Converting to grayscale")


# Displays all frames of video
def displaying_frames(queue2):
    print("Displaying frames")


def main():
    # Asks user for video
    file_name = ""
    while not os.path.exists(file_name):
        file_name = input("What video do you want to see? ")

    extract_queue = PCQueue()    # Original frames Queue
    grayscale_queue = PCQueue()  # Grayscale frames Queue

    # Concurrently produce and consume.
    extraction_thread = Thread(target=extract_frames, args=(file_name, extract_queue))
    extraction_thread.start()
    convert_grayscale_thread = Thread(target=convert_grayscale, args=(extract_queue, grayscale_queue))
    convert_grayscale_thread.start()
    display_thread = Thread(target=displaying_frames, args=(grayscale_queue,))
    display_thread.start()


if __name__ == "__main__":
    main()
