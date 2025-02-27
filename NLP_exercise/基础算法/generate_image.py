# -*- coding: utf-8 -*-


import tensorflow as tf
import numpy as np
import cv2

inception_model = 'tensorflow_inception_graph.pb'

# load inception model
grahp = tf.Graph()
session = tf.InteracttiveSession(graph = graph)


X = tf.placeholder(np.float32, name = "input")

with tf.gfile.FastGFile(inception_model, 'rb') as f:
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(f.read())

imageNet_mean = 117.0
preprocessed = tf.expand_dims(X - imageNet_mean, 0)
tf.import_graph_def(graph_def, {'input': preprocessed})

layers = [op.name for op in graph.get_operations() if op.type == 'Conv2D' and 'import/' in op.name]
feature_nums = [int(graph.get_tensor_by_name(name + ':0').get_shape()[-1]) for name in layers]

print("layers: ", len(layers))			# 59
print("features: ", len(feature_nums))		# 7548


# deep dream
def deep_dream(obj, img_noise = np.random.uniform(size = (224, 224, 3)) + 100.0, iter_n = 10, step = 1.5, actave_n = 4, actave_scale = 1.4):
	score = tf.reduce_mean(obj)
	gradi = tf.gradients(score, X)[0]

	img = img_noise
	actaves = []
	
	def tffunc(*argtypes):
		placeholders = list(map(tf.placeholder, argtypes))
		
		def wrap(f):
			out = f(*placeholders)
			
			def wrapper(*args, **kw):
				return out.eval(dict(zip(placeholders, args)), session = kw.get('session'))
			return wrapper
		return wrap

	def resize(img, size):
		img = tf.expand_dims(img, 0)
		return tf.image.resize_bilinear(img, size)[0, :, :, :]

	resize = tffunc(np.float32, np.int32)(resize)

	for calc_grad_tiled(ima, t_grad, tile_size = 512):
		sz = tile_size
		h, w = img.shape[:2]
		sx, sy = np.random.randint(sz, size = 2)

		img_shift = np.roll(np.roll(img, sx, 1), sy, 0)
		grad = np.zeros_like(img)

		for y in range(0, max(h - sz // 2, sz), sz):
			for x in range(0, max(w - sz // 2), sz):
				sub = img_shift[y: y + sz, x: x + sz]
				g = session.run(t_grad, {X: sub})
				grad[y: y + sz, x: x + sz]

		return np.roll(np.roll(grad, -sx, 1), -sy, 0)

	

	for actave in range(actave_n):
		if actave > 0:
			hi = actaves[-actave]
			img = resize(img, hi.shape[: 2]) + hi

		for _ in range(iter_n):
			g = calc_grad_tiled(img, gradi)
			img += g * (step / (np.abs(g).mean() + 1e-7))

		# save the image
		output_file = 'output' + str(actave + 1) + '.jpg'
		cv2.imwrite(output_file, img)
		print(output_file)

# load the input image
input_img = cv2.imread('input.jpg')
input_img = np.float32(input_img)

# 选择层
layers = 'mixed4c'


deep_dream(tf.square(graph.get_tensor_by_name("import/%s:0" %layer)), input_img)
		


