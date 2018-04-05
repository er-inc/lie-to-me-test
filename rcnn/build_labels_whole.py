"""
Given a folder of videos arranged in class´s folders, build our features
for training.
Dumpea al archivo labeled-frames-[batch].pkl el array de listas (imagen, clase). Para esto levanta de la carpeta
de 'images' todas las fotos del 'batch' querido identificado por su subcarpeta. batch -> video.
Y para saber la clase, compara el timestamp con los guardados en el archivo commercials.py
"""
import glob
import pickle
from shutil import copyfile
from commercials import commercials

def label_frames(batch, commercials, copyimage=True):
    """Label our frames."""
    # Get all our images.
    images = sorted(glob.glob('./images/' + str(batch) + '/*'))
    num_images = len(images)

    print("Labelling %d frames." % num_images)

    # Loop through our images and set our labels.
    labeled_images = []
    num_commercials = 0
    for image in images:
        # Get the timestamp.
        timestamp = image.replace('.jpg', '').split('/')[-1]

        # What is it?
        label = get_label(timestamp, commercials)

        # Save it.
        labeled_images.append([timestamp, label])

        # Copy it.
        if copyimage:
            copyfile(image, './images/classifications/' + label + '/' + timestamp + '.jpg')

        # Info.
        if label == 'ad':
            num_commercials += 1

    print("Done labelling, with %d commercial frames and %d not." %
          (num_commercials, num_images - num_commercials))

    with open('data/labeled-frames-' + str(batch) + '.pkl', 'wb') as fout:
        pickle.dump(labeled_images, fout)

    return labeled_images

def get_label(timestamp, commercials):
    """Given a timestamp and the commercials list, return if
    this frame is a commercial or not. If not, return label."""
    for com in commercials['commercials']:
        if com['start'] <= timestamp <= com['end']:
            return 'ad'
    return commercials['class']

if __name__ == '__main__':
    batches = ['1']
    for batch in batches:
        label_frames(batch, commercials[str(batch)], copyimage=False)
