import subprocess
import json
import server
from threading import Thread


def test_best_image():
    t = Thread(target=server.main)
    t.start()
    curl_response = subprocess.getoutput('curl --header "Content-Type: application/json" --request POST '
        '--data \'{"images":["testing/detection-1-thumbnail.jpg", "testing/detection-2-thumbnail.jpg", '
        '"testing/detection-3-thumbnail.jpg", "testing/detection-4-thumbnail.jpg", '
        '"testing/detection-5-thumbnail.jpg"]}\' http://localhost:5000/best_image')
    assert "testing/detection-3-thumbnail.jpg" in json.loads(curl_response.splitlines()[-1]).keys()

test_best_image()