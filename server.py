from flask import Flask, request, jsonify
from azure.cognitiveservices.vision.face import FaceClient, models
from msrest.authentication import CognitiveServicesCredentials
from configs import FACE_API_URL, SUBSCRIPTION_KEY
import os
import logging

app = Flask(__name__)
log = logging.getLogger(__name__)
FACE_CLIENT = FaceClient(endpoint=FACE_API_URL, credentials=CognitiveServicesCredentials(SUBSCRIPTION_KEY))


@app.route('/best_image', methods=['POST'])
def get_best_image():
    """
    Recieves POST requests and returns the best image out of a list
    MUST give full file_paths
    :return dict: {best_image_name: azure metadata}
    """
    images_dict = {}
    for image_path in request.json.get('images', ''):
        log.info('getting azure image data')
        try:
            detection = FACE_CLIENT.face.detect_with_stream(open(image_path, 'r+b'))
        except models._models_py3.APIErrorException:
            continue
        images_dict[image_path] = get_largest_face_size(detection, os.stat(image_path).st_size)

    log.info('calculating best image')
    best_image = max(images_dict.keys(), key=(lambda key: images_dict[key][0]))
    return jsonify({best_image: images_dict[best_image][1].as_dict()}), 201


def get_largest_face_size(faces_json, full_image_size):
    log.info('getting largest face in image ')
    # list of tuples containing image quality and metadata per face in image
    all_faces = [(full_image_size - (face.face_rectangle.height * face.face_rectangle.width), face)
                 for face in faces_json]

    return max(all_faces, key=lambda key: key[0]) if all_faces else (0, {})


def main():
    app.run(port='8000')


if __name__ == '__main__':
    main()
