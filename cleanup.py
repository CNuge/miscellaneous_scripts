tagged ='13-10-03 13-10-03 13-10-03 13-10-03 13-10-03 13-10-03 13-10-03 13-10-03 13-10-17 13-10-17 13-10-17 13-10-17 13-10-24 13-10-24 13-10-24 13-10-24 13-10-24 13-10-31 13-10-31 13-10-31 13-10-31 13-11-07 13-11-07 13-11-07 13-11-07 13-11-07 13-11-07 13-11-07 13-11-07 13-11-21 13-11-21 13-11-21 13-11-21 13-11-27 13-11-27 13-11-27 13-11-27 13-11-27 13-11-27 13-11-27 13-11-27 13-12-04 13-12-04 13-12-04'.split()

outstring=''

for i in tagged:
	dat = i.split('-')

	out = f'{dat[2]}-{dat[1]}-20{dat[0]}\n'

	outstring +=out
