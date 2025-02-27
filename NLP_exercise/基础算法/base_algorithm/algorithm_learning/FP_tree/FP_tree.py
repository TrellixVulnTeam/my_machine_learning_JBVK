# -*- coding: utf-8 -*-

# FP (frequency pattern) tree
class treeNode:
	def __init__(self, nameValue, numOccur, parentNode):
		self.name = nameValue
		self.count = numOccur
		self.nodeLink = None
		self.parent = parentNode
		self.children = {}
	
	def inc(self, numOccur):
		self.count += numOccur
	
	def disp(self, ind = 1):
		print "   " * ind, self.name, "   ", self.count
		for child in self.children.values():
			child.disp(ind + 1)



def create_tree(dataSet, min_support = 1):
	header_table = {}
	for trans in dataSet:
		for item in trans:
			header_table[item] = header_table.get(item, 0) + dataSet[trans]
	
	for key in header_table.keys():
		if header_table[key] < min_support:
			del(header_table[key])
	
	freq_itemSet = set(header_table.keys())

	if len(freq_itemSet) == 0:
		return None, None

	for k in header_table:
		# None 表示存储的指针
		header_table[k] = [header_table[k], None]
	
	return_tree = treeNode('Null Set', 1, None)

	for tran_set, count in dataSet.items():
		local_data = {}
		for item in tran_set:
			if item in freq_itemSet:
				# 取出 count
				local_data[item] = header_table[item][0]

		if len(local_data) > 0:
			order_items = [v[0] for v in sorted(local_data.items(), key = lambda p: p[1], reverse = True)]
			update_tree(order_items, return_tree, header_table, count)
	
	return return_tree, header_table



def update_tree(items, in_tree, header_table, count):
	if items[0] in in_tree.children:
		in_tree.children[items[0]].inc(count)
	else:
		in_tree.children[items[0]] = treeNode(items[0], count, in_tree)
		# 空指针,新建指针域
		if header_table[items[0]][1] == None:
			header_table[items[0]][1] = in_tree.children[items[0]]
		# 更新指针域
		else:
			update_header(header_table[items[0]][1], in_tree.children[items[0]])
	
	if len(items) > 1:
		update_tree(items[1::], in_tree.children[items[0]], header_table, count)




def update_header(node_to_test, target_node):
	while(node_to_test.nodeLink != None):
		node_to_test = node_to_test.nodeLink
	
	node_to_test.nodeLink = target_node




def load_simpData():
	simple_data = [['r', 'z', 'h', 'j', 'p'], 
			['z', 'y', 'x', 'w', 'v', 'u', 't', 's'], 
			['z'], 
			['r', 'x', 'n', 'o', 's'], 
			['y', 'r', 'x', 'z', 'q', 't', 'p'], 
			['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
	return simple_data


# 由于 create_tree() 函数中的参数 dataSet 是一个字典，故应将 load_simpData()函数中的列表 list 类型转化成为字典 dict 类型的数据
def create_initSet(dataSet):
	return_dict = {}
	for trans in dataSet:
		return_dict[frozenset(trans)] = 1
	return return_dict


def ascend_tree(leaf_node, prefix_path):
	if leaf_node != None:
		prefix_path.append(leaf_node.name)
		ascend_tree(leaf_node.parent, prefix_path)


def find_prefixPath(basePat, tree_node):
	condPats = {}
	while tree_node != None:
		prefix_path = []
		ascent_tree(tree_node, prefix_path)
		if len(prefix_path) > 1:
			condPats[frozenset(prefix_path[1:])] = tree_node.count
		tree_node = tree_node.parent
	return condPats



def mine_tree(in_tree, header_table, min_support, prefix, freqItem_list):
	big_len = [v[0] for v in sorted(header_table.items(), key = lambda p: p[1])]
	
	for basePat in big_len:
		new_freqSet = prefix.copy()
		new_freqSet.add(basePat)
		freqItem_list.append(new_freqSet)

		condPattBases = find_prefixPath(basePat, header_table[basePat][1])
		my_condTree, header = create_tree(condPattBases, min_support)
		if header != None:
			mine_tree(my_condTree, header, min_support, new_freqSet, freqItem_list)








