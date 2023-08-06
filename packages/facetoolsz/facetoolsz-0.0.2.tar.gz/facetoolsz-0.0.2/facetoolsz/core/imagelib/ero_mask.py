import cv2
import numpy as np


def ero_mask(face_mask, ero=20, blur=50, input_size=256):
    # add zero pad
    new_face_mask = np.pad(face_mask, input_size, mode='constant')
    # print(face_mask.shape)
    if ero > 0:
        new_face_mask = cv2.erode(new_face_mask, cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (ero, ero)), iterations=1)
    elif ero < 0:
        new_face_mask = cv2.dilate(new_face_mask, cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (-ero, -ero)), iterations=1)
    else:
        new_face_mask = new_face_mask

    clip_size = input_size + blur // 2

    new_face_mask[:clip_size, :] = 0
    new_face_mask[-clip_size:, :] = 0
    new_face_mask[:, :clip_size] = 0
    new_face_mask[:, -clip_size:] = 0

    if blur > 0:
        blur = blur + (1-blur % 2)
        wrk_face_mask_a_0 = cv2.GaussianBlur(new_face_mask, (blur, blur), 0)

    wrk_face_mask_a_0 = wrk_face_mask_a_0[input_size:-
                                          input_size, input_size:-input_size]

    wrk_face_mask_a_0 = np.clip(wrk_face_mask_a_0, 0, 1)

    return wrk_face_mask_a_0