"""
Go through all of our images and save out the pool layer
representation of our images. This is not a prediction, but rather the
convolutional representation of features that we can then pass to an
RNN. The idea is that later we'll add an RNN layer directly onto
the CNN. This gives us a way to test if that's a good strategy
before putting in the work required to do so.
"""
import tensorflow as tf, sys
import pickle
import sys
import os
import argparse
from tqdm import tqdm
from utils import get_direct_subdirs_in, create_dir_if_not_exists

def predict_on_frames(cnn_graph, frames, videos_dir, batch):
    # Unpersists graph from file
    with tf.gfile.FastGFile(cnn_graph, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        pool_tensor = sess.graph.get_tensor_by_name('pool_3:0')

        # Moving this into the session to make it faster.
        cnn_features = []
        video_path = os.path.join(FLAGS.videos_dir, batch)
        pbar = tqdm(total=len(frames))
        for i, frame in enumerate(frames):
            filename = frame[0]
            label = frame[1]

            # For some reason, we have a tar reference in our pickled file.
            if 'tar' in filename:
                continue

            # Get the image path.
            image = os.path.join(video_path, filename + '.jpg')

            # Read in the image_data
            image_data = tf.gfile.FastGFile(image, 'rb').read()

            try:
                cnn_representation = sess.run(pool_tensor,
                     {'DecodeJpeg/contents:0': image_data})
            except KeyboardInterrupt:
                print("You quit with ctrl+c")
                sys.exit()
            except:
                print("Error making prediction, continuing.")
                continue

            # Save it out.
            frame_row = [cnn_representation, label]
            cnn_features.append(frame_row)

            if i > 0 and i % 10 == 0:
                pbar.update(10)

        pbar.close()

        return cnn_features

def main(batches, videos_dir, frames_labels_dir, predictions_dir, cnn_graph):
    for batch in batches:
        print("Doing batch %s" % batch)
        path = os.path.join(frames_labels_dir, f"labeled-frames-{batch}.pkl")
        with open(path, 'rb') as fin:
            frames = pickle.load(fin)

        # Build the convoluted features for this batch.
        cnn_features = predict_on_frames(cnn_graph, frames, videos_dir, batch)

        # Save it.
        path = os.path.join(predictions_dir, f"cnn-features-frames-{batch}.pkl")
        with open(path, 'wb') as fout:
            pickle.dump(cnn_features, fout)

    print("Done.")

def create_necessary_dirs(FLAGS):
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
            create_necessary_dirs(FLAGS)
            print(f"Processing videos: {batches}")
            main(batches, FLAGS.videos_dir, FLAGS.frames_labels_dir, FLAGS.predictions_dir, FLAGS.cnn_graph)
