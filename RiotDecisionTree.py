import numpy
import scipy.io
import math
import csv
import sys

maxDepth = 124

class Node:
	def __init__(self, split_rule, left = None, right = None):
		self.split_rule = split_rule
		self.left = left
		self.right = right

	def getRule(self):
		return self.split_rule

	def getLeft(self):
		return self.left

	def getRight(self):
		return self.right

	def isLeaf(self):
		return False

class LeafNode(Node):
	def __init__(self, label):
		self.split_rule = None
		self.left = None
		self.right = None
		self.label = label

	def getLabel(self):
		return self.label

	def isLeaf(self):
		return True

def allSpam(data, labels):
	for i in range(len(data)):
		if labels[i] != 1:
			return False
	return True

def allHam(data, labels):
	for i in range(len(data)):
		if labels[i] != 0:
			return False
	return True

def findMajority(data, labels):
	spam_count = 0
	ham_count = 0
	for i in range(len(data)):
		if labels[i] == 1:
			spam_count += 1
		else:
			ham_count += 1
	if spam_count >= ham_count:
		return 1
	else:
		return 0

def impurity(left, right):

	left_total = left["spam"] + left["ham"]
	if left_total == 0:
		left_pct = 0
	else:
		left_pct = left["spam"]/float(left_total)
	right_total = right["spam"] + right["ham"]
	if right_total == 0:
		right_pct = 0
	else:
		right_pct = right["spam"]/float(right_total)

	if left_pct == 1.0:
		left_impurity = 0
	elif left_pct == 0.0:
		left_impurity = 1
	else:
		left_impurity = 0.0
		left_impurity += left_pct*math.log(left_pct, 2)
		left_impurity += (1 - left_pct)*math.log((1 - left_pct), 2)
		left_impurity = -left_impurity
	if right_pct == 1.0:
		right_impurity = 0
	elif right_pct == 0.0:
		right_impurity = 1
	else:
		right_impurity = 0.0
		right_impurity += right_pct*math.log(right_pct, 2)
		right_impurity += (1 - right_pct)*math.log((1 - right_pct), 2)
		right_impurity = -right_impurity

	return left_impurity + right_impurity

def segmentor(data_points, data_labels, impurity):
	best_feature = None
	best_threshold = 0
	best_impurity = float("inf")

	for i in range(len(data_points[0])):
		spam_count = 0
		ham_count = 0
		spam_total = 0
		ham_total = 0
		for j in range(len(data_points)):
			if data_labels[j] == 1:
				spam_count += 1
				spam_total += data_points[j][i]
			else:
				ham_count += 1
				ham_total += data_points[j][i]
		spam_average = spam_total/float(spam_count)
		ham_average = ham_total/float(ham_count)
		average = (spam_average + ham_average)/2
		left = {"spam" : 0, "ham" : 0}
		right = {"spam" : 0, "ham" : 0}
		for j in range(len(data_points)):
			if data_points[j][i] >= average:
				if data_labels[j] == 1:
					left["spam"] += 1
				else:
					left["ham"] += 1
			else:
				if data_labels[j] == 1:
					right["spam"] += 1
				else:
					right["ham"] += 1
		current_impurity = impurity(left, right)
		if current_impurity < best_impurity:
			best_feature = i
			best_threshold = average
			best_impurity = current_impurity

	return (best_feature, best_threshold)


class DecisionTree:

	def __init__(self, depth, impurity, segmentor):
		self.depth = depth
		self.impurity = impurity
		self.segmentor = segmentor
		self.root = None

		self.inOrder = []
		self.postOrder = []

	def train(self, data, labels):
		self.root = self.train_helper(data, labels, self.depth)

	def train_helper(self, data, labels, depth):
		if allSpam(data, labels):
			return LeafNode(1)
		elif allHam(data, labels):
			return LeafNode(0)
		elif depth == 0:
			majority = findMajority(data, labels)
			if majority == 1:
				return LeafNode(1)
			else:
				return LeafNode(0)
		split_decision = self.segmentor(data, labels, self.impurity)
		feature = split_decision[0]
		threshold = split_decision[1]

		set0 = []
		set0_labels = []
		set1 = []
		set1_labels = []
		for i in range(len(data)):
			if data[i][feature] >= threshold:
				set0.append(data[i])
				set0_labels.append(labels[i])
			else:
				set1.append(data[i])
				set1_labels.append(labels[i])

		return Node(split_decision, self.train_helper(set0, set0_labels, depth - 1), self.train_helper(set1, set1_labels, depth - 1))

	def predict(self, data):
		predictions = []
		for point in data:
			prediction= self.predict_helper(self.root, point)
			predictions.append(prediction)
		return predictions

	def predict_helper(self, current_node, data):
		if current_node.isLeaf():
			return current_node.getLabel()

		splitRule = current_node.getRule()

		feature = splitRule[0]
		threshold = splitRule[1]

		if data[feature] == 1:
			return self.predict_helper(current_node.getLeft(), data)
		else:
			return self.predict_helper(current_node.getRight(), data)

	def getInOrderTraversal(self):
		self.inOrder = []
		self.inOrderHelper(self.root)

	def inOrderHelper(self, current_node):
		if current_node is None:
			return
		else:
			self.inOrderHelper(current_node.getLeft())
			self.inOrder.append(current_node)
			self.inOrderHelper(current_node.getRight())

	def getPostOrderTraversal(self):
		self.postOrder = []
		self.postOrderHelper(self.root)

	def postOrderHelper(self, current_node):
		if current_node is None:
			return
		else:
			self.postOrderHelper(current_node.getLeft())
			self.postOrderHelper(current_node.getRight())
			self.postOrder.append(current_node)

	def export(self):
		f = open('savedTree.txt', 'wb')
		for i in range(len(self.inOrder)):
			current_node = self.inOrder[i]
			if current_node.isLeaf() == False:
				splitRule = current_node.getRule()
				splitFeature = splitRule[0]
				f.write("%d " % splitFeature)
			else:
				label = current_node.getLabel()
				if label == 1:
					f.write("Win ")
				else:
					f.write("Lose ")
		f.write('\n')

		for i in range(len(self.postOrder)):
			current_node = self.postOrder[i]
			if current_node.isLeaf() == False:
				splitRule = current_node.getRule()
				splitFeature = splitRule[0]
				f.write("%d " % splitFeature)
			else:
				label = current_node.getLabel()
				if label == 1:
					f.write("Win ")
				else:
					f.write("Lose ")

		f.close()


def main():
	mat = scipy.io.loadmat(sys.argv[1])
	trainingData = mat['trainingData']
	trainingLabels = mat['trainingLabels'][0]


	classifier = DecisionTree(maxDepth, impurity, segmentor)
	classifier.train(trainingData, trainingLabels)

	#classifier.getInOrderTraversal()
	#classifier.getPostOrderTraversal()

	#classifier.export()

	testData = scipy.io.loadmat(sys.argv[2])
	predictions = classifier.predict(testData)

	f = open('DecisionTreePredictions.csv', 'wb')
	writer = csv.writer(f)
	writer.writerow(['Team Comp Number', 'Result'])
	for i in range(len(predictions)):
		if predictions[i] == 1
			writer.writerow([i+1, "Win"])
		else:
			writer.writerow([i+1, "Loss"])

	f.close()


if __name__ == "__main__":
	main()
