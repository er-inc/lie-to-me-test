"""
Run a holdout set of data through our trained RNN. Requires we first
run train_rnn.py and save the weights.
"""
from rnn_utils import get_network, get_network_deep, get_network_wide, get_data
import tflearn
from tensorflow import reset_default_graph

PREDICTIONS_FILE = "./rcnn/data/ccn_predictions/predicted-frames-fede_01_h.pkl"
RNN_MODEL = "./rcnn/data/rnn.tflearn"

def main(filename, frames, batch_size, num_classes, input_length):
    """From the blog post linked above."""
    # Get our data.
    X_train, _, y_train, _ = get_data(filename, frames, num_classes, input_length)

    # Get sizes.
    num_classes = len(y_train[0])

    # Get our network.
    net = get_network_wide(frames, input_length, num_classes)

    # Get our model.
    model = tflearn.DNN(net, tensorboard_verbose=0)
    model.load(RNN_MODEL)


    print(f"Y: {y_train}")

    # Evaluate.
    #res = model.evaluate(X_train, y_train)  #Evaluates model accuracy.
    res = model.predict(X_train)  #Predicts probabilities of each class
    print(f"RESULTADO: {res}")
    print(f"RESULTADO tipo: {type(res)}")
    print(f"RESULTADO shape: {res.shape}")

    res = model.predict_label(X_train) #Predicts bitmask of classed (1 if it is that class, 0 if not)
    print(f"RESULTADO LABEL: {res}")


if __name__ == '__main__':
    filename = PREDICTIONS_FILE
    input_length = 2
    # filename = 'data/cnn-features-frames-2.pkl'
    # input_length = 2048
    frames = 40
    batch_size = 32
    num_classes = 2

    reset_default_graph()
    main(filename, frames, batch_size, num_classes, input_length)
