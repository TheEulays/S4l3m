def __repr__(self):
	s = "--------------------------------\n\n"
	s += "*********** ANNONCES : ***********\n"
	s += "\n"
	g = self.joueurs
	for k in self.encheresLog:
		id = k[0]
		montant = k[1]
		couleur = k[2]
		name = g[id].name
		s += "\n"
		s += name + " annonce : " + str(montant) + " | " + couleur
		s += "\n"
	s += "L'équipe " + str(self.encheresLog[-1][0] % 2) + " a pris à " + str(self.encheresLog[-1][1]) + " | " + self.encheresLog[-1][2]
	s += "\n"
	s += "*********** JEU : ***********"
	s += "\n"
	tour = 0
	for k in self.plis:
		s += "Tour : " + srt(tour) + "\n"
		commence = k[0]
		gagne = k[1].index #C'est bizarre, ça, TODO regarder d'ou ca vient
		card = k[2]
		i = commence
		for j in range(0,4):
			s += g[i].name + " : " + card[j].__repr__() + "\n"
			i += 1
			if i > 3:
				i = 0
		s += g[gagne].name + " remporte le pli !\n"
		tour += 1
	s += "*********** RÉSULTAT : ***********\n"
	s += "L'équipe " + str(self.winner) + " a gagné !\n"
	s += "Équipe " + str(self.winner) + " : " + str(manche.points) +¨"\n"
	s += "Équipe " + str(- 1 * self.winner + 1) + " : " + str(162 - manche.points) + "\n"
		