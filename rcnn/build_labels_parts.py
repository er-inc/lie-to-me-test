"""
Given a folder of images and commercial start/end times, build our features
for training.
Dumpea al archivo labeled-frames-[batch].pkl el array de listas (imagen, clase). Para esto levanta de la carpeta
de 'images' todas las fotos del 'batch' querido identificado por su subcarpeta. batch -> video.
Y para saber la clase, compara el timestamp con los guardados en el archivo classes.py
"""
import glob
import pickle
from shutil import copyfile
from classes import classes

def label_frames(batch, classes, copyimage=True):
    """Label our frames."""
    # Get all our images.
    images = sorted(glob.glob('./images/' + str(batch) + '/*'))
    num_images = len(images)

    print("Labelling %d frames." % num_images)

    # Loop through our images and set our labels.
    labeled_images = []
    num_commercials = 0
    classes_counter = {}
    for image in images:
        # Get the timestamp.
        timestamp = image.replace('.jpg', '').split('/')[-1]

        # What is it?
        label = get_label(timestamp, classes)

        # Save it.
        labeled_images.append([timestamp, label])

        # Copy it.
        if copyimage:
            copyfile(image, './images/classifications/' + label + '/' + timestamp + '.jpg')

        # Info.
        classes_counter[label] += 1

    print("Done labelling.")
    for klass, count in classes_counter:
        print("Found %d frames of class %s" % (count, klass))

    with open('data/labeled-frames-' + str(batch) + '.pkl', 'wb') as fout:
        pickle.dump(labeled_images, fout)

    return labeled_images

def get_label(timestamp, classes):
    """Given a timestamp and the class list, return to which class the frame
    belongs to. If not, return label."""
    for klass, predictions in classes:
        for time_range in predictions:
            if time_range['start'] <= timestamp <= time_range['end']:
                return klass
    return None # This is not good, but should not happen. We should think of a better return value here nonetheless.

if __name__ == '__main__':
    batches = ['1']
    for batch in batches:
        label_frames(batch, classes[str(batch)], copyimage=False)
