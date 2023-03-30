import calendar
y = int(input('digite o ano: '))
while True:
	m = int(input('digite 1 para iniciar: '))
	if m != 1:
		print('opção invalida')
	if m == 1:
		break
while m != 13:
	print(calendar.month(y, m))
	m += 1
