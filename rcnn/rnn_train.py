"""
Given a saved output of predictions or pooled features from our CNN,
train an RNN (LSTM) to examine temporal dependencies.
"""
from rnn_utils import get_network, get_network_deep, get_network_wide, get_data, get_classes
import tflearn
import argparse
import os
import re
from tensorflow.python.platform import gfile
from tensorflow import reset_default_graph
from utils import get_direct_subdirs_in, create_dir_if_not_exists

def main(filename, frames, batch_size, num_classes, input_length, output_model):
    """From the blog post linked above."""
    # Get our data.
    X_train, X_test, y_train, y_test = get_data(filename, frames, num_classes, input_length)

    # Get sizes.
    num_classes = len(y_train[0])

    # Get our network.
    net = get_network_wide(frames, input_length, num_classes)

    # Train the model.
    model = tflearn.DNN(net, tensorboard_verbose=0)
    model.fit(X_train, y_train, validation_set=(X_test, y_test),
              show_metric=True, batch_size=batch_size, snapshot_step=100,
              n_epoch=4)

    # Save it.
    model.save(output_model)

def create_necessary_dirs(FLAGS, batches):
    create_dir_if_not_exists(FLAGS.predictions_dir)

def check_expected_dirs_and_files(FLAGS, batches):
    if not os.path.exists(FLAGS.predictions_dir):
        print("Predictions directory '" + FLAGS.predictions_dir + "' not found.")
        return False
    for video in batches:
        filename = f"cnn-features-frames-{video}.pkl" if FLAGS.pool else f"predicted-frames-{video}.pkl"
        path = os.path.join(FLAGS.predictions_dir, filename)
        if not os.path.exists(path):
            print("Predictions file '" + path + "' not found.")
            return False
    return True

def get_existing_videos_from_predictions(predictions_dir, filename_format):
    regex = filename_format.format("*")
    files = gfile.Glob(os.path.join(predictions_dir, regex))
    regex = os.path.join(predictions_dir, filename_format.format("(.*)"))
    p = re.compile(regex)
    return [p.search(filename).group(1) for filename in files]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-pool',
        action='store_true'
    )
    parser.add_argument(
        '--videos',
        type=str,
        nargs='+',
        help="""\
        Specific videos to process.\
        """
    )
    parser.add_argument(
        '--predictions_dir',
        type=str,
        default='/tmp/data/predictions',
        help="""\
        Where to find the CNN prediction files.\
        """
    )
    parser.add_argument(
        '--before_frames',
        type=int,
        default=40,
        help="""\
        How many before frames should be considered
        to evaluate a frame.\
        """
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=32,
        help="""\
        Batch size used to train RNN.\
        """
    )
    parser.add_argument(
        '--output_model',
        type=str,
        default='tmp/checkpoints/rnn.tflearn',
        help="""\
        Where to save the trained model.
        It's a .tflearn file.\
        """
    )
    FLAGS, unparsed = parser.parse_known_args()

    if FLAGS.pool:
        filename = 'cnn-features-frames-{}.pkl'
        input_length = 2048
    else:
        filename = 'predicted-frames-{}.pkl'
        input_length = 2

    batches = FLAGS.videos if FLAGS.videos else get_existing_videos_from_predictions(FLAGS.predictions_dir, filename)
    okay = check_expected_dirs_and_files(FLAGS, batches)
    if okay:
        create_necessary_dirs(FLAGS, batches)
        print(f"Processing videos: {batches}")
        for video in batches:
            file = os.path.join(FLAGS.predictions_dir, filename.format(video))
            print("Doing batch %s" % video)
            reset_default_graph()
            main(file, FLAGS.before_frames, FLAGS.batch_size, len(get_classes()), input_length, FLAGS.output_model)
