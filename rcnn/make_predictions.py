"""
Classify all the images in a holdout set.
"""
import pickle
import sys
import os
import tensorflow as tf
from tqdm import tqdm
from utils import get_direct_subdirs_in, create_dir_if_not_exists

def get_labels(labels_file):
    """Return a list of our trained labels so we can
    test our training accuracy. The file is in the
    format of one label per line, in the same order
    as the predictions are made. The order can change
    between training runs."""
    with open(labels_file, 'r') as fin:
        labels = [line.rstrip('\n') for line in fin]
    return labels

def predict_on_frames(cnn_graph, frames, videos_dir, batch):
    """Given a list of frames, predict all their classes."""
    # Unpersists graph from file
    with tf.gfile.FastGFile(cnn_graph, 'rb') as fin:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(fin.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        frame_predictions = []
        video_path = os.path.join(FLAGS.videos_dir, batch)
        pbar = tqdm(total=len(frames))
        for i, frame in enumerate(frames):
            filename = frame[0]
            label = frame[1]

            # Get the image path.
            image = os.path.join(video_path, filename + '.jpg')

            # Read in the image_data
            image_data = tf.gfile.FastGFile(image, 'rb').read()

            try:
                predictions = sess.run(
                    softmax_tensor,
                    {'DecodeJpeg/contents:0': image_data}
                )
                prediction = predictions[0]
            except KeyboardInterrupt:
                print("You quit with ctrl+c")
                sys.exit()
            except:
                print("Error making prediction, continuing.")
                continue

            # Save the probability that it's each of our classes.
            frame_predictions.append([prediction, label])

            if i > 0 and i % 10 == 0:
                pbar.update(10)

        pbar.close()

        return frame_predictions

def get_accuracy(predictions, labels):
    """After predicting on each batch, check that batch's
    accuracy to make sure things are good to go. This is
    a simple accuracy metric, and so doesn't take confidence
    into account, which would be a better metric to use to
    compare changes in the model."""
    correct = 0
    for frame in predictions:
        # Get the highest confidence class.
        this_prediction = frame[0].tolist()
        this_label = frame[1]

        max_value = max(this_prediction)
        max_index = this_prediction.index(max_value)
        predicted_label = labels[max_index]

        # Now see if it matches.
        if predicted_label == this_label:
            correct += 1

    accuracy = correct / len(predictions)
    return accuracy

def main(batches, videos_dir, cnn_labels, frames_labels_dir, predictions_dir, cnn_graph):
    labels = get_labels(cnn_labels)

    for batch in batches:
        print("Doing batch %s" % batch)

        path = os.path.join(frames_labels_dir, f"labeled-frames-{batch}.pkl")
        with open(path, 'rb') as fin:
            frames = pickle.load(fin)

        # Predict on this batch and get the accuracy.
        predictions = predict_on_frames(cnn_graph, frames, videos_dir, batch)
        accuracy = get_accuracy(predictions, labels)
        print("Batch accuracy: %.5f" % accuracy)

        # Save it.
        path = os.path.join(predictions_dir, f"predicted-frames-{batch}.pkl")
        with open(path', 'wb') as fout:
            pickle.dump(predictions, fout)

    print("Done.")

def create_necessary_dirs(FLAGS, batches):
    create_dir_if_not_exists(FLAGS.predictions_dir)


def check_expected_dirs_and_files(FLAGS, batches):
    if not os.path.exists(FLAGS.videos_dir):
        print("Videos directory '" + FLAGS.videos_dir + "' not found.")
        return False
    for video in batches:
        path = os.path.join(FLAGS.videos_dir, video)
        if not os.path.exists(path):
            print("Video directory '" + path + "' not found.")
            return False
    if not os.path.exists(FLAGS.frames_labels_dir):
        print("Frames label directory '" + FLAGS.frames_labels_dir + "' not found.")
        return False
    for video in batches:
        path = os.path.join(FLAGS.frames_labels_dir, f"labeled-frames-{video}.pkl")
        if not os.path.exists(path):
            print("Frame label file '" + path + "' not found.")
            return False
    if not os.path.exists(FLAGS.cnn_labels):
        print("CNN labels file '" + FLAGS.cnn_labels + "' not found.")
        return False
    if not os.path.exists(FLAGS.cnn_graph):
        print("CNN graph file '" + FLAGS.cnn_graph + "' not found.")
        return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
		'--frames_labels_dir',
		type=str,
		default='/tmp/output_labels',
		help="""\
		Where to find the files for information on
        the label/class each frame of each video has.\
		"""
	)
    parser.add_argument(
		'--cnn_labels',
		type=str,
		default='/tmp/output_labels.txt',
		help="""\
		Where to find the CNN trained graph\'s labels.\
		"""
	)
    parser.add_argument(
        '--cnn_graph',
        type=str,
        default='/tmp/output_graph.pb',
        help='Where to find the CNN trained graph.'
    )
    parser.add_argument(
        '--predictions_dir',
        type=str,
        default='/tmp/data/predictions',
        help="""\
        Where to save the CNN predictions data.\
        """
    )
    parser.add_argument(
        '--videos_dir',
        type=str,
        default='/tmp/videos',
        help="""\
        Where to find the recorded videos.\
        """
    )
    parser.add_argument(
        '--videos',
        type=str,
        nargs='+',
        default=None,
        help="""\
        Specific videos to process.
        If none is provided, all in the video heriarchy
        will be processed.\
        """
    )
    FLAGS, unparsed = parser.parse_known_args()

    batches = FLAGS.videos if FLAGS.videos else get_direct_subdirs_in(FLAGS.videos_dir)
    okay = check_expected_dirs_and_files(FLAGS, batches)
    if okay:
        okay = check_expected_batches(FLAGS.videos_dir, batches)
        if okay:
            create_necessary_dirs(FLAGS, batches, class_per_frame)
            print(f"Processing videos: {batches}")
            main(batches, FLAGS.videos_dir, FLAGS.cnn_labels, FLAGS.frames_labels_dir, FLAGS.predictions_dir, FLAGS.cnn_graph)
