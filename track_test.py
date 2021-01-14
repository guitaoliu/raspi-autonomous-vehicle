import logging
from pathlib import Path

import numpy as np
from PIL import Image

from plugins import Track

logger = logging.getLogger(__name__)
data = Path("data")
imgs = ["data/" + str(img.name) for img in data.iterdir()]
imgs = sorted(imgs)

if __name__ == "__main__":
    track = Track()
    # for img in imgs:
    #     print(img)
    #     status = track.basic(np.asarray(Image.open(img))[:, :, ::-1])
    #     print(status)

    status = track.basic(np.asarray(Image.open("data/image-left.jpg"))[:, :, ::-1])
    print(status)
