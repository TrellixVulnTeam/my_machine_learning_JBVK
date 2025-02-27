# -*- coding: utf-8 -*-

def load_dataSet():
	return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]



def create_candidate(dataSet):
	candidate = []
	for transaction in dataSet:
		for item in transaction:
			if not [item] in candidate:
				candidate.append([item])	
	candidate.sort()
	# 候选 1 项集不可修改，故使用 frozenset 函数
	return map(frozenset, candidate)



def scan_dataSet(dataSet, candidate, min_support):
	candidate_dict = {}
	for tid in dataSet:
		for can in candidate:
			if can.issubset(tid):
				if not candidate_dict.has_key(can):
					candidate_dict[can] = 1
				else:
					candidate_dict[can] += 1	
	number_items = float(len(dataSet))
	ret_list = []
	support_data = {}
	for key in candidate_dict:
		support = candidate_dict[key] / number_items
		if support >= min_support:
			ret_list.insert(0, key)
		support_data[key] = support
	return ret_list, support_data




# 由频繁 k 项集生成候选 k+1 项集
def apriori_generate(Lk, k):
	return_list = []
	len_Lk = len(Lk)
	for i in range(len_Lk):
		for j in range(i + 1, len_Lk):
			L1 = list(Lk[i])[: k - 2]
			L2 = list(Lk[j])[: k - 2]
			L1.sort()
			L2.sort()
			if L1 == L2:
				return_list.append(Lk[i] | Lk[j])	# 两个集合合并
	return return_list




def apriori(dataSet, min_support = 0.5):
	candidate = create_candidate(dataSet)
	dataSet = map(set, dataSet)
	L1, support_data = scan_dataSet(dataSet, candidate, min_support)
	L = [L1]
	k = 2
	while(len(L[k - 2]) > 0):
		candidate_k = apriori_generate(L[k - 2], k)
		Lk, support_k = scan_dataSet(dataSet, candidate_k, min_support)
		support_data.update(support_k)
		L.append(Lk)
		k += 1
	return L, support_data




def generate_rules(L, support_data, min_conf = 0.7):
	big_ruleList = []
	for i in range(1, len(L)):
		for freq_set in L[i]:
			H1 = [frozenset([item]) for item in freq_set]
			if (i > 1):
				rule_conseq(freq_set, H1, support_data, big_ruleList, min_conf)
			else:
				calc_conf(freq_set, H1, support_data, big_ruleList, min_conf)	
	return big_ruleList




def calc_conf(freq_set, H, support_data, rule_list, min_conf = 0.7):
	pruned_rule = []
	for conseq in H:
		conf = support_data[freq_set] / support_data[freq_set - conseq]
		print "conf: ", conf
		if conf >= min_conf:
			print "freq_set: ", freq_set
			print freq_set - conseq, '-->', conseq, 'conf: ', conf
			print "----------------------------------"
			rule_list.append((freq_set - conseq, conseq, conf))
			pruned_rule.append(conseq)
	return pruned_rule




def rule_conseq(freq_set, H, support_data, rule_list, min_conf = 0.7):
	length = len(H[0])
	if (len(freq_set) > (length + 1)):
		H_temp = apriori_generate(H, length + 1)
		H_temp = calc_conf(freq_set, H_temp, support_data, rule_list, min_conf)
		if (len(H_temp) > 1):
			rule_conseq(freq_set, H_temp, support_data, rule_list, min_conf)




from time import sleep
from votesmart import votesmart

def get_actionID():
	actionID_list = []
	billTitle_list = []
	file = open('recent20bills.txt')
	for line in file.readlines():
		bill_number = int(line.split('\t')[0])
		try:
			bill_detail = votesmart.votes.getBill(bill_number)
			for action in bill_detail.actions:
				# 过滤出包含投票的行为
				if action.level == 'House' and (action.stage == 'Passage' or action.stage == 'Amendment Vote'):
					action_id = int(action.action_id)
					print "bill: %d has action_id: %d " %(bill_number, action_id)
					actionID_list.append(action_id)
					billTitle_list.append(line.strip().split('\t')[1])
		except:
			print "problem getting bill %d " % bill_number
		sleep(1)
	return actionID_list, billTitle_list



