from __future__ import print_function
import tensorflow as tf
import numpy as np
import datetime
import cv2
import os
import time
import argparse

def get_labels(retrained_labels_path):
	"""Get a list of labels so we can see if what class it is."""
	with open(retrained_labels_path, 'r') as fin:
		labels = [line.rstrip('\n') for line in fin]
	return labels

def capture_images(labels, retrained_graph_path):
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

	# Unpersists graph from file
	with tf.gfile.FastGFile(retrained_graph_path, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='')

	with tf.Session() as sess:
		softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

		while(True):
			# Capture frame-by-frame
			read_correctly, frame = camera.read()

			if read_correctly:
				# Make the prediction. Big thanks to this SO answer:
				# http://stackoverflow.com/questions/34484148/feeding-image-data-in-tensorflow-for-transfer-learning
				predictions = sess.run(softmax_tensor, { 'DecodeJpeg:0': frame })
				prediction = predictions[0]

				# Get the highest confidence category.
				prediction = prediction.tolist()
				max_value = max(prediction)
				max_index = prediction.index(max_value)
				predicted_label = labels[max_index]

				print("%s (%.2f%%)" % (predicted_label, max_value * 100))

				# Display the resulting frame
				cv2.imshow('gilada', frame)

				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

	# When everything done, release the capture
	camera.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--retrained_labels',
      type=str,
      default='/tmp/output_labels.txt',
      help="""\
      Where to find the output_labels of the retrain.py script.\
      """
  )
  parser.add_argument(
      '--retrained_graph',
      type=str,
      default='/tmp/output_graph.pb',
      help="""\
      Where to find the retrained graph model
	  (output_graph of retrain.py).\
      """)
  FLAGS, unparsed = parser.parse_known_args()
  capture_images(get_labels(FLAGS.retrained_labels), FLAGS.retrained_graph)
