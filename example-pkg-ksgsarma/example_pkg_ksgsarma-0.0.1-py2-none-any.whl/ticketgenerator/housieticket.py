import random
import copy
flag = 1
def generateTicket():
	row_one_count = 5
	row_two_count = 5
	row_three_count = 5
	ones_count = 3
	two_count = 6
	i = 0
	j = 0
	ticket = [[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]]
	lala = [1,2,3,4,5,6,7,8,9,10]
	while(ones_count > 0 and two_count > 0):
		#print(ones_count, two_count)
		x = random.choice([1,2])
		if x == 1:
			ones_count -= 1
		else:
			two_count -= 1
		l = [0,1,2]
		if(row_one_count == 0):
			l.remove(0)
		if(row_two_count == 0):
			l.remove(1)
		if(row_three_count == 0):
			l.remove(2)
		haha = copy.deepcopy(lala)
		for o in range(x):
			n = random.choice(lala)
			lala.remove(n)
			k = random.choice(l)
			l.remove(k)
			if k == 0:
				row_one_count -= 1
			elif k == 1:
				row_two_count -= 1
			else:
				row_three_count -= 1
			ticket[k][j] = n
		#print(n)
		j = j + 1
		i = i + 10
		lala = haha
		for i in range(10):
			lala[i] += 10
		
	while(ones_count > 0 ):
		x = 1
		l = [0,1,2]
		if(row_one_count == 0):
			l.remove(0)
		if(row_two_count == 0):
			l.remove(1)
		if(row_three_count == 0):
			l.remove(2)
		haha = copy.deepcopy(lala)
		for o in range(x):
			n = random.choice(lala)
			lala.remove(n)
			k = random.choice(l)
			l.remove(k)
			if k == 0:
				row_one_count -= 1
			elif k == 1:
				row_two_count -= 1
			else:
				row_three_count -= 1
			ticket[k][j] = n
		#print(n)
		j = j + 1
		i = i + 10
		ones_count -= 1
		lala = haha
		for i in range(10):
			lala[i] += 10
		
	while(two_count > 0 ):
		x = 2
		l = [0,1,2]
		if(row_one_count == 0):
			l.remove(0)
		if(row_two_count == 0):
			l.remove(1)
		if(row_three_count == 0):
			l.remove(2)
		haha = copy.deepcopy(lala)
		for o in range(x):
			n = random.choice(lala)
			lala.remove(n)
			k = random.choice(l)
			if k == 0:
				row_one_count -= 1
			elif k == 1:
				row_two_count -= 1
			else:
				row_three_count -= 1
			l.remove(k)
			ticket[k][j] = n
			#print(n)
		j = j + 1
		i = i + 10
		two_count -= 1
		lala = haha
		for i in range(10):
			lala[i] += 10
			
	for j in range(9):
		abcde = []
		for i in range(3):
			if ticket[i][j] != 0:
				abcde.append(ticket[i][j])
		abcde.sort()
		for i in range(3):
			if ticket[i][j] != 0:
				ticket[i][j] = abcde[0]
				abcde.remove(ticket[i][j])
	return ticket

def ticket_mail_generator(a):
	string = ""
	for i in a:
		string += "<tr>"
		for j in i:
			x = str(j)
			if j == 0:
			 	x = ""
			string += "<td>" + x + "</td>"
		string += "</tr>"
	ticket = "<table border = ""1"">" + string +" </table>"
	return ticket
	
def ticket_html(ticket):
	html = '''<html><head><style>table{border-collapse:collapse;}</style></head><body>'''
	html += ticket + '</body></html>'
	
	return html
def get_ticket(n):
	haha = []
	arehoo = ''
	while n > 0:
		flag = 1
		while(flag == 1):
			try:
				l = generateTicket()
				flag = 0
				ticket = ticket_mail_generator(l)
				haha.append(ticket)
			except:
				pass
		n -= 1
	for i in range(len(haha)):
		arehoo += "<p>Ticket No:" + str(i + 1) + "</p>" + haha[i] + "<br>"  
	ramayan = ticket_html(arehoo)
	return ramayan
	