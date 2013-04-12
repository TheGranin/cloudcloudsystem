from collections import OrderedDict


#http://stackoverflow.com/questions/2437617/limiting-the-size-of-a-python-dictionary
class LimitedSizeDict():
	def __init__(self, size_limit, *args):
		self.size_limit = size_limit
		self.d = OrderedDict(*args)
		self._check_size_limit()

	def __setitem__(self, key, value):
		self.d[key] =  value
		self._check_size_limit()
	def __getitem__(self, key):
		value = self.d[key]
		self.pop(key)
		self[key] = value
		return value

	def __len__(self):
		return len(self.d)
	def __delitem__(self, k):
		del self.d[k]
	
	def pop(self,key):
		self.__delitem__(key)
		
	def __iter__(self):
		return iter(self.d)

	def _check_size_limit(self):
		if self.size_limit is not None:
			while len(self) > self.size_limit:
				self.d.popitem(last=False)
	def __str__(self):
		return str(self.d)
if __name__ == '__main__':
	d = {'banana': 3, 'apple':4, 'pear': 1, 'orange': 2}
	lm = LimitedSizeDict(4, d)
	lm['jordon'] = 1
	lm['satan'] = 1
	print lm['banana']
	lm.pop('jordon')
	print lm
	print 'satan' in lm
	print lm


