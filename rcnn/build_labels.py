"""
Given a folder of images and commercial start/end times, build our features
for training.
Dumpea al archivo labeled-frames-[batch].pkl el array de listas (imagen, clase). Para esto levanta de la carpeta
de 'images' todas las fotos del 'batch' querido identificado por su subcarpeta. batch -> video.
Y para saber la clase, compara el timestamp con los guardados en el archivo classes.py
"""
import pickle
import argparse
import os
import glob
from shutil import copyfile
from utils import get_direct_subdirs_in, create_dir_if_not_exists, check_expected_batches

def label_frames(video_dir, batch, classes, labels_dir, copydir=None):
    """Label our frames."""
    # Get all our images.
    images = sorted(glob.glob(os.path.join(video_dir, str(batch), "*")))
    num_images = len(images)

    print("Labelling %d frames for '%s' video." % (num_images, batch))

    # Loop through our images and set our labels.
    labeled_images = []
    num_commercials = 0
    classes_counter = {}
    for image in images:
        # Get the timestamp.
        filename = os.path.basename(image)
        timestamp = os.path.splitext(filename)[0]

        # What is it?
        label = get_label(timestamp, classes)

        # Save it.
        labeled_images.append([timestamp, label])

        # Copy it.
        if copydir:
            copyfile(image, os.path.join(copydir, label, batch, filename))

        # Info.
        classes_counter[label] = classes_counter.get(label, 0) + 1

    print("Done labelling.")
    for klass, count in classes_counter.items():
        print("Found %d frames of class %s." % (count, klass))

    path = os.path.join(labels_dir, f"labeled-frames-{batch}.pkl")
    with open(path, 'wb') as fout:
        pickle.dump(labeled_images, fout)

    return labeled_images

def get_label(timestamp, classes):
    """Given a timestamp and the class list, return to which class the frame
    belongs to. If not, return label."""
    for klass, predictions in classes.items():
        for time_range in predictions:
            if time_range['start'] <= timestamp <= time_range['end']:
                return klass
    return None # This is not good, but should not happen. We should think of a better return value here nonetheless.

def create_necessary_dirs(FLAGS, batches, class_per_frame):
    create_dir_if_not_exists(FLAGS.output_labels_dir)
    if FLAGS.copy_dir:
        create_dir_if_not_exists(FLAGS.copy_dir)
        classes_per_video = [class_per_frame[video].keys() for video in batches]
        for i in range(len(classes_per_video)):
            for klass in classes_per_video[i]:
                class_path = os.path.join(FLAGS.copy_dir, klass)
                video_path = os.path.join(class_path, batches[i])
                create_dir_if_not_exists(class_path)
                create_dir_if_not_exists(video_path)


def check_expected_dirs_and_files(FLAGS):
    if not os.path.exists(FLAGS.videos_dir):
        print("Videos directory '" + FLAGS.videos_dir + "' not found.")
        return False
    classes_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), FLAGS.classes_file + ".py")
    if not os.path.exists(classes_path):
        print("Classes file '" + classes_path + "' not found.")
        return False
    return True

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

    class_per_frame = getattr(__import__(FLAGS.classes_file, fromlist=[FLAGS.classes_dict]), FLAGS.classes_dict)

    okay = check_expected_dirs_and_files(FLAGS)
    if okay:
        batches = FLAGS.videos if FLAGS.videos else get_direct_subdirs_in(FLAGS.videos_dir)
        okay = check_expected_batches(FLAGS.videos_dir, batches)
        if okay:
            create_necessary_dirs(FLAGS, batches, class_per_frame)
            print(f"Processing videos: {batches}")
            for batch in batches:
                label_frames(FLAGS.videos_dir, batch, class_per_frame[batch], FLAGS.output_labels_dir, copydir=FLAGS.copy_dir)
