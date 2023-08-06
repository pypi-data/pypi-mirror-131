import requests
import time
import gc
import tempfile
import os
import cv2
import statistics
import numpy as np
from . import helpers
from nsfw_detector import predict
from fluxhelper import Logger
from .exceptions import *
from PIL import Image
from io import BytesIO

class Classifier:
    def __init__(self, model: str, logging: Logger = None, **kwargs):
        self.model = predict.load_model(model)

        if not logging:
            self.logging = Logger()
        else:
            self.logging = logging

        # Params
        self.frameUniqueness = kwargs.get('frameUniqueness', 5)
        self.imgSize = kwargs.get("imgSize", (224, 224))
        self.workers = kwargs.get("workers", 4)

    def classify(self, url: str) -> str:
        """
        Classify a image/video url.
        
        Parameters
        ----------
        `content` : str
            The url of the image/video to classify.
        
        Returns
        -------
        {
            "contentType": str,
            "data": {
                if video or gif:
                    "frames": {
                        frame_number: {
                            "sexy": float,
                            "neutral": float,
                            "porn": float,
                            "hentai": float,
                            "drawings": float
                        },
                        ...
                    },
                    "mean": float
                else:
                    "sexy": float,
                    "neutral": float,
                    "porn": float,
                    "hentai": float,
                    "drawings": float
            }
        }

        Raises
        ------
        `InternalRequestError` :
            When there's an error getting the content from the url.
        `UnknownContentType` :
            When the content type is not supported or unknown, mostly raised in video types.
        """
        
        data = {"contentType": None}

        try:
            start = time.time()

            with requests.Session() as session:
                r = session.get(url)

            end = round((time.time() - start) * 1000, 2)
            self.logging.debug(f"Getting content from url took {end}ms")

            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise InternalRequestError(e)
        
        data["contentType"] = r.headers["Content-Type"].lower().strip()
        predictionType = "single"

        if data["contentType"] == "image/gif":
            predictionType = "multiple"

            f = BytesIO(r.content)
            frames = helpers.extractGifFrames(f, self.logging, self.frameUniqueness)
            f.close()

        elif data["contentType"].startswith("video/"):
            predictionType = "multiple"
            
            suffix = helpers.VIDEO_MAPPINGS.get(data["contentType"])
            if not suffix:
                raise UnknownContentType(data["contentType"])

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                path = tmp.name
                tmp.write(r.content)
                tmp.close()

                frames = helpers.extractVideoFrames(path, self.logging, self.frameUniqueness, self.workers)
                os.unlink(path)
        else:
            raise UnknownContentType(data["contentType"])
    
        if predictionType == "multiple":
            start = time.time()
            nds = []
            for frame in frames:

                img = frame[0]
                img = img.convert("RGB")

                img = np.array(img, dtype=np.float64)
                img = cv2.resize(img, self.imgSize)
                img /= 255

                nds.append(img)

            nds = np.asarray(nds)
            end = round((time.time() - start) * 1000, 2)
            self.logging.debug(f"Converting frames to numpy arrays and resizing took {end}ms.")

            self.logging.debug(f"Classifying {len(nds)} frames.")
            start = time.time()
            r = predict.classify_nd(self.model, nds)
            _ = gc.collect()
            end = round((time.time() - start) * 1000, 2)
            self.logging.debug(f"Classifying {len(nds)} frames took {end}ms.")
            self.logging.debug(f"Processing {len(r)} results.")

            start = time.time()
            classified = {i: c for i, c in enumerate(r)}
            end = round((time.time() - start) * 1000, 2)
            self.logging.debug(f"Processing {len(r)} results took {end}ms.")

            data["data"] = {
                "frames": classified,
            }

            return data

        elif predictionType == "single":
            img = Image.open(BytesIO(r.content))
            img = img.convert("RGB")
            img = np.array(img, dtype=np.float64)
            img = cv2.resize(img, self.imgSize)
            img /= 255

            start = time.time()
            r = predict.classify_nd(self.model, np.asarray([img]))
            _ = gc.collect()
            end = round((time.time() - start) * 1000, 2)
            self.logging.debug(f"Classifying image took {end}ms.")

            data["data"] = r[0]
            return data
