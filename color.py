import numpy as np
import cv2


def gstreamer_pipeline(
        capture_width=1280,
        capture_height=720,
        display_width=1280,
        display_height=720,
        framerate=30,
        flip_method=0,
):
    return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=true"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
    )

val1 = 0
val2 = 0
val3 = 0
val4 = 0

def process(frame):
    global val1, val2, val3, val4
    rect_size = 100
    h_sensivity = 20
    s_h = 255
    v_h = 255
    s_l = 50
    v_l = 50
    width, height, channels = frame.shape

    start_point = (int(height / 2 - rect_size / 2 - 200), int(width / 2 - rect_size / 2))
    end_point = (int(height / 2 + rect_size / 2 - 200), int(width / 2 + rect_size / 2))

    start_point2 = (int(height / 2 - rect_size / 2 - 100), int(width / 2 - rect_size / 2))
    end_point2 = (int(height / 2 + rect_size / 2 - 100), int(width / 2 + rect_size / 2))

    start_point3 = (int(height / 2 - rect_size / 2), int(width / 2 - rect_size / 2))
    end_point3 = (int(height / 2 + rect_size / 2), int(width / 2 + rect_size / 2))

    start_point4 = (int(height / 2 - rect_size / 2 + 100), int(width / 2 - rect_size / 2))
    end_point4 = (int(height / 2 + rect_size / 2 + 100), int(width / 2 + rect_size / 2))

    color = (0, 0, 0)
    thickness = 2
    rect = cv2.rectangle(frame, start_point, end_point, color, thickness)
    rect2 = cv2.rectangle(frame, start_point2, end_point2, color, thickness)
    rect3 = cv2.rectangle(frame, start_point3, end_point3, color, thickness)
    rect4 = cv2.rectangle(frame, start_point4, end_point4, color, thickness)

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blue_upper = np.array([122 + h_sensivity, s_h, v_h])
    blue_lower = np.array([122 - h_sensivity, s_l, v_l])
    mask_frame = hsv_frame[start_point[1]:end_point[1] + 1, start_point[0]:end_point[0] + 1]
    mask_blue = cv2.inRange(mask_frame, blue_lower, blue_upper)
    blue_rate = np.count_nonzero(mask_blue) / (rect_size * rect_size)

    green_upper = np.array([60 + h_sensivity, s_h, v_h])
    green_lower = np.array([60 - h_sensivity, s_l, v_l])
    mask_frame2 = hsv_frame[start_point2[1]:end_point2[1] + 10, start_point2[0]:end_point2[0] + 10]
    mask_green = cv2.inRange(mask_frame2, green_lower, green_upper)
    green_rate = np.count_nonzero(mask_green) / (rect_size * rect_size)

    lightblue_upper = np.array([90 + h_sensivity, s_h, v_h])
    lightblue_lower = np.array([90 - h_sensivity, s_l, v_l])
    mask_frame3 = hsv_frame[start_point3[1]:end_point3[1] + 10, start_point3[0]:end_point3[0] + 10]
    mask_lightblue = cv2.inRange(mask_frame3, lightblue_lower, lightblue_upper)
    lightblue_rate = np.count_nonzero(mask_lightblue) / (rect_size * rect_size)

    pink_upper = np.array([160 + h_sensivity, s_h, v_h])
    pink_lower = np.array([160 - h_sensivity, s_l, v_l])
    mask_frame4 = hsv_frame[start_point4[1]:end_point4[1] + 10, start_point4[0]:end_point4[0] + 10]
    mask_pink = cv2.inRange(mask_frame4, pink_lower, pink_upper)
    pink_rate = np.count_nonzero(mask_pink) / (rect_size * rect_size)

    org = end_point
    org2 = end_point2[0] - 70, end_point2[1] + 20
    org3 = end_point3[0] - 70, end_point3[1] + 20
    org4 = end_point4[0] - 70, end_point4[1] + 20
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.7

    if blue_rate > 0.9:
        val1 = 1
        text = cv2.putText(rect, ' OK (blue) ', org, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        text = cv2.putText(rect, '  ', org, font, fontScale, color, thickness, cv2.LINE_AA)

    """again """
    if green_rate > 0.9 and val1:
        val2 = 1
        text2 = cv2.putText(rect2, ' OK (green) ', org2, font, fontScale, color, thickness, cv2.LINE_AA)
        rect2 = cv2.rectangle(frame, start_point2, end_point2, color, thickness)
    else:
        text2 = cv2.putText(rect2, '  ', org2, font, fontScale, color, thickness, cv2.LINE_AA)

    if lightblue_rate > 0.9 and val1 and val2:
        val3 = 1
        text3 = cv2.putText(rect3, ' OK (lightblue) ', org3, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        text3 = cv2.putText(rect3, '  ', org3, font, fontScale, color, thickness, cv2.LINE_AA)

    if pink_rate > 0.9 and val1 and val2 and val3:
        val4 = 1
        text4 = cv2.putText(rect4, ' OK (pink) ', org4, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        text4 = cv2.putText(rect4, '  ', org3, font, fontScale, color, thickness, cv2.LINE_AA)

    av_hue = np.average(mask_frame[:, :, 0])
    av_sat = np.average(mask_frame[:, :, 1])
    av_val = np.average(mask_frame[:, :, 2])
    average = [int(av_hue), int(av_sat), int(av_val)]

    if val1 and val2 and val3 and val4:
        text = cv2.putText(frame, 'Right password',
                           (int(height / 2 + rect_size / 2 - 180), int(width / 2 + rect_size / 2) + 50), font,
                           fontScale, (110, 150, 50), thickness, cv2.LINE_AA)

    text = cv2.putText(rect, str(average) + " " + str(blue_rate), (10, 50), font, fontScale, color, thickness,
                       cv2.LINE_AA)
    frame = text
    return frame


print('Press 4 to Quit the Application\n')

# Open Default Camera
cap = cv2.VideoCapture(0)  # gstreamer_pipeline(flip_method=4), cv2.CAP_GSTREAMER)

while (cap.isOpened()):
    # Take each Frame
    ret, frame = cap.read()

    # Flip Video vertically (180 Degrees)
    frame = cv2.flip(frame, 180)

    invert = process(frame)

    # Show video
    cv2.imshow('Cam', frame)

    # Exit if "4" is pressed
    k = cv2.waitKey(1) & 0xFF
    if k == 52:  # ord 4
        # Quit
        print('Good Bye!')
        break

# Release the Cap and Video
cap.release()
cv2.destroyAllWindows()
