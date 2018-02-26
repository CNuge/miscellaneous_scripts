
class ChangeCal():

	def calculate_change(self, cost, paid):
		""" calculate the difference between the cost and the money given"""
		self.__change_amount = paid - cost

		#play with the below error to make sure it flags underpayment
		#but also lets rounding to the nearest nickle through
		if self.__change_amount < -0.02:
			raise ValueError(f'{cost-paid:.2f}')
		elif self.__change_amount <= 0.2:
			self.__change_amount = 0.0
		print(f'${self.__change_amount:.2f}')
	
	@property
	def change(self):
		return self.__change_amount

	@property
	def change_breakdown(self):
		""" represent the change in an optimal set of bills and change"""
		denominations = {100 : None, 50 : None, 20 : None, 10 : None, 5 : None,
							2 : None, 1 : None, 0.25 : None, 0.1 : None, 0.05 : None}
		if self.__change_amount < -0.02:
			raise ValueError(f'They have underpaid you by: ${-self.__change_amount:.2f}')

		total_breakdown = self.__change_amount
		for i in denominations.keys():
			num_denom = total_breakdown // i
			if num_denom != 0:
				denominations[i] = int(num_denom)
				total_breakdown = total_breakdown - (num_denom * i)

		outstring = ' '
		for k, v in denominations.items():
			if v is not None:
				if k >= 5:
					outstring += f"{v} ${k} bill"
				else:
					outstring += f"{v} ${k} coin"
				if v > 1:
					outstring += 's'
				outstring += '\n'
		return outstring

	def __repr__(self):
		return f'change due: ${self.__change_amount}\n{self.change_breakdown}'

if __name__ == '__main__':
	test = ChangeCal()

	c1 = 2.40
	p1 = 5.00

	test.calculate_change(c1,p1)
	print(test.change_breakdown)
	test

	c2 = 17.38
	p2 = 20.00
	test.calculate_change(c2,p2)
	print(test.change_breakdown)

	#value error
	c3 = 21.77
	p3 = 20.75
	test.calculate_change(c3,p3)
	print(test.change_breakdown)

	#should be withing rounding tolerance
	c4 = 21.77
	p4 = 21.75
	test.calculate_change(c4,p4)
	print(test.change_breakdown)
