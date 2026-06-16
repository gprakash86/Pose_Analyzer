import cv2
import mediapipe as mp
import numpy as np

# --------------------------
# Exercise Selection
# --------------------------

exercise = input(
    "1. Squat\n"
    "2. Push-up\n"
    "3. Horse Stance\n"
    "Enter choice: "
)

counter = 0
stage = None
import time

start_time = None




# --------------------------
# Angle Function
# --------------------------

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(
        c[1]-b[1],
        c[0]-b[0]
    ) - np.arctan2(
        a[1]-b[1],
        a[0]-b[0]
    )

    angle = np.abs(
        radians * 180.0 / np.pi
    )

    if angle > 180:
        angle = 360 - angle

    return angle

# --------------------------
# MediaPipe Setup
# --------------------------

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_drawing = mp.solutions.drawing_utils

# --------------------------
# Webcam
# --------------------------

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = pose.process(rgb_frame)

    try:

        landmarks = results.pose_landmarks.landmark

        # --------------------------
        # Common Landmarks
        # --------------------------

        hip = [
            landmarks[
                mp_pose.PoseLandmark.LEFT_HIP.value
            ].x,
            landmarks[
                mp_pose.PoseLandmark.LEFT_HIP.value
            ].y
        ]

        knee = [
            landmarks[
                mp_pose.PoseLandmark.LEFT_KNEE.value
            ].x,
            landmarks[
                mp_pose.PoseLandmark.LEFT_KNEE.value
            ].y
        ]

        ankle = [
            landmarks[
                mp_pose.PoseLandmark.LEFT_ANKLE.value
            ].x,
            landmarks[
                mp_pose.PoseLandmark.LEFT_ANKLE.value
            ].y
        ]

        shoulder = [
            landmarks[
                mp_pose.PoseLandmark.LEFT_SHOULDER.value
            ].x,
            landmarks[
                mp_pose.PoseLandmark.LEFT_SHOULDER.value
            ].y
        ]

        elbow = [
            landmarks[
                mp_pose.PoseLandmark.LEFT_ELBOW.value
            ].x,
            landmarks[
                mp_pose.PoseLandmark.LEFT_ELBOW.value
            ].y
        ]

        wrist = [
            landmarks[
                mp_pose.PoseLandmark.LEFT_WRIST.value
            ].x,
            landmarks[
                mp_pose.PoseLandmark.LEFT_WRIST.value
            ].y
        ]

        # --------------------------
        # Squat Mode
        # --------------------------

        if exercise == "1":

            name = "SQUATS"

            angle = calculate_angle(
                hip,
                knee,
                ankle
            )

            point = knee

            if angle > 160:

                if stage == "DOWN":
                    counter += 1

                stage = "UP"

            elif angle < 90:

                stage = "DOWN"

        # --------------------------
        # Push-up Mode
        # --------------------------

        elif exercise == "2":

            name = "PUSHUPS"

            elbow_angle = calculate_angle(
                shoulder,
                elbow,
                wrist
            )

            body_angle = calculate_angle(
                shoulder,
                hip,
                ankle
            )

            angle = elbow_angle
            point = elbow

            if body_angle < 150:

                cv2.putText(
                    frame,
                    "KEEP BODY STRAIGHT",
                    (150, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

            if body_angle > 150:

                if elbow_angle > 160:

                    if stage == "DOWN":
                        counter += 1

                    stage = "UP"

                elif elbow_angle < 90:

                    stage = "DOWN"



        elif exercise == "3":

            name = "HORSESTANCE"

            knee_angle = calculate_angle(
                hip,
                knee,
                ankle
            )

            torso_angle = calculate_angle(
                shoulder,
                hip,
                knee
            )

            angle = knee_angle
            point = knee

            if (
                80 <= knee_angle <= 110 and
                torso_angle > 110
            ):

                if start_time is None:
                    start_time = time.time()

                elapsed = int(
                    time.time() - start_time
                )

                cv2.putText(
                    frame,
                    f"TIME: {elapsed}s",
                    (10,120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    "HORSESTANCE",
                    (150,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

            else:

                start_time = None

                if torso_angle <= 110:

                    cv2.putText(
                        frame,
                        "DON'T LEAN FORWARD",
                        (100,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,0,255),
                        2
                    )

                elif knee_angle < 80:

                    cv2.putText(
                        frame,
                        "GO LOWER",
                        (150,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,0,255),
                        2
                    )

                elif knee_angle > 120:

                    cv2.putText(
                        frame,
                        "STANCE TOO LOW",
                        (120,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,0,255),
                        2
                    )
        # --------------------------
        # Display Angle
        # --------------------------

                cv2.putText(
                    frame,
                    str(int(angle)),
                    tuple(
                        np.multiply(
                            point,
                            [640, 480]
                        ).astype(int)
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2
                )
                print(
    "Knee:", int(knee_angle),
    "Torso:", int(torso_angle)
)

    except:
        pass

    # --------------------------
    # Draw Skeleton
    # --------------------------

    if results.pose_landmarks:

        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # --------------------------
    # Display Counter
    # --------------------------

    cv2.rectangle(
        frame,
        (0, 0),
        (250, 80),
        (245, 117, 16),
        -1
    )


    label = "COUNT"

    if exercise == "3":
        label = "TIME"

    cv2.putText(
        frame,
        label,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        str(counter),
        (10, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Exercise Analyzer",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()