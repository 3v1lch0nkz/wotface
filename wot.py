import os
import sys
import cv2 as cv
from pathlib import Path

# Function to get the Desktop path depending on the OS
def get_desktop_path():
    if sys.platform == "win32":  # Windows
        return str(Path.home() / "Desktop")
    elif sys.platform == "darwin":  # macOS
        return str(Path.home() / "Desktop")
    else:  # Linux or other UNIX-like systems
        return str(Path.home() / "Desktop")

# Load the custom Haar Cascade
# Replace 'path_to_your_custom_cascade.xml' with the path to your cascade file
if getattr(sys, 'frozen', False):  # For PyInstaller executable
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# READ HERE Multiple Path to the Haar Cascade goes Here (make sure to adjust this to your actual XML file path)
#cascade_path = os.path.join(base_path, 'res', 'haarcascade_frontalface_default.xml')  # Update for your custom cascade
#animal_cascade = cv.CascadeClassifier(cascade_path)

# READ HERE default testing path goes in, format your directories in Winblows10
animal_cascade = cv.CascadeClassifier(r"")

if animal_cascade.empty():
    print("Error: Could not load Haar Cascade.")
    sys.exit(1)

# Capture video from the cam device
cap = cv.VideoCapture(0)  # 0 for the default camera

if not cap.isOpened():
    print("Error: Could not open camera.")
    sys.exit(1)

while True:
    # read frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Step 4: Convert the frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Step 5: Detect objects (animals) in the frame
    animals = animal_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Step 6: Draw rectangles around detected animals
    for (x, y, w, h) in animals:
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv.putText(frame, 'Face', (x, y - 10), cv.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255), 2)
    # Step 7: Display the resulting frame
    cv.imshow('Live Animal Detection | Press Q to quit, C to capture', frame)

    # Step 8: Handle keypresses
    key = cv.waitKey(1) & 0xFF

    # Save the current frame when 'c' is pressed
    if key == ord('c'):
        desktop_path = get_desktop_path()  # Get the Desktop path
        save_path = os.path.join(desktop_path, 'captured_frame.jpg')
        cv.imwrite(save_path, frame)
        print(f"Frame saved at {save_path}")

    # Break the loop on 'q' key press
    if key == ord('q'):
        break

# clean exit release the capture and close windows
cap.release()
cv.destroyAllWindows()
