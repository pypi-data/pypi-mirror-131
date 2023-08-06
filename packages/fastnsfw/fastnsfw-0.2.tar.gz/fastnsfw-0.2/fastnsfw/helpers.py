from typing import List, Tuple
import cv2
import io
import time
import imagehash
import cv2
from contextlib import contextmanager
from PIL import Image
from fluxhelper import Logger


VIDEO_MAPPINGS = {
    "video/x-msvideo": ".avi",
    "video/mp4": ".mp4",
    "video/mpeg": ".mpeg",
    "video/ogg": ".ogv",
    "video/mp2t": ".ts",
    "video/webm": ".webm",
    "video/x-matroska": ".mkv"
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


def extractVideoFrames(filepath: str, logging: Logger, uniqueness: float) -> List[Tuple[Image.Image, imagehash.ImageHash]]:
    """
    Extract unique frames from a video file path.
    """

    frames = []
    total = 0

    start = time.time()
    with VideoCapture(filepath) as cap:

        status, frame = cap.read()
        while status:
            frame = frame[:, :, ::-1]

            with Image.fromarray(frame) as frame:
                hashed = imagehash.average_hash(frame)
                go = True

                if len(frames) > 1:
                    for fc in frames:
                        if (fc[1] - hashed) < uniqueness:
                            go = False
                            break
                
                if go:
                    frames.append((frame, hashed))
            
            total += 1
            status, frame = cap.read()
    end = round((time.time() - start) * 1000, 2)

    if logging:
        logging.debug(f"Extracted {len(frames)}/{total} unique frames in {end}ms.")
    return frames
