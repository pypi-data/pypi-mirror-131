from typing import List, Tuple
import cv2
import io
import time
import imagehash
import threading
import cv2
from contextlib import contextmanager
from PIL import Image
from fluxhelper import Logger
from queue import Queue


VIDEO_MAPPINGS = {
    "video/x-msvideo": ".avi",
    "video/mp4": ".mp4",
    "video/mpeg": ".mpeg",
    "video/ogg": ".ogv",
    "video/mp2t": ".ts",
    "video/webm": ".webm",
    "video/x-matroska": ".mkv",
    "video/quicktime": ".mov"
}


@contextmanager
def VideoCapture(*args, **kwargs):
    cap = cv2.VideoCapture(*args, **kwargs)
    try:
        yield cap
    finally:
        cap.release()


def extractGifFrames(filelike: io.BytesIO, logging: Logger, uniqueness: float) -> List[Tuple[Image.Image, imagehash.ImageHash]]:
    """
    Extract frames from a filelike object.
    """

    frames = []

    start = time.time()
    with Image.open(filelike) as img:

        if logging:
            logging.debug(f"Extracting {img.n_frames} frames from a GIF")

        for frame in range(img.n_frames):
            img.seek(frame)
            go = True
            hashed = imagehash.average_hash(img)

            if len(frames) > 1:
                for fc in frames:
                    if (fc[1] - hashed) < uniqueness:
                        go = False
                        break

            if go:
                frames.append((img, hashed))

    end = round((time.time() - start) * 1000, 2)
    if logging:
        logging.debug(f"Extracted {len(frames)} unique frames in {end}ms.")

    return frames


def extractVideoFrames(filepath: str, logging: Logger, uniqueness: float, workers: int) -> List[Tuple[Image.Image, imagehash.ImageHash]]:
    """
    Extract unique frames from a video file path.
    """

    queue = Queue()
    frames = Queue()
    total = 0
    frameCount = cv2.VideoCapture(filepath).get(cv2.CAP_PROP_FRAME_COUNT)

    start = time.time()
    def p():
        while True:
            frame = queue.get()
            if frame is None:
                logging.debug("Exiting worker...")
                break
            
            frame = frame[:, :, ::-1]
            with Image.fromarray(frame) as frame:
                hashed = imagehash.average_hash(frame)
                go = True

                if len(list(frames.queue)) > 1:
                    for fc in list(frames.queue):
                        if (fc[1] - hashed) < uniqueness:
                            go = False
                            break
                if go:
                    frames.put((frame, hashed))
            queue.task_done()

    if frameCount <50:
        logging.warning("There are less than 20 frames, using 1 worker instead as it should do the job.")
        workers = 1

    # Construct workers
    funcs = [p] * workers

    # Launch workers
    for i, t in enumerate(funcs):
        th = threading.Thread(target=t, daemon=True)
        th.start()
        logging.debug(f"Launched worker {i}")
    
    # Put frames into queue
    logging.debug("Extracting frames...")
    with VideoCapture(filepath) as cap:

        status, frame = cap.read()
        while status:
            queue.put(frame)

            total += 1
            status, frame = cap.read()

    # Wait for all workers to be finished
    logging.debug("Waiting for workers to finish...")
    queue.join()

    logging.debug("Workers finished, exiting them...")
    for i in range(workers):
        queue.put(None)

    end = round((time.time() - start) * 1000, 2)
    frames = list(frames.queue)

    if logging:
        logging.debug(
            f"Extracted {len(frames)}/{total} unique frames in {end}ms.")
    return frames
