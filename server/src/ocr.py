import cv2
import numpy as np
import easyocr

from spacial_bin import SpacialBin

reader = easyocr.Reader(['en'])


def recognize(image):
    """
    Obtain rows + cols from nonogram image
    Writes debug image to ./out.png

    :param image: Path to image
    :return: rows, cols
    """

    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 11, 30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
    crop = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 11, 30)
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    areas = []

    for c in cnts:
        area = cv2.contourArea(c)
        areas.append(area)

    # Filter small areas (might just be an intersection or dot)
    cnts = [c for c in cnts if cv2.contourArea(c) > min(areas) * 1.25]

    rect = cv2.boundingRect(cnts[0])
    is_column_mode = False
    tolerance = rect[2] // 2 # Tolerance within 1 char width

    # Bins for detecting rows / cols + bounding boxes for rows / cols
    row_bin = SpacialBin(tolerance)
    col_bin = SpacialBin(tolerance)
    row_bound_bin = SpacialBin(tolerance)
    col_bound_bin = SpacialBin(tolerance)

    # In general features start on bottom row rightmost and go left and up
    # Note this assumption doesn't hold
    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        subimage = crop[y:y + h, x:x + w]

        p = reader.recognize(subimage, allowlist="0123456789")
        read_char = int(p[0][1])

        if x > image.shape[0] // 2 + tolerance:
            is_column_mode = True

        if not is_column_mode:
            row_bin.set(y, [(read_char, x)] + row_bin.get(y, []))

            # Bounding box for the row
            if not row_bound_bin.haskey(y):
                row_bound_bin.add(y, [9999999, 9999999, 0, 0])
            bounds = row_bound_bin.get(y)
            row_bound_bin.set(y, [min(x, bounds[0]), min(y, bounds[1]), max(x + w, bounds[2]), max(y + h, bounds[3])])
        else:
            col_bin.set(x, [(read_char, y)] + col_bin.get(x, []))

            # Bounding box for the col
            if not col_bound_bin.haskey(x):
                col_bound_bin.add(x, [9999999, 9999999, 0, 0])
            bounds = col_bound_bin.get(x)
            col_bound_bin.set(x, [min(x, bounds[0]), min(y, bounds[1]), max(x + w, bounds[2]), max(y + h, bounds[3])])

        image = cv2.putText(image, str(read_char), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0),
                            2, cv2.LINE_AA)

    # Draw row / col bounding boxes
    for row in row_bound_bin.to_list():
        x1, y1, x2, y2 = row
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 120, 255), 2)
    for col in col_bound_bin.to_list():
        x1, y1, x2, y2 = col
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 120, 0), 2)

    cv2.imwrite('out.png', image)

    # Sort each row + col by x & y value respectively
    rows, cols = row_bin.to_list(), col_bin.to_list()
    rows = [[x[0] for x in sorted(r, key=lambda x: x[1])] for r in rows]
    cols = [[x[0] for x in sorted(c, key=lambda x: x[1])] for c in cols]
    return rows, cols
