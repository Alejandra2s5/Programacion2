import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import cv2
import face_recognition

class FaceAuthApp(App):

    def build(self):
        # Crea un layout principal
        main_layout = GridLayout(cols=1, padding=10)

        # Etiqueta para mostrar instrucciones
        instruction_label = Label(text="Selecciona una opción:", font_size=20)
        main_layout.add_widget(instruction_label)

        # Botón para registrar rostro
        register_button = Button(text="Registrar rostro")
        register_button.bind(on_press=self.register_face)
        main_layout.add_widget(register_button)

        # Botón para autenticar rostro
        auth_button = Button(text="Autenticar rostro")
        auth_button.bind(on_press=self.authenticate_face)
        main_layout.add_widget(auth_button)

        return main_layout

    def capture_frame(self):
        # Crea una instancia de la cámara
        camera = Camera(index=0, resolution=(640, 480))
        main_layout.add_widget(camera)

        # Captura un frame de la cámara
        frame = camera.texture.as_image()

        # Elimina la cámara del layout
        main_layout.remove_widget(camera)

        # Convierte el frame a formato OpenCV
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

        return frame

    def register_face(self, instance):
        # Captura el rostro del usuario
        captured_face = self.capture_frame()

        # Si se capturó un rostro, procede al registro
        if captured_face is not None:
            name = input("Ingresa tu nombre: ")
            encodings = face_recognition.face_encodings(captured_face)[0]
            with open(f"images/{name}.txt", "w") as file:
                file.write(str(encodings))
            print(f"Rostro registrado para {name}")

    def authenticate_face(self, instance):
        # Captura el rostro del usuario
        captured_face = self.capture_frame()

        # Si se capturó un rostro, procede a la autenticación
        if captured_face is not None:
            known_encodings = []
            known_names = []

            for filename in os.listdir("images"):
                if filename.endswith(".txt"):
                    name = filename[:-4]
                    with open(f"images/{filename}", "r") as file:
                        encodings = np.fromstring(file.read(), dtype=np.float32)
                        known_encodings.append(encodings)
                        known_names.append(name)

            unknown_encodings = face_recognition.face_encodings(captured_face)[0]
            distances = face_recognition.face_distance(known_encodings, unknown_encodings)
            index_min = distances.argmin()
            name_predicted = known_names[index_min]
            distance_min = distances[index_min]

            if distance_min < 0.5:
                print(f"¡Bienvenido/a {name_predicted}!")
            else:
                print(f"Rostro desconocido: {distance_min:.2f}")
