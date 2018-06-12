def comptelespoints(manche):
	gagnant=manche.winner
	quiappel=manche.enchereslog[-1][0]%2
	cbappel=manche.encherslog[-1][1]
	lespoints=manche.points
	capot=true
	for k in range(len(manche.plis) - 1):
		capot = capot and manche.plis[k+1][1]%2==manche.plis[k][1]%2
	if capot:
		if gagnant==0:
			A=(252+cbappel,0)
		else:
			A=(0,252+cbappel)
	elif quiappel==gagnant:
		if gagnant==0:
			A=(cbappel+lespoints,162-lespoints)
		else:
			A=(162-lespoints,cbappel+lespoints)
	else:
		if gagnant==0:
			A=(162+cbappel,0)
		else:
			A=(0,cbappel+162)
	return A
