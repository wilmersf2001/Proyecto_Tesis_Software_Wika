import os
import cv2
from mediapipe.python.solutions.holistic import FACEMESH_CONTOURS, POSE_CONNECTIONS, HAND_CONNECTIONS
from mediapipe.python.solutions.drawing_utils import draw_landmarks, DrawingSpec
import numpy as np
import pandas as pd
from typing import NamedTuple
from utils.Constants import Constants


def buscar_usuario_por_nombre(nombre):
    carpeta_buscada = Constants.URL_IMGS + "/users"
    archivos = os.listdir(carpeta_buscada)
    nombre = nombre + '.jpg'

    for archivo in archivos:
        if archivo.endswith('.jpg'):
            if archivo == nombre:
                ruta_imagen = os.path.join(nombre, archivo)
                return True
    return False


def eliminar_user_directorio(nombre):
    carpeta_buscada = Constants.URL_IMGS + "/users"
    archivos = os.listdir(carpeta_buscada)
    nombre = nombre + '.jpg'

    for archivo in archivos:
        if archivo.endswith('.jpg'):
            if archivo == nombre:
                os.remove(os.path.join(carpeta_buscada, archivo))
                return True
    return False


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def there_hand(results: NamedTuple) -> bool:
    return results.left_hand_landmarks or results.right_hand_landmarks


def get_actions(path):
    out = []
    for action in os.listdir(path):
        name, ext = os.path.splitext(action)
        if ext == ".h5":
            out.append(name)
    return out


def configurar_resolucion(camara):
    camara.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def draw_keypoints(image, results):

    draw_landmarks(
        image,
        results.face_landmarks,
        FACEMESH_CONTOURS,
        DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
        DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1),
    )

    draw_landmarks(
        image,
        results.pose_landmarks,
        POSE_CONNECTIONS,
        DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
        DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2),
    )

    draw_landmarks(
        image,
        results.left_hand_landmarks,
        HAND_CONNECTIONS,
        DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
        DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2),
    )

    draw_landmarks(
        image,
        results.right_hand_landmarks,
        HAND_CONNECTIONS,
        DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
        DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
    )


def save_frames(frames, output_folder):
    for num_frame, frame in enumerate(frames):
        frame_path = os.path.join(output_folder, f"{num_frame + 1}.jpg")
        cv2.imwrite(frame_path, cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA))


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten(
    ) if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten(
    ) if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten(
    ) if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten(
    ) if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])


def get_keypoints(model, path):
    kp_seq = np.array([])
    for img_name in os.listdir(path):
        img_path = os.path.join(path, img_name)
        frame = cv2.imread(img_path)
        _, results = mediapipe_detection(frame, model)
        kp_frame = extract_keypoints(results)
        kp_seq = np.concatenate([kp_seq, [kp_frame]]
                                if kp_seq.size > 0 else [[kp_frame]])
    return kp_seq


def insert_keypoints_sequence(df, n_sample: int, kp_seq):
    for frame, keypoints in enumerate(kp_seq):
        data = {'sample': n_sample, 'frame': frame +
                1, 'keypoints': [keypoints]}
        df_keypoints = pd.DataFrame(data)
        df = pd.concat([df, df_keypoints])
    return df


def get_sequences_and_labels(actions, data_path):
    sequences, labels = [], []
    for label, action in enumerate(actions):
        hdf_path = os.path.join(data_path, f"{action}.h5")
        data = pd.read_hdf(hdf_path, key='data')

        for _, data_filtered in data.groupby('sample'):
            sequences.append([fila['keypoints']
                             for _, fila in data_filtered.iterrows()])
            labels.append(label)
    return sequences, labels


def format_sentences(sent, sentence, repe_sent):
    if len(sentence) > 1:
        if sent in sentence[1]:
            repe_sent += 1
            sentence.pop(0)
            sentence[0] = f"{sent} (x{repe_sent})"
        else:
            repe_sent = 1
    return sentence, repe_sent
