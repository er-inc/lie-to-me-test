from __future__ import print_function
import os
import argparse
import datetime
import numpy as np
import cv2

from utils import convert_path_to_windows_format

def capture_images(save_folder):
	"""Stream images off the camera and save them."""
	camera = cv2.VideoCapture(0)

	if not camera.isOpened():
		print("Hubo un error y no se pudo iniciar la camara de captura.")
		return
	print("La resolucion es de {}x{}".format(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
	print("El frame count es de {}".format(camera.get(cv2.CAP_PROP_FPS)))
	print()
	print("Se pudo cambiar el width a 640: {}".format(camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)))
	print("Se pudo cambiar el height a 480: {}".format(camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)))
	print()
	print("La resolucion es de {}x{}".format(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
	print("Se pudo cambiar el frame count a 10: {}".format(camera.set(cv2.CAP_PROP_FPS, 10)))
	print("El frame count es de {}".format(camera.get(cv2.CAP_PROP_FPS)))

	count = 0

	while(True):
		# Capture frame-by-frame
		read_correctly, frame = camera.read()

		if read_correctly:
			# Save frame to file

			# Windows doesn't accept ":" in file name
			# and cv2.imwrite will silently fail
			timestamp = str(datetime.datetime.now()).replace(":", "-")

			img_path = os.path.join(save_folder, "{}.jpg".format(timestamp))
			cv2.imwrite(img_path, frame)
			print("pathhh: ", img_path)
			# Display the resulting frame
			cv2.imshow('Video', frame)
		else:
			print("Couldn't read image from cv2 correctly.")

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		count += 1

	# When everything done, release the capture
	camera.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--video_dir',
      type=str,
      default='/tmp/video',
      help="""\
      Path to store recorded images.\
      """
  )
  FLAGS, unparsed = parser.parse_known_args()
  if not os.path.exists(FLAGS.video_dir):
    os.makedirs(FLAGS.video_dir)
  capture_images(FLAGS.video_dir)
