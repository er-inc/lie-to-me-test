from __future__ import print_function
import numpy as np
import datetime
import cv2
import os

def capture_images(save_folder):
	"""Stream images off the camera and save them."""
	camera = cv2.VideoCapture(0)
	
	if not camera.isOpened():
		print("Hubo un error y no se pudo iniciar la camara de captura.")
	print("La resolucion es de {}x{}".format(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
	print("El frame count es de {}".format(camera.get(cv2.CAP_PROP_FPS)))
	print()
	print("Se pudo cambiar el width a 320: {}".format(camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)))
	print("Se pudo cambiar el height a 240: {}".format(camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)))
	print("La resolucion es de {}x{}".format(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
	print("Se pudo cambiar el frame count a 10: {}".format(camera.set(cv2.CAP_PROP_FPS, 10)))
	
	count = 0
	
	while(True):
		# Capture frame-by-frame
		read_correctly, frame = camera.read()

		if read_correctly:
			# Save frame to file
			timestamp = datetime.datetime.now()
			img_path = os.path.join(save_folder, "{}.jpg".format(timestamp))
			cv2.imwrite(img_path, frame)

			# Display the resulting frame
			cv2.imshow('Video', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		count += 1

	# When everything done, release the capture
	camera.release()
	cv2.destroyAllWindows()

#script_path = os.path.dirname(os.path.abspath(__file__))
current_path = os.getcwd()
capture_images(os.path.join(current_path, "test"))

""" How to run
python retrain.py \
    --bottleneck_dir=/Users/festeban/Documents/tpprof/lie-to-me/cnn/bottleneck \
    --model_dir=/Users/festeban/Documents/tpprof/lie-to-me/cnn/inception \
    --output_graph=/Users/festeban/Documents/tpprof/lie-to-me/cnn/retrained_graph.pb \
    --output_labels=/Users/festeban/Documents/tpprof/lie-to-me/cnn/retrained_labels.txt \
    --image_dir /Users/festeban/Documents/tpprof/lie-to-me/cnn/photos
"""
