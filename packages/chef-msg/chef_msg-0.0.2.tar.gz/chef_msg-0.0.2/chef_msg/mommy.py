from pathlib import Path

import cv2 as cv


def kkakdugi(img_path: str, size=256, overlap_factor=1):
    """
    chop image
    """
    img_name = Path(img_path).name
    save_dir = Path('./chopped') / img_name
    save_dir.mkdir(parents=True, exist_ok=True)

    img = cv.imread(img_path)
    w, h, ch = img.shape
    print(f':: image read {img.shape}')

    if overlap_factor > 0:
        max_h_count = int(w / size) * overlap_factor
        w_offset = int((w - size) / max_h_count)
        w_chop_count = max_h_count + 1

        max_h_count = int(h / size) * overlap_factor
        h_offset = int((h - size) / max_h_count)
        h_chop_count = max_h_count + 1

        for h in range(h_chop_count):
            h0 = h * h_offset
            h1 = h0 + size
            for w in range(w_chop_count):
                w0 = w * w_offset
                w1 = w0 + size
                region = img[h0:h1, w0:w1]
                try:
                    cv.imwrite(f'{save_dir}/{h:02d}_{w:02d}_{img_name}', region)
                except cv.error:
                    pass
                print(f':: "{h:02d}_{w:02d}_{img_name}" saved.')
