# -*- coding: utf-8 -*-

from math import log
import operator

def calcShannonEnt(dataSet):
	number_entries = len(dataSet)
	label_count = {}

	for featVec in dataSet:
		current_label = featVec[-1]
		if current_label not in label_count.keys():
			label_count[current_label] = 0
		label_count[current_label] += 1
	
	shannonEnt = 0.0
	for key in label_count:
		prob = float(label_count[key]) / number_entries
		shannonEnt -= prob * log(prob, 2)
	
	return shannonEnt


def createDataSet():
	dataSet = [[1, 1, 'yes'], 
			[1, 1, 'yes'], 
			[1, 0, 'no'], 
			[0, 1, 'no'], 
			[0, 1, 'no']]

	labels = ['no surfacing', 'flippers']

	return dataSet, labels



# 按照属性划分数据集
'''
	@params:
		dataSet: 待划分的数据集
		axis: 待划分的数据集特征
		value: 需要返回的特征的值
'''
def split_dataSet(dataSet, axis, value):
	return_dataSet = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reduce_featVec = featVec[:axis]
			reduce_featVec.extend(featVec[axis + 1 :])
			return_dataSet.append(reduce_featVec)
	
	return return_dataSet


# 选择最好的数据集划分方式
def choose_bestFeature_split(dataSet):
	number_features = len(dataSet[0]) - 1
	base_entropy = calcShannonEnt(dataSet)

	best_infoGain = 0.0
	best_feature = -1

	for i in range(number_features):
		feature_list = [example[i] for example in dataSet]
		unique_values = set(feature_list)
		new_entropy = 0.0

		for value in unique_values:
			sub_dataSet = split_dataSet(dataSet, i, value)
			prob = len(sub_dataSet) / float(len(dataSet))
			new_entropy += prob * calcShannonEnt(sub_dataSet)

		info_gain = base_entropy - new_entropy
		if (info_gain > best_infoGain):
			best_infoGain = info_gain
			best_feature = i
	
	return best_feature


def majorityCnt(classList):
	class_count = {}

	for vote in classList:
		if vote not in class_count.keys():
			class_count[vote] = 0
		class_count[vote] += 1
	
	sortedClass_count = sorted(class_count.iteritems(), key = operator.itemgetter(1), reverse = True)

	return sortedClass_count[0][0]



def createTree(dataSet, labels):
	classList = [example[-1] for example in dataSet]
	
	# 类别完全相同
	if classList.count(classList[0]) == len(classList):
		return classList[0]

	if len(classList[0]) == 1:
		return majorityCnt(classList)

	bestFeature = choose_bestFeature_split(dataSet)
	bestFeature_label = labels[bestFeature]

	my_tree = {bestFeature_label:{}}
	del(labels[bestFeature])

	feature_values = [example[bestFeature] for example in dataSet]
	unique_values = set(feature_values)

	for value in unique_values:
		sub_labels = labels[:]
		my_tree[bestFeature_label][value] = createTree(split_dataSet(dataSet, bestFeature, value), sub_labels)
	
	return my_tree


def classify(input_tree, feature_labels, test_vector):
	first_str = input_tree.keys()[0]
	second_dict = input_tree[first_str]
	feature_index = feature_labels.index(first_str)

	for key in second_dict.keys():
		if test_vector[feature_index] == key:
			if type(second_dict[key]).__name__ == 'dict':
				class_label = classify(second_dict[key], feature_labels, test_vector)
			else:
				class_label = second_dict[key]
	return class_label



def store_tree(input_tree, filename):
	import pickle
	file_write = open(filename, 'w')

	pickle.dump(input_tree, file_write)
	file_write.close()


def grab_tree(filename):
	import pickle
	file_read = open(filename)

	return pickle.load(file_read)




