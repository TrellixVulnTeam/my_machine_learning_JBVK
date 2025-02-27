# -*- coding: utf-8 -*-

from numpy import *

def load_dataSet(filename, delim = '\t'):
	file = open(filename)
	string_array = [line.strip().split(delim) for line in file.readlines()]
	data_array = [map(float, line) for line in string_array]
	return mat(data_array)



# PCA 变换步骤：
	# 1. 将 m * n 的训练图像重新排列为 m * n 维的列向量。计算均值向量，并利用均值向量将所有样本中心化
	# 2. 利用中心化后的样本向量，根据式 ST = E{(xi-u)*(xi-u)T} = X'X'T 其中X’ = [x1-μ, x2-μ,...., xN-μ]，计算协方差矩阵；并对其进行特征值分解，并将其特征向量按照其对应的特征值大小进行降序排列
	# 3. 选择第二步所得的 K <= N - 1 个最大特征值所对应的特征向量组成的投影矩阵 A，将每幅已中心化的训练图像(x1-μ, x2-μ,...., xN-μ)，向矩阵A投影，得到每幅训练图像的降维表示为(y1-μ, y2-μ,...., yN)
	# 4. 对测试图像中心化，并投影到矩阵 A，则可得到测试图像的降维表示

def pca(data_array, topN_feature = 9999999):
	mean_value = mean(data_array, axis = 0)
	mean_removed = data_array - mean_value
	cov_matrix = cov(mean_removed, rowvar = 0)

	# 求解特征值和特征向量
	eigen_value, eigen_vector = linalg.eig(mat(cov_matrix))

	eigenValue_index = argsort(eigen_value)
	eigenValue_index = eigenValue_index[: -(topN_feature + 1): -1]
	red_eigenVector = eigen_vector[:, eigenValue_index]
	
	# 将数据转换到新空间
	newSpace_matrix = mean_removed * red_eigenVector
	reconstruct_matrix = (newSpace_matrix * red_eigenVector.T) + mean_value

	return newSpace_matrix, reconstruct_matrix



def process_nanValue():
	data_matrix = load_dataSet('secom.data', ' ')
	num_feature = shape(data_matrix)[1]
	for i in range(num_feature):
		mean_value = mean(data_matrix[nonzero(~isnan(data_matrix[:, i].A))[0], i])
		
		# 使用均值代替 nan
		data_matrix[nonzero(isnan(data_matrix[:, i]))[0], i] = mean_value
	return data_matrix



