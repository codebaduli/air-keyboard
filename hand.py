import cv2
import mediapipe as mp
import math


# -----------------------------------
# Function to calculate distance
# between two landmarks
# -----------------------------------

def calculate_distance(point1, point2):

    dx = point1.x - point2.x
    dy = point1.y - point2.y

    distance = math.sqrt(
        dx ** 2 + dy ** 2
    )

    return distance


# -----------------------------------
# Function to find the key
# under the fingertip
# -----------------------------------

def get_key(tip_x, tip_y, keys):

    for key in keys:

        name, action, x1, y1, x2, y2 = key

        if x1 < tip_x < x2 and y1 < tip_y < y2:
            return key

    return None


# -----------------------------------
# MediaPipe setup
# -----------------------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# -----------------------------------
# Open webcam
# -----------------------------------

cap = cv2.VideoCapture(0)


# -----------------------------------
# Press state
# -----------------------------------

press_state = False


# -----------------------------------
# Distance thresholds
# -----------------------------------

TOUCH_RATIO = 0.35
RELEASE_RATIO = 0.50


# -----------------------------------
# Text that has been typed
# -----------------------------------

typed_text = ""


# -----------------------------------
# Keyboard layout
# -----------------------------------

keyboard_rows = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]


# -----------------------------------
# Main loop
# -----------------------------------

