
import face_recognition

# Print version to ensure it's imported correctly
print("face_recognition version:", face_recognition.__version__)

# Load a sample picture and learn how to recognize it.
image = face_recognition.load_image_file("path_to_sample_image.jpg")
face_locations = face_recognition.face_locations(image)

print("Found {} faces in the image.".format(len(face_locations)))
