# -*- coding: utf-8 -*-

from numpy import *
import operator
from os import listdir

def createDataSet():
	group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
	labels = ['A', 'A', 'B', 'B']

	return group, labels


def classify(inX, dataSet, labels, k):
	dataSet_Size = dataSet.shape[0]
	diff_mat = tile(inX, (dataSet_Size, 1)) - dataSet

	# 计算欧氏距离
	sq_diff_mat = diff_mat ** 2
	sq_distances = sq_diff_mat.sum(axis = 1)
	distances = sq_distances ** 0.5

	# 对距离进行升序排序，返回索引序列
	sort_dist_indicies = distances.argsort()
	class_count = {}

	for i in range(k):
		vote_label = labels[sort_dist_indicies[i]]
		class_count[vote_label] = class_count.get(vote_label, 0) + 1
	
	sorted_class_count = sorted(class_count.iteritems(), key = operator.itemgetter(1), reverse = True)
	return sorted_class_count[0][0]



def file2matrix(filename):
	file = open(filename)
	array_lines = file.readlines()
	number_of_lines = len(array_lines)

	return_matrix = zeros((number_of_lines, 3))
	class_label_vector = []
	index = 0
	
	for line in array_lines:
		line = line.strip()
		listFromLine = line.split('\t')

		return_matrix[index, :] = listFromLine[0:3]
		class_label_vector.append(int(listFromLine[-1]))
		index += 1
	return return_matrix, class_label_vector



# 维度特征归一化
def auto_norm(dataSet):
	# 选取每列中的最小值和最大值
	min_values = dataSet.min(0)
	max_values = dataSet.max(0)

	ranges = max_values - min_values
	norm_dataSet = zeros(shape(dataSet))

	length = dataSet.shape[0]
	norm_dataSet = dataSet - tile(min_values, (length, 1))
	norm_dataSet = norm_dataSet / tile(ranges, (length, 1))

	return norm_dataSet, ranges, min_values



# 取10%的数据作为测试数据
def dating_testClass():
	test_ratio = 0.1
	datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')

	norm_matrix, ranges, min_values = auto_norm(datingDataMat)
	length = norm_matrix.shape[0]
	number_test = int(test_ratio * length)
	error_count = 0.0

	for i in range(number_test):
		classifier_result = classify(norm_matrix[i, :], norm_matrix[number_test:length, :], datingLabels[number_test:length], 3)

		print "the classifier came back with: %d, the real answer is : %d" %(classifier_result, datingLabels[i])

		if (classifier_result != datingLabels[i]):
			error_count += 1.0
	
	print "the total error rato is: %f" %(error_count / float(number_test))



def classifyPerson():
	result_list = ['not at all', 'in small doses', 'in large doses']

	percentTats = float(raw_input("percentage of time spent playing video games: "))
	ffMiles = float(raw_input("frequent flier miles earned per year: "))
	iceCream = float(raw_input("liters of ice cream consumed per year:"))
	
	datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
	norm_matrix, ranges, min_values = auto_norm(datingDataMat)

	inArr = array([ffMiles, percentTats, iceCream])

	classifier_result = classify((inArr - min_values) / ranges, norm_matrix, datingLabels, 3)

	print "you will probablly like this person: ", result_list[classifier_result - 1]


# 将32 * 32的像素图像转化成为一个1 * 1024的向量
def image2Vector(filename):
	return_vector = zeros((1, 1024))
	file = open(filename)
	for i in range(32):
		line_str = file.readline()
		for j in range(32):
			return_vector[0, 32 * i + j] = int(line_str[j])
	return return_vector


def handwriting_classTest():
	handwriting_labels = []
	training_fileList = listdir('trainingDigits')

	length = len(training_fileList)
	trainingMat = zeros((length, 1024))

	for i in range(length):
		filename_str = training_fileList[i]
		file_str = filename_str.split('.')[0]
		class_numberStr = int(file_str.split('_')[0])

		handwriting_labels.append(class_numberStr)
		trainingMat[i, :] = image2Vector('trainingDigits/%s' %filename_str)
	
	test_fileList = listdir('testDigits')
	error_count = 0.0
	test_length = len(test_fileList)

	for i in range(test_length):
		filename_str = test_fileList[i]
		file_str = filename_str.split('.')[0]
		class_numberStr = int(file_str.split('_')[0])

		vector_test = image2Vector('testDigits/%s' %filename_str)

		classifier_result = classify(vector_test, trainingMat, handwriting_labels, 3)

		print "the classifier came back with: %d, the real answer is: %d" %(classifier_result, class_numberStr)

		if (classifier_result != class_numberStr):
			error_count += 1.0
	
	print "the total number of errors is: %d" %error_count
	print "the total error rate is: %f" %(error_count / float(test_length))