while True:

    # Get camera frame
    success, frame = cap.read()

    if not success:
        print("Could not read frame")
        break

    # -----------------------------------
    # Frame dimensions
    # -----------------------------------

    height, width, _ = frame.shape

    # -----------------------------------
    # Keyboard settings
    # -----------------------------------

    key_width = 45
    key_height = 45
    gap = 5

    start_y = int(height * 0.50)

    # -----------------------------------
    # Create keyboard
    # -----------------------------------

    keys = []

    for row_index, row in enumerate(keyboard_rows):

        row_width = (
            len(row) * key_width
            + (len(row) - 1) * gap
        )

        row_start_x = (
            width - row_width
        ) // 2

        row_y = (
            start_y
            + row_index * (key_height + gap)
        )

        for key_index, letter in enumerate(row):

            x1 = (
                row_start_x
                + key_index * (key_width + gap)
            )

            y1 = row_y

            x2 = x1 + key_width
            y2 = y1 + key_height

            keys.append(
                (
                    letter,
                    letter,
                    x1,
                    y1,
                    x2,
                    y2
                )
            )

    # -----------------------------------
    # Special keys
    # -----------------------------------

    special_y = (
        start_y
        + 3 * (key_height + gap)
    )

    # SPACE
    space_width = 180

    space_x1 = (
        width - space_width
    ) // 2

    keys.append(
        (
            "SPACE",
            " ",
            space_x1,
            special_y,
            space_x1 + space_width,
            special_y + key_height
        )
    )

    # BACKSPACE
    back_width = 100

    back_x1 = (
        space_x1
        + space_width
        + gap
    )

    keys.append(
        (
            "BACK",
            "BACKSPACE",
            back_x1,
            special_y,
            back_x1 + back_width,
            special_y + key_height
        )
    )

    # ENTER
    enter_width = 80

    enter_x1 = (
        space_x1
        - gap
        - enter_width
    )

    keys.append(
        (
            "ENTER",
            "ENTER",
            enter_x1,
            special_y,
            enter_x1 + enter_width,
            special_y + key_height
        )
    )

    # -----------------------------------
    # Convert BGR → RGB
    # -----------------------------------

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # -----------------------------------
    # Process frame
    # -----------------------------------

    results = hands.process(rgb_frame)

    current_key = None
    tip_x = None
    tip_y = None

    # -----------------------------------
    # Find fingertip
    # -----------------------------------

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]

        index_tip = hand_landmarks.landmark[8]

        tip_x = int(
            index_tip.x * width
        )

        tip_y = int(
            index_tip.y * height
        )

        current_key = get_key(
            tip_x,
            tip_y,
            keys
        )

    # -----------------------------------
    # Draw keyboard
    # -----------------------------------

    for key in keys:

        name, action, x1, y1, x2, y2 = key

        # Highlight current key
        if current_key is not None:

            if current_key[0] == name:
                thickness = 4
            else:
                thickness = 2

        else:

            thickness = 2

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 255, 255),
            thickness
        )

        # -----------------------------------
        # Display key text
        # -----------------------------------

        display_name = name

        text_size = cv2.getTextSize(
            display_name,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            2
        )[0]

        text_x = (
            x1
            + (x2 - x1 - text_size[0]) // 2
        )

        text_y = (
            y1
            + (y2 - y1 + text_size[1]) // 2
        )

        cv2.putText(
            frame,
            display_name,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

    # -----------------------------------
    # Hand detection
    # -----------------------------------

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]

        # -----------------------------------
        # Fingertips
        # -----------------------------------

        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]

        # -----------------------------------
        # Hand reference points
        # -----------------------------------

        index_mcp = hand_landmarks.landmark[5]
        pinky_mcp = hand_landmarks.landmark[17]

        # -----------------------------------
        # Calculate fingertip distance
        # -----------------------------------

        finger_distance = calculate_distance(
            index_tip,
            middle_tip
        )

        # -----------------------------------
        # Calculate hand size
        # -----------------------------------

        hand_size = calculate_distance(
            index_mcp,
            pinky_mcp
        )

        # -----------------------------------
        # Calculate normalized ratio
        # -----------------------------------

        if hand_size > 0:

            finger_ratio = (
                finger_distance / hand_size
            )

        else:

            finger_ratio = 999

        # -----------------------------------
        # Middle fingertip coordinates
        # -----------------------------------

        middle_x = int(
            middle_tip.x * width
        )

        middle_y = int(
            middle_tip.y * height
        )

        # -----------------------------------
        # Press detection
        # -----------------------------------

        if not press_state:

            if finger_ratio < TOUCH_RATIO:

                press_state = True

                if current_key is not None:

                    key_name = current_key[0]
                    action = current_key[1]

                    # -----------------------------------
                    # Normal letter
                    # -----------------------------------

                    if len(action) == 1:

                        typed_text += action

                        print(
                            "PRESSED:",
                            key_name
                        )

                    # -----------------------------------
                    # Space
                    # -----------------------------------

                    elif action == " ":

                        typed_text += " "

                        print(
                            "PRESSED: SPACE"
                        )

                    # -----------------------------------
                    # Backspace
                    # -----------------------------------

                    elif action == "BACKSPACE":

                        typed_text = typed_text[:-1]

                        print(
                            "PRESSED: BACKSPACE"
                        )

                    # -----------------------------------
                    # Enter
                    # -----------------------------------

                    elif action == "ENTER":

                        typed_text += "\n"

                        print(
                            "PRESSED: ENTER"
                        )

        else:

            if finger_ratio > RELEASE_RATIO:

                press_state = False

        # -----------------------------------
        # Draw hand landmarks
        # -----------------------------------

        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        # -----------------------------------
        # Draw index fingertip
        # -----------------------------------

        cv2.circle(
            frame,
            (tip_x, tip_y),
            8,
            (255, 0, 0),
            -1
        )

        # -----------------------------------
        # Draw middle fingertip
        # -----------------------------------

        cv2.circle(
            frame,
            (middle_x, middle_y),
            8,
            (0, 255, 0),
            -1
        )

        # -----------------------------------
        # Draw line between fingertips
        # -----------------------------------

        cv2.line(
            frame,
            (tip_x, tip_y),
            (middle_x, middle_y),
            (255, 255, 0),
            2
        )

        # -----------------------------------
        # Display ratio
        # -----------------------------------

        cv2.putText(
            frame,
            f"Ratio: {finger_ratio:.3f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2
        )

        # -----------------------------------
        # Display press state
        # -----------------------------------

        state_text = (
            "PRESSED"
            if press_state
            else "RELEASED"
        )

        cv2.putText(
            frame,
            f"State: {state_text}",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2
        )

        # -----------------------------------
        # Display current key
        # -----------------------------------

        if current_key is not None:

            cv2.putText(
                frame,
                f"Key: {current_key[0]}",
                (20, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 255, 0),
                2
            )

    else:

        # No hand detected
        press_state = False

    # -----------------------------------
    # Display typed text
    # -----------------------------------

    cv2.rectangle(
        frame,
        (20, 110),
        (width - 20, 200),
        (255, 255, 255),
        2
    )

    # Display text line by line
    text_lines = typed_text.split("\n")

    y_position = 145

    for line in text_lines:

        cv2.putText(
            frame,
            line,
            (30, y_position),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        y_position += 30

    # -----------------------------------
    # Display camera
    # -----------------------------------

    cv2.imshow(
        "Air Keyboard",
        frame
    )

    # -----------------------------------
    # Press q to exit
    # -----------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------------
# Cleanup
# -----------------------------------

cap.release()
cv2.destroyAllWindows()