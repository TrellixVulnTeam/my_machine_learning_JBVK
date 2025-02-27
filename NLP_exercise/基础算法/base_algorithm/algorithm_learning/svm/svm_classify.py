# -*- coding: utf-8 -*-

import numpy

def load_dataSet(filename):
	data_matrix = []
	label_matrix = []
	file = open(filename)

	for line in file.readlines():
		line_array = line.strip().split('\t')
		data_matrix.append([float(line_array[0]), float(line_array[1])])
		label_matrix.append(float(line_array[2]))

	return data_matrix, label_matrix


# SMO算法随机选取拉格朗日乘子
# 参数：
	# i: 第 i 个乘子的下标
	# m: 乘子总数
def select_Jrand(i, m):
	j = i

	while(j == i):
		j = int(numpy.random.uniform(0, m))
	return j


# 调整大于 high 和小于 low 的乘子的值
# 每个乘子 alpha 的范围在 high 和 low 之间
def clip_alpha(alpha_J, high, low):
	if alpha_J > high:
		alpha_J = high
	if alpha_J < low:
		alpha_J = low
	return alpha_J



# 简化版的SMO
# 参数：
	# C: 常数
	# tolerance: 误差率
	# max_iter: 迭代次数
def simple_SMO(data_inputMatrix, class_label, C, tolerance, max_iter):
	data_matrix = numpy.mat(data_inputMatrix)
	label_matrix = numpy.mat(class_label).transpose()

	# 偏倚 b
	b = 0

	row, column = data_matrix.shape
	alphas = numpy.mat(numpy.zeros((row, 1)))
	iter = 0

	while (iter < max_iter):
		# 标志：记录 alpha 是否已经被优化
		alpha_pairs_changed = 0

		for i in range(row):
			# f_Xi 表示输入样本 Xi 的输出类别
			f_Xi = float(numpy.multiply(alphas, label_matrix).T * (data_matrix * data_matrix[i, :].T)) + b

			# error_Xi 表示样本 Xi 的误差
			error_Xi = f_Xi - float(label_matrix[i])

			if ((label_matrix[i] * error_Xi < -tolerance) and (alphas[i] < C)) or ((label_matrix[i] * error_Xi > tolerance) and (alphas[i] > 0)):
				# 随机选取第二个 alpha (乘子)
				j = select_Jrand(i, row)

				f_Xj = float(numpy.multiply(alphas, label_matrix).T * (data_matrix * data_matrix[j, :].T)) + b
				error_Xj = f_Xj - float(label_matrix[j])
				
				# 保存两个优化乘子的原始值
				alpha_Iold = alphas[i].copy()
				alpha_Jold = alphas[j].copy()
				
				# 当两个优化乘子所对应的标签异号, 分别更新上下界
				if (label_matrix[i] != label_matrix[j]):
					low = max(0, alphas[j] - alphas[i])
					high = min(C, C + alphas[j] - alphas[i])
				else:
					low = max(0, alphas[j] + alphas[i] - C)
					high = min(C, alphas[j] + alphas[i])

				if low == high:
					print "low == high"
					continue

				# Eta: alpha 的最优修改量
				Eta = 2.0 * data_matrix[i, :] * data_matrix[j, :].T - data_matrix[i, :] * data_matrix[i, :].T - data_matrix[j, :] * data_matrix[j, :].T

				if Eta >= 0:
					print "Eta >= 0"
					continue

				# 对其中一个 alphas[i] 进行修改， 修改量与 alphas[j] 相同，方向相反
				alphas[j] -= label_matrix[j] * (error_Xi - error_Xj) / Eta
				alphas[j] = clip_alpha(alphas[j], high, low)

				if (abs(alphas[j] - alpha_Jold) < 0.00001):
					print "j not moving enough"
					continue

				alphas[i] += label_matrix[j] * label_matrix[i] * (alpha_Jold - alphas[j])
				b1 = b - error_Xi - label_matrix[i] * (alphas[i] - alpha_Iold) * data_matrix[i, :] * data_matrix[i, :].T - label_matrix[j] * (alphas[j] - alpha_Jold) * data_matrix[i, :] * data_matrix[j, :].T

				b2 = b - error_Xj - label_matrix[i] * (alphas[i] - alpha_Iold) * data_matrix[i, :] * data_matrix[j, :].T - label_matrix[i] * (alphas[j] - alpha_Jold) * data_matrix[j, :] * data_matrix[j, :].T

				if (alphas[i] > 0) and (alphas[i] < C):
					b = b1

				elif (alphas[j] > 0) and (alphas[j] < C):
					b = b2

				else:
					b = (b1 + b2) / 2

				alpha_pairs_changed += 1

				print "iter: %d	i: %d, pairs changed: %d" %(iter, i, alpha_pairs_changed)

		if (alpha_pairs_changed == 0):
			iter += 1

		else:
			iter = 0

		print "iteration number: %d" %iter

	return b, alphas


# 创建数据结构
class optimiza_struct:
	def __init__(self, data_inputMatrix, class_label, C, tolerance):
		self.data_matrix = data_inputMatrix
		self.label_matrix = class_label
		self.C = C
		self.tolerance = tolerance

		self.row = data_inputMatrix.shape[0]
		self.alphas = numpy.mat(numpy.zeros((self.row, 1)))
		self.b = 0
		self.eCache = numpy.mat(numpy.zeros((self.row, 2)))


# 计算误差
# 参数
	# op_struct: optimize_struct 的一个实例
	# k: 样本 k 的误差
def calcEk(op_struct, k):
	f_Xk = float(numpy.multiply(op_struct.alphas, op_struct.label_matrix).T * (op_struct.data_matrix * op_struct.data_struct[k, :].T)) + op_struct.b

	error_k = f_Xk - float(op_struct.label_matrix[k])

	return error


# 采用启发式算法选取拉格朗日乘子
def select_J(i, op_struct, error_i):
	max_k = -1
	max_deltaError = 0
	error_j = 0

	op_struct.eCache[i] = [i, error_i]
	valid_eCacheList = numpy.nonzero(op_struct.eCache[:, 0].A)[0]

	if (len(valid_eCacheList)) > 1:
		for k in valid_eCacheList:
			if k == i:
				continue

			error_k = calcEk(op_struct, k)
			delta_error = abs(error_i - error_k)

			if delta_error > max_deltaError:
				max_k = k
				max_deltaError = delta_error
				error_j = error_k
		return max_k, error_j

	else:
		i = select_Jrand(i, op_struct.row)
		error_j = calcEk(op_struct, j)
	return j, error_j


# 误差更新
def updateEk(op_struct, k):
	error_k = calcEk(op_struct, k)
	op_struct.eCache[k] = [1, error_k]



# 根据求得的 alphas 来求解权重 weights
def calc_weights(alphas, data_array, class_label):
	data_matrix = numpy.mat(data_array)
	label_array = numpy.mat(class_label).transpose()

	row, column = data_matrix.shape
	weights = numpy.zeros((row, 2))

	for i in range(row):
		weights += numpy.multiply(alphas[i] * label_array[i], data_matrix[i, :])
		# weights += alphas[i] * label_array[i] * data_matrix[i, :]
	return weights
