# lie-to-me-test
Hay que instalar:
- Python _<insert link>_
- Tensorflow _<insert link>_
- OpenCV _<insert link>_

## MNIST Tutorial
Para correr los ejemplos del [tutorial de MNIST de Tensorflow](https://www.tensorflow.org/tutorials/layers):
```
python ./mnist_tutorial/mnist_beginner.py
python ./mnist_tutorial/mnist_deep.py
```

## CNN Inception
Para reentrenar la última capa de la red Inception con tus propias fotos:

1. Poné tus fotos en la carpeta `photos`.
Tenés que crear dentro de `photos` una carpeta por cada categoría que quieras tener y dentro de esas carpetas las fotos.

2. Corré el comando:
```
python ./cnn/retrain.py --bottleneck_dir=./cnn/bottleneck --model_dir=./cnn/inception --output_graph=./cnn/retrained_graph.pb --output_labels=./cnn/retrained_labels.txt --image_dir ./cnn/photos
```
