import math


class BinClassify(object):
	def __init__(self):
		self.val = True
		self.varQuestion = 0
	
	def CoutQustion(self, number):
		if number > 1 and type(number) == type(1):
			self.varHigh = number
			self.varQuestion = math.ceil(math.log(number, 2))
			self.val = False
			return self.varQuestion
		else:
			print("The range does not fit.")
			return None
			
	def Answer(self, arr):
		if len(arr) != self.varQuestion or self.val:
			print("The array and the number of questions do not match(CoutQustion).")
			return None
		low = 1
		high = self.varHigh 
		for i in arr:
			mid = (low + high) // 2
			if i == 0:
				high = mid 
			elif i == 1:
				low = mid  
			else:
				print("The number is not 1 not 0.")
				return None
		 
		return high