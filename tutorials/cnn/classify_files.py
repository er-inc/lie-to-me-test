import tensorflow as tf
import numpy as np
import datetime
import cv2
import os
import time

import argparse
from utils import get_labels

def classify_images(labels, retrained_graph_path, source):
	frames = []

	# Unpersists graph from file
	with tf.gfile.FastGFile(retrained_graph_path, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='')

	with tf.Session() as sess:
		softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

		for base_dir, dirs, files in os.walk(source):
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

				print("Image: %s, prediction: %s (%.2f%%)" % (file, predicted_label, max_value * 100))


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
		"""
	)
	parser.add_argument(
		'--data',
		type=str,
		default='/tmp/data',
		help="""\
		Where to find the images to classify.
		All files inside the directory tree will be classified.\
		"""
	)
	FLAGS, unparsed = parser.parse_known_args()
	classify_images(get_labels(FLAGS.retrained_labels), FLAGS.retrained_graph, FLAGS.data)
