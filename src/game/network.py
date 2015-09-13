import numpy as np
import os
import pyradbas as pyrb

dir = os.path.dirname(__file__)

class Network(object):

	def __init__(self, filename, ahead):

		self.data = []
		self.dataLength = 0
		self.target = []
		self.ahead = ahead
		self.net = None

		input = []
		output = []

		with open(os.path.join(dir, filename)) as reactions:
			
			for line in reactions:
				parts = line.split(";")
				chunk = []

				for i in range(self.ahead * 3):
					chunk.append(int(float(parts[i])))

				input.append(chunk)
				output.append(int(parts[len(parts) - 1]))

		self.data = np.array(input).reshape((len(input), self.ahead * 3))
		self.target = np.array(output).reshape((len(output), 1))
		self.dataLength = len(input)

	def train(self):

		self.net = pyrb.train_ols(self.data, self.target, 0.00001, 0.6, verbose=True)
		S = self.net.sim(self.data)

		errors = 0
		count = 0

		for i in range(len(self.target)):
			count += 1

			if int(round(S[i][0])) != self.target[i]:
				errors += 1

		print('Learning error: ' + str(round((errors / count) * 100)) + '%')
		

	def sim(self, board):
		return self.net.sim(board)

if __name__ == '__main__':
	net = Network("results/reactions.txt", 1)
	net.train()
