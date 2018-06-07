# lie-to-me-test
Hay que instalar:
- [Python 3](https://algoritmos7540-rw.tk/python)
- [Tensorflow](https://www.tensorflow.org/install)
- OpenCV 3: [Windows](https://pypi.python.org/pypi/opencv-python) o [Mac, Linux y RaspberryPi](https://www.pyimagesearch.com/opencv-tutorials-resources-guides/)
- [Pip](https://pip.pypa.io/en/stable/installing/)
- Install python dependencies: `pip3 install -r requirements.txt`
Si tenés una computadora con GPU, primero modificá `requirements.txt`
para instalar `tensorflow-gpu` en vez de `tensorflow`.

## MNIST Tutorial
Para correr los ejemplos del [tutorial de MNIST de Tensorflow](https://www.tensorflow.org/tutorials/layers):
```
python3 ./mnist_tutorial/mnist_beginner.py
python3 ./mnist_tutorial/mnist_deep.py
```

## Grabar video

### Grabar como secuencia de imágenes
1. Correr `python capture_frames.py --video_dir ./<path_a_carpeta>`.
Las imágenes van a tener el formato `YYYY-MM-dd hh:mm:ss.ms`

## Descargar CNN Inception
Todas las operaciones que hagamos van a usar la red Inception V3 por default, que es uno de los [modelos preentrenados](https://www.tensorflow.org/tutorials/image_recognition) con muchas imágenes.
Y vamos a reentrenar sólo las últimas capas con lo que nos interesa para nuestro problema.

1. Correr el comando:
```
python3 ./cnn/download_model.py
	--model_dir=./cnn/inception
```

De todas formas, los pasos que lo necesiten se encargarán de esto.


## CNN

### Reentrenamiento
Para reentrenar la última capa de la red Inception con tus propias fotos:

1. Poné tus fotos en la carpeta `cnn/photos`.
Tenés que crear dentro de `cnn/photos` una carpeta por cada categoría que quieras tener y dentro de esas carpetas las fotos.

2. Corré el comando:
```
python3 ./cnn/retrain.py
	--bottleneck_dir=./cnn/bottleneck
	--model_dir=./cnn/inception
	--output_graph=./cnn/retrained_graph.pb
	--output_labels=./cnn/retrained_labels.txt
	--image_dir ./cnn/photos
```

### Clasificación de imágenes real time
Clasifica los frames.

1. Reentrená la red
2. Corré
```
python3 ./cnn/classify_real_time.py
	--retrained_labels ./cnn/retrained_labels.txt
	--retrained_graph ./cnn/retrained_graph.pb
	--data ./cnn/photos
```

### Clasificación de imágenes
Clasifica todas las imágenes en una carpeta.

1. Reentrená la red
2. Corré:
```
python3 ./cnn/classify_files.py
	--retrained_labels ./cnn/retrained_labels.txt
	--retrained_graph ./cnn/retrained_graph.pb
```


## RCNN

### Reentrenamiento

#### Cada video es de una clase en particular
Para casos donde todo el video se clasifica de una clase y no pedazos de él, hay que seguir el [siguiente formato](#especificar-que-momentos-del-video-son-de-una-clase), especificando toda la duración de una sola clase.

#### Especificar qué momentos del video son de una clase
Para casos donde el video tiene partes de distintas clases.
Acá importa para la clasificación cómo van apareciendo las clases y sus tiempos.

1. Tenés que ubicar los videos en la carpeta `rcnn/videos` y crear un archivo llamado `rcnn/classes.py` que defina el diccionario `class_per_frame` con el siguiente formato:
```
"nombre_del_video": {
	"clase1": [
		{ "start":  "YYYY-MM-dd hh-mm-ss.ms",
		  "end": 	"YYYY-MM-dd hh-mm-ss.ms" },
		{ "start":  "YYYY-MM-dd hh-mm-ss.ms",
		  "end": 	"YYYY-MM-dd hh-mm-ss.ms" }
	],
	"clase2": [
		{ "start":  "YYYY-MM-dd hh-mm-ss.ms",
		  "end": 	"YYYY-MM-dd hh-mm-ss.ms" }
	]
}
```
Nota: es de suma importancia los rangos de los timestamps. Pues si no se tiene en cuenta algun frame el mismo va a ser clasificado con clase None.

2. Moverse a la carpeta `rcnn`.
3. Reentrená la CNN usando el retrain dentro de rcnn. Corré el comando:
```
python3 ./retrain_cnn.py --bottleneck_dir=./cnn/bottleneck --model_dir=./cnn/inception --output_graph=./cnn/retrained_graph.pb --output_labels=./cnn/retrained_labels.txt --processed_video_dir ./videos
```
4. En el archivo `build_labels.py` , modificar los batches deseados (los videos que se quieren labelear).
5. Correr el comando `python build_labels.py`.
6. Modificar en el archivo `rnn_train.py` los batches que se quieren usar para entrenar y si se predijo sin o con pool.
El primer camino (sin pool) sirve para predecir los datos del training usando sólo el resultado de los frames anteriores.
El segundo predice usando los datos del frame anterior de la última capa previa a la predicción, dándole más información.
7. Correr el comando `python rnn_train.py`.


### Clasificación de un video real time
Clasifica cada 4 segundos (40 frames), el frame que se está viendo.

1. Reentrená la red
2.

### Clasificación de un video
Clasifica los distintos frames del video.

1. Reentrená la red
2. En el archivo `make_predictions.py` o `make_predictions_pool.py` modificar los batches que se quieren predecir.
3. Correr el comando `python make_predictions.py` o `python make_predictions_pool.py` correspondientemente, según lo elegido en el paso 5 del reentrnamiento.
