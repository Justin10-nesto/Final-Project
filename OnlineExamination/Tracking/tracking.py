import cv2
import mediapipe as mp

# Set up MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Set up webcam capture
cap = cv2.VideoCapture(0)

# Initialize variables
talk_counter = 0
look_counter = 0
talk_threshold = 30  # Number of consecutive frames to consider as talking
look_threshold = 30  # Number of consecutive frames to consider as looking outside

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB for processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    results = face_detection.process(rgb_frame)

    # Reset counters if no faces detected
    if not results.detections:
        talk_counter = 0
        look_counter = 0
        continue

    # Iterate over detected faces
    for detection in results.detections:
        bbox = detection.location_data.relative_bounding_box
        x, y, w, h = int(bbox.xmin * frame.shape[1]), int(bbox.ymin * frame.shape[0]), \
                     int(bbox.width * frame.shape[1]), int(bbox.height * frame.shape[0])

        # Draw bounding box on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Check for talking
        if detection.speech_likelihood > mp_face_detection.FaceDetection.MediumLikelihood:
            talk_counter += 1
        else:
            talk_counter = 0

        # Check for looking outside
        if x < 100 or x + w > frame.shape[1] - 100 or y < 100 or y + h > frame.shape[0] - 100:
            look_counter += 1
        else:
            look_counter = 0

        # Check if student is talking or looking outside for a long duration
        if talk_counter >= talk_threshold:
            print("Student is talking for a long duration!")
            # Add your action here, such as displaying a warning message or notifying the exam proctor

        if look_counter >= look_threshold:
            print("Student is looking outside for a long duration!")
            # Add your action here, such as displaying a warning message or notifying the exam proctor

    # Display the frame
    cv2.imshow("Webcam", frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
