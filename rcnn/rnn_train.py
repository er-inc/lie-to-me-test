"""
Given a saved output of predictions or pooled features from our CNN,
train an RNN (LSTM) to examine temporal dependencies.
"""
from rnn_utils import get_network, get_network_deep, get_network_wide, get_data, get_classes
import tflearn

def main(filename, frames, batch_size, num_classes, input_length):
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
    model.save('checkpoints/rnn.tflearn')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--videos_dir',
        type=str,
        default='/tmp/videos',
        help="""\
        Where to find the recorded videos.\
        """
    )
    parser.add_argument(
		'--classes_file',
		type=str,
		default='classes',
		help="""\
		Name of the file (without extension) where the classes
        for each video are specified.
        This file must be in the same folder as this file,
        and it must define a dictionary with the classes
        in the correct format (check README).\
		"""
	)
    parser.add_argument(
		'--classes_dict',
		type=str,
		default='classes',
		help="""\
		Name of the dictionary that contains the
        classes for each video frame.\
		"""
	)
    parser.add_argument(
        '--output_labels_dir',
        type=str,
        default='/tmp/output_labels',
        help="""\
        Where to store the results, which is
        the label/class each frame of each video has,
        based on the classes file.\
        """
    )
    parser.add_argument(
        '--copy_dir',
        type=str,
        default=None,
        help="""\
        Where to store the video frames
        in relation to its label/class.\
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
    
    batches = ['fede_01_h', 'fede_02_c', 'dani_01_h', 'dani_02_c']
    pool = False
    if pool:
        filename = 'data/cnn-features-frames-1.pkl'
        input_length = 2048
    else:
        filename = 'data/predicted-frames-1.pkl'
        input_length = 2
    frames = 40
    batch_size = 32

    main(filename, frames, batch_size, len(get_classes()), input_length)
