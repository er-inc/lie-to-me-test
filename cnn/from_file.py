from __future__ import print_function
import tensorflow as tf
import numpy as np
import datetime
import cv2
import os
import time

def get_labels():
	"""Get a list of labels so we can see if it's an ad or not."""
	with open('retrained_labels.txt', 'r') as fin:
		labels = [line.rstrip('\n') for line in fin]
	return labels

def capture_images(labels, source):
	print(source)
	frames = []

	# Unpersists graph from file
	with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='')

	with tf.Session() as sess:
		softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

		for base_dir, dirs, files in os.walk(source):
			print(base_dir, dirs, files)
			for file in files:
				frame = cv2.imread(os.path.join(base_dir, file))


				# Make the prediction. Big thanks to this SO answer:
				# http://stackoverflow.com/questions/34484148/feeding-image-data-in-tensorflow-for-transfer-learning
				predictions = sess.run(softmax_tensor, { 'DecodeJpeg:0': frame })
				prediction = predictions[0]

				# Get the highest confidence category.
				prediction = prediction.tolist()
				max_value = max(prediction)
				max_index = prediction.index(max_value)
				predicted_label = labels[max_index]

				print("Imagen: %s, prediccion: %s (%.2f%%)" % (file, predicted_label, max_value * 100))

current_path = os.getcwd()
capture_images(get_labels(), os.path.join(current_path, "photos"))
