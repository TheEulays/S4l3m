#import socket
import random
import math
import numpy as np
import pickle
import gc
import time
gc.enable()

t = time.time()

def top():
	global t
	print(time.time() - t)
	t = time.time()

def pack(obj, fileName):
	"""Fonction permettant de sérialiser obj dans le fichier fileName."""
	f = open(fileName, 'wb')
	pickle.dump(obj, f)
	f.close()

def unpack(fileName):
	"""Fonction permettant de désérialiser l'objet dans fileName."""
	f = open(fileName, 'rb')
	temp = pickle.load(f)
	f.close()
	return temp

    
#s = socket.socket()
#s.connect(("localhost", 4321))

#Entree : parametres du jeu
#Sortie : carte a jouer (index)



# -----------------------------

class Genome:
    def __init__(self):
        self.genes = []

class Gene:
    CONNECTION_TYPE = 0
    NODE_TYPE = 1
    def __init__(self, TYPE):
        self.TYPE = TYPE

    
def generateNN(genome):
    pass #TODO, pour David ? C'est des arbres rigolos...


class NN:#Neural network (V2.0) TODO
    def __init__(self, nodes, connections, w, b):
        pass
        
#-------------------------
class BeloteServer:
    
    INIT_STATE = 0
    def __init__(self, servsock):
        self.ss = servsock
        self.state = INIT_STATE
        self.log = []
        self.socketpool = []

    def run(self):
        pass #Threading
        
#------------------------------
    

class Manche: #Sert a stocker des trucs

	def __init__(self, joueurs): #TODO Tout déclarer proprement
		self.joueurs = joueurs
		self.plis = []

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
		s += "Équipe " + str(self.winner) + " : " + str(manche.points) + "\n"
		s += "Équipe " + str(- 1 * self.winner + 1) + " : " + str(162 - manche.points) + "\n"
		return s

class Carte:

    tabatou ={"7" : 0,"8" : 1,"dame" : 2,"roi" : 3,"10" : 4,"1" : 5,"9" : 6,"valet" : 7}
    tabpaatou = {"7" : 0,"8" : 1,"9" : 2,"valet" : 3,"dame" : 4,"roi" : 5,"10" : 6,"1" : 7}
    valatou = {0 : 0,1 : 0,2 : 3,3 : 4,4 : 10,5 : 11,6 : 14,7 : 20}  
    valpaatou = {0 : 0, 1 : 0, 2 : 0, 3 : 2, 4 : 3, 5 : 4, 6 : 10, 7 : 11}

    def __init__(self,v,c, manche): #Carte(manche) tf TODO
        self.valeur = v
        self.couleur = c
        self.manche = manche

    def value(self):
        atout = self.manche.atout
        if self.couleur == atout:
            return self.valatou[self.tabatou[self.valeur]]
        else:
            return self.valpaatou[self.tabpaatou[self.valeur]]

    def __gt__(self,carte):
        atout = self.manche.atout
        couleurdemandee = self.manche.couleurdemandee
        if (self.couleur == atout and carte.couleur == atout):
            if self.tabatou[self.valeur] > self.tabatou[carte.valeur]:
                return True
            else:
                return False
        elif self.couleur == atout:
            return True
        elif carte.couleur == atout:
            return False
        elif self.couleur == carte.couleur and self.couleur == couleurdemandee:
            if self.tabpaatou[self.valeur] > self.tabpaatou[carte.valeur]:
                return True
            else:
                return False
        elif self.couleur == couleurdemandee:
            return True
        elif carte.couleur == couleurdemandee:
            return False
        elif self.couleur!= couleurdemandee and carte.couleur != couleurdemandee:
            return self.tabpaatou[self.valeur]>self.tabpaatou[carte.valeur]
	    
        else:
            return False
        print(42)
            
    def __lt__(self, carte):
        return not (self > carte)

    def __repr__(self):
        return "( " + self.valeur + " " + self.couleur + " )"

class Deck:
    def __init__(self, cartes):
        self.cartes = cartes

    def everydayImShufflin(self):
        random.shuffle(self.cartes)

def createDeck(manche):        
    preskpak = []
    for k in ["7","8","9","10","valet","dame","roi","1"]:
        for l in ["coeur", "carreau", "pique", "trefle"]:
            preskpak.append(Carte(k,l, manche))
    PAKET = Deck(preskpak)
    PAKET.everydayImShufflin()
    return PAKET

class Joueur:
	def __init__(self, index, partenaire, namae, JAIPADENOM):
		self.index = index
		self.main = []
		self.partenaire = partenaire
		self.name = namae
		self.JAIPADENOM = JAIPADENOM #Strategy Pattern in disguise
		self.JAIPADENOM.joueur = self

	def annoncer(self, manche):
		return self.JAIPADENOM.annonce(self.main, manche)

	def jouer(self, manche):
		return self.JAIPADENOM.jouerUneCarte(self.main, manche)

	def end(self, manche):
		self.JAIPADENOM.end(manche)	

def jaidezatouts(tab, manche):
    a = manche.atout
    for k in tab:
        if k.couleur == a:
            return True
    return False


def plimaitre(c, pred, manche):
    for k in cartespossibleschezlennemiàlacouleurdec:
        if c<k:
            return False
    return True
        
class Sarkis: #Noob bot
    def __init__(self):
        self.compte = []
        self.comptelezatouts = 0
        self.strategie=""
        self.flag=True  #TODO reinitialiser dans les annonces
        self.mesannonces=[]
    
    def end(self, manche):
        pass
 
    def debut(self,main,manche):
        self.paketo = manche.pack
        self.devine = {}
        self.dico={}
        self.appel={}
        self.start=True
        self.comptelezatouts=0
        self.compte=[]
        self.mesannonces=[]
        for k in self.paketo.cartes:
                self.devine[k]=[0,1,1,1]
        for k in main:
                self.devine[k]=[1,0,0,0]

    def atout_main(self,main,manche):
        self.d=0
        for k in main:
            if k.couleur==manche.atout:
                self.d+=1
        return self.d

    def apresLesAnnonces(self,manche):
        if manche.encheresLog[-1][0]%2==self.joueur.index%2:
            self.strategie="atk"
        else:
            self.strategie="def"
    
    def annonce(self,main,manche):
        if len(manche.encheresLog)<=4:
            self.debut(main,manche)
        self.dico={}    #dico contiendra les plis maitres a chaque couleur
        self.appel={}   #appel contiendra les appels à chaque couleur
        #print(main)
        for couleur in ["coeur","carreau","pique","trefle"]:  #boucle de génération des plis maitres
            manche.atout=couleur
            self.o=self.plimaitre(main,manche)  #o est un tableau intermediaire contenant les plis maitres
            #print(self.o)
            self.o.append(self.atout_main(main,manche))
            self.dico[couleur]=self.o
        for couleur in ["coeur","carreau","pique","trefle"]: #boucle de génération des valeurs des potentiels appels
            self.appel[couleur]=0
            self.A=False
            if len(self.dico[couleur])>1:
                for k in self.dico[couleur][:-1]:
                    self.A = (self.A or k.valeur=="valet")
                if self.A:
                    if self.dico[couleur][-1] in (3,4):
                        self.appel[couleur]=80
                    elif self.dico[couleur][-1]>=5:
                        self.appel[couleur]=100
                    self.appel[couleur]+=10*(len(self.dico[couleur])-2)
        self.theappel = (self.appel["coeur"],"coeur")                #ici on compare les appels solo
        #print(self.theappel)                                        #
        for couleur in ["carreau","pique","trefle"]:                 #  
            if self.appel[couleur] >= self.theappel[0]:              #
                self.theappel = (self.appel[couleur], couleur)       #
                #print(self.theappel)
        if len(manche.encheresLog)>=3:          #on considère le fait de surrenchérir a la couleur du partenaire
            if (manche.encheresLog[-2][2] not in self.mesannonces) and manche.encheresLog[-2][0]%2==self.joueur.index: #des closes pour ne pas monter à l'infini à la poursuite du bonheur
                if manche.encheresLog[-2][0]!=self.joueur.index:
                    manche.atout=manche.encheresLog[-2][2]
                    b=self.plimaitre(main,manche)
                
                    self.encherepart=manche.encheresLog[-2][1]
                    self.encherepart+=10*(len(b))
                    if self.theappel[0]<=self.encherepart:    #comparaison entre lappel solo et l'appel duo
                        self.theappel=(self.encherepart,manche.atout)
        #print(self.theappel[0])
        #print(manche.encheresLog[-1][1])
        if manche.encheresLog[-1][1]<self.theappel[0]:

            self.mesannonces.append(self.theappel[1])  #pour ne pas monter à l'infini à la poursuite du bonheur
            a=(self.joueur.index,)+(self.theappel)
            #print(a)
            return a
        else:
            #print("passe")
            return manche.encheresLog[-1]

    def plimaitre(self,main,manche):
        try:
            self.couleursimulee=manche.couleurdemandee
        except:
            self.couleursimulee="NoColor"
        self.plimaitres=[]
        for k in main:
            self.A=True
            for i in self.paketo.cartes:
            
                if k.couleur==i.couleur and i not in main:
                    manche.couleurdemandee=k.couleur
                    self.A = self.A and k > i
            if self.A:
                self.plimaitres.append(k)
        manche.couleurdemandee=self.couleursimulee
        return self.plimaitres
        
        
    def jouerUneCarte(self, main, manche):
        if self.ilrestedezatouts(manche)==0:
            self.strategie="atk"
            
        if self.start:
            if manche.enchere[0]%2 == self.joueur.index%2:
                self.strategie = "atk"
            else:
                self.strategie="def"
            self.start=False
        if manche.plis!=[]:
            for i in manche.plis[-1][2]:
                self.devine[i] = [0,0,0,0]
        for i in manche.pliEnCours:
            self.devine[i] = [0,0,0,0]
        if manche.plis!=[]:
            self.couleur = manche.plis[-1][2][0].couleur
            for i in range(1,4):
                if manche.plis[-1][2][i].couleur != self.couleur:
                    for k in self.paketo.cartes:
                        if k.couleur == self.couleur:
                            self.devine[k][i] =0
        if manche.pliEnCours!=[]:
            self.couleur = manche.pliEnCours[0].couleur
            for i in range(1,len(manche.pliEnCours)):
                if manche.pliEnCours[i].couleur != self.couleur:
                    for k in self.paketo.cartes:
                        if k.couleur == self.couleur:
                            self.devine[k][i] = 0
                        
                
        self.materpli=self.plimaitre(main,manche)
        self.materpli.append(self.atout_main(main,manche))
        self.untableau=[]
        self.cartatou=cartesALaCouleur(main,manche.atout)    
        
        
        if manche.couleurdemandee =="NoColor":
            if self.strategie=="atk" and  self.ilrestedezatouts(manche)!=0 and self.cartatou!=[]:
                #print(self.materpli)
                for k in self.materpli[:-1]:
                    if k.couleur == manche.atout:
                        main.remove(k)
                        return k
                j = minPliALaCouleur(self.cartatou,manche.atout)
                main.remove(j)
                return j
            else:
                for k in self.materpli[:-1]:
                    if k.couleur!=manche.atout:
                        self.untableau.append(k)
                if len(self.untableau)>0:
                    j = self.untableau[0]
                    main.remove(j)
                    return j
                else:
                    j = self.goodplay(main, manche)
                    main.remove(j)
                    return j
        else:
            self.cartescouleur=cartesALaCouleur(main,manche.couleurdemandee)
            
            if len(manche.pliEnCours)==1:
                if manche.couleurdemandee== manche.atout:
                    if self.strategie=="atk":
                        try:
                            self.m=max(self.cartatou)
                            if self.m>manche.pliEnCours[-1]:
                                j = self.m
                                main.remove(j)
                                return j
                            else:
                                j = min(self.cartatou)
                                main.remove(j)
                                return j
                        except:
                            try:
                                j = random.choice([k for k in main if k not in self.materpli])
                                main.remove(j)
                                return j
                            except:
                                j = random.choice(main)
                                main.remove(j)
                                return j
                    else:
                        self.c=[k for k in self.cartatou if k>manche.pliEnCours[0]]
                        if self.c!=[]:
                            j = min(self.c)
                            main.remove(j)
                            return j
                        else:
                            try:
                                j = min(self.cartatou)
                                main.remove(j)
                                return j
                            except:
                                j = min(main)
                                main.remove(j)
                                return j
                else:
                    if self.cartescouleur !=[]:
                        self.d=[k for k in self.cartescouleur if k  in self.materpli]
                        if self.d!=[]:
                            j = max(self.d)
                            main.remove(j)
                            return j
                        else:
                            j = min(self.cartescouleur)
                            main.remove(j)
                            return j
                    elif self.cartatou!=[]:
                        if self.strategie=="atk":
                            j = min(self.cartatou)
                            main.remove(j)
                            return j
                        else:
                            j = max(self.cartatou)
                            main.remove(j)
                            return j
                    else:
                        j = min(main)
                        main.remove(j)
                        return j
                                    
                                    
            elif len(manche.pliEnCours)==2:
                self.cartpart=manche.pliEnCours[-2]
                self.flag=self.cartpart > manche.pliEnCours[-1]
                if manche.couleurdemandee!=manche.atout:
                    for k in self.paketo.cartes:
                        if k.couleur!=manche.atout and self.devine[k][(self.joueur.index+1)%4]!=0:
                            self.flag = self.flag and self.cartpart>k
                else:
                    for k in self.paketo.cartes:
                        if self.devine[k][(self.joueur.index+3)%4]!=0:
                            self.flag = self.flag and self.cartpart>k
                if self.flag:
                    if self.cartescouleur!=[]:
                        try:
                            j = max([k for k in self.cartescouleur if k not in self.materpli])
                            main.remove(j)
                            return j
                        except:
                            j = max(self.cartescouleur)
                            main.remove(j)
                            return j
                    else:
                        try:
                            j = max([k for k in main if (k not in self.materpli and k not in self.cartatou) ])
                            main.remove(j)
                            return j
                        except:
                            if self.strategie == "atk":
                                try:
                                    j = min([k for k in main if (k in self.materpli and k not in self.cartatou)])
                                    main.remove(j)
                                    return j
                                except:
                                    j = min(main)
                                    main.remove(j)
                                    return j
                            else:
                                j = max(main)
                                main.remove(j)
                                return j
                else:
                    if self.strategie=="atk":
                        if self.cartescouleur != []:
                            for k in self.materpli[:-1]:
                                if k.couleur==manche.couleurdemandee:
                                    main.remove(k)
                                    return k
                            try:
                                j = min([k for k in self.cartescouleur if k not in self.materpli])
                                main.remove(j)
                                return j
                            except:
                                j = min([k for k in self.cartescouleur])
                                main.remove(j)
                                return j
                        elif  (self.cartpart>manche.pliEnCours[-1] or self.cartatou==[]):
                            j = min(main)
                            main.remove(j)
                            return j
                        else:
                            j = min(self.cartatou)
                            main.remove(j)
                            return j
                    else:
                        if self.cartescouleur!=[]:
                            j = max([k for k in self.cartescouleur])
                            main.remove(j)
                            return j
                        else:
                            try:
                                j = max(self.cartatou)
                                main.remove(j)
                                return j
                            except:
                                try:
                                    j = min([k for k in main if k not in self.materpli])
                                    main.remove(j)
                                    return j
                                except:
                                    j = min(main)
                                    main.remove(j)
                                    return j

            else:#On joue en dernier
                self.cartpart=manche.pliEnCours[-2]
                self.maxpli=max(manche.pliEnCours)
                self.flag=(self.cartpart==self.maxpli)
                if self.cartescouleur!=[]:
                    self.m=max(self.cartescouleur)
                    if self.m>self.maxpli:
                        j = self.m
                        main.remove(j)
                        return j
                    elif self.flag:
                        self.f=[k for k in self.cartescouleur if k not in self.materpli]
                        if self.f!=[]:
                            j = max(self.f)
                            main.remove(j)
                            return j
                        else:
                            j = max(self.cartescouleur)
                            main.remove(j)
                            return j
                    else:
                        j = min(self.cartescouleur)
                        main.remove(j)
                        return j
                else:
                    if self.strategie=="atk":
                        if self.flag:
                            try:
                                j = max([k for k in main if (k not in self.materpli and k not in self.cartatou)])
                                main.remove(j)
                                return j
                            except:
                                try:
                                    j = min([k for k in self.materpli not in self.cartatou])
                                    main.remove(j)
                                    return j
                                except:
                                    j = min(main)
                                    main.remove(j)
                                    return j
                        elif self.cartatou!=[]:
                            self.e=[k for k in self.cartatou if k>self.maxpli]
                            if self.e!=[]:
                                j = min(self.e)
                                main.remove(j)
                                return j
                            else:
                                j = min(self.cartatou)
                                main.remove(j)
                                return j
                        else:
                            j = min(main)
                            main.remove(j)
                            return j
                    else:
                        if self.flag:
                            try:
                                j = max([k for k in main if (k not in self.materpli and k not in self.cartatou)])
                                main.remove(j)
                                return j
                            except:
                                try:
                                    j = max([k for k in main if k not in self.cartatou])
                                except:
                                    j = max(main)
                                main.remove(j)
                                return j
                        elif self.cartatou!=[]:
                            self.e=[k for k in self.cartatou if k > self.maxpli]
                            if self.e!=[]:
                                j = max(self.e)
                                main.remove(j)
                                return j
                            else:
                                j = min(self.cartatou)
                                main.remove(j)
                                return j
                        else:
                            j = min(main)
                            main.remove(j)
                    return j                  
                                
    def goodplay(self, main, manche):
        self.truc = []
        for k in main:
                if k.couleur != manche.atout:
                        self.truc.append(k)
        if self.truc != []:
                return random.choice(self.truc)
        return random.choice(main)

    def ilrestedezatouts(self, manche):
        self.c=0
        for k in self.paketo.cartes:
                if k.couleur == manche.atout and self.devine[k][(self.joueur.index+1)%4] != 0 and self.devine[k][(self.joueur.index+3)%4]== 0:
                        self.c+=1
        return self.c

class Human:
    def __init__(self):
        pass

    def annonce(self, main, manche):
        ench = input("Nouvelle enchère")
        if ench == "Passe": #TODO
            return manche.encheresLog[-1]
        couleur=input("pik/keur/karo/trefl le signe de gang :")
        return (self.joueur.index,int(ench),couleur)
	
    def jouerUneCarte(self, main, manche):
        print(main)
        print("Cartes jouables :")
        print(cartesJouables(self.joueur, manche))
        ncarte = input("Quelle carte jouer ?")
        carte = main[int(ncarte)] #TODO Pick among playable cards
        main.remove(carte)
        return carte
    
    def end(self, manche):
        pass

def sigmoid(z): #sigmoid function, faut peut-être l'étaler... z / alpha, alpha > 1, alpha(z);
        return 1 / ( 1 + np.exp(-1 * np.clip(z, -35, 35)))

class NNLBot:
	def __init__(self):
		self.NB_HIDDEN = 410
		self.DIM_IN = 206 #TODO ca va probablement changer
		self.DIM_OUT = 2 # 3 ?

		self.weights1 = np.random.randn(self.NB_HIDDEN, self.DIM_IN)
		self.bias1 = np.random.randn(self.NB_HIDDEN, 1)

		self.weights2 = np.random.randn(self.DIM_OUT, self.NB_HIDDEN)
		self.bias2 = np.random.randn(self.DIM_OUT, 1)
		self.ins = []
		self.hids = []
		self.outs = []

	def generateIN(self, manche, main): #on cree le vecteur d'entree du nn ||| len(IN) = 1 + 31 * 3 + 8 * 5 * 2 + 8 * 2 + 8 * 2 = 206 TODO : Est-ce raisonnable d'utiliser des valeurs = 0 ?
		IN = []
		colorValues = {"NoColor" : -1, "pique" : 1, "coeur" : 2, "trefle" : 3, "carreau" : 4}
		cardValues = {"7" : 1, "8" : 2, "9" : 3, "10" : 4, "valet" : 5, "dame" : 6, "roi" : 7, "1" : 8}
		IN.append(manche.lePremier)
		for k in range(31): #Encheres TODO, nbre max (en prenant en compte contre et surcontre, + 2?)
			if k < len(manche.encheresLog):
				IN.append(manche.encheresLog[k][0])
				IN.append(manche.encheresLog[k][1])
				IN.append(colorValues[manche.encheresLog[k][2]])
			else:
				IN.append(0)
				IN.append(0)
				IN.append(0)
		for k in range(8): #Les plis
			try:
				test = manche.pliEnCours #Si ca rate, go except
				if k < len(manche.plis):
					IN.append(manche.plis[k][0])
					IN.append(manche.plis[k][1])
					for l in range(4):
						IN.append(cardValues[manche.plis[k][2][l].valeur])
						IN.append(colorValues[manche.plis[k][2][l].couleur])
				elif k == len(manche.plis): #Peut etre le mettre a part (endroit fixe ?) (pli en cours)
					IN.append(manche.joueurs[0].index)
					IN.append(0)
					for l in range(4):
						if l < len(manche.pliEnCours):
							IN.append(cardValues[manche.pliEnCours[l].valeur])
							IN.append(colorValues[manche.pliEnCours[l].couleur])
						else:
							IN.append(0)
							IN.append(0)
				else:
					IN.append(0)
					IN.append(0)
					for l in range(4):
						IN.append(0)
						IN.append(0)
			except:
				IN.append(0)
				IN.append(0)
				for l in range(4):
					IN.append(0)
					IN.append(0)
		for k in range(8):#Main
			if k < len(main):
				IN.append(cardValues[main[k].valeur])
				IN.append(colorValues[main[k].couleur])
			else:
				IN.append(0)
				IN.append(0)
		for k in range(8):#Cartes jouables de la main (TODO, redondant ?) TODO le présenter différemment ?
			try: #Meme feinte que plus haut
				j = cartesJouables(self.joueur, manche)
				if k < len(j):
					IN.append(cardValues[j[k].valeur])
					IN.append(colorValues[j[k].couleur])
				else:
					IN.append(0)
					IN.append(0)
			except:
				IN.append(0)
				IN.append(0)
		return IN

	def annonce(self, main, manche):#TODO pas super content de mon implementation.
		IN = np.array([self.generateIN(manche, main)])
		HIDDEN = self.forward_pass(IN, self.weights1, self.bias1)
		OUT = self.forward_pass(HIDDEN, self.weights2, self.bias2)
		self.ins.append(IN)
		self.hids.append(HIDDEN)
		self.outs.append(OUT)
		colors = ["pique", "carreau", "trefle", "coeur"] #Faire un cas passe ?
		try:
			c = colors[math.floor(OUT[0][0] * 4)]
		except:
			c = colors[-1] #Cas où ca fait 4
		e = manche.encheresLog[-1]
		a = e[1]
		v = a + 10 * math.floor(OUT[0][1] * (17 - a / 10)) #Cas 0 TODO
		if v == a:
			return e
		return (self.joueur.index, v, c)
        
	def jouerUneCarte(self, main, manche):
		IN = np.array([self.generateIN(manche, main)])
		HIDDEN = self.forward_pass(IN, self.weights1, self.bias1)
		OUT = self.forward_pass(HIDDEN, self.weights2, self.bias2)
		self.ins.append(IN)
		self.hids.append(HIDDEN)
		self.outs.append(OUT)
		j = cartesJouables(self.joueur, manche)
		try:
			carte = j[math.floor(OUT[0][0] * len(j))] # != 8 à priori, à checker (et mert', y'a un cas limite... )
		except:
			carte = j[-1] #Cas où la précision sur les float donne len(j).
		main.remove(carte)
		return carte


	def forward_pass(self, IN, W, B):#Passage d'une rangée de neurones à la suivante.
		result = np.dot(W, IN.transpose()).transpose() # - B TODO
		return sigmoid(result)

	def backprop(self, manche): #TODO Attention ! C'est pas en 2D !!!!!
		if self.joueur.index % 2 == manche.winner:
			c = -1 #win -> diminution des pertes
		else:
			c = 1
		for i in range(len(self.ins)):
			IN = self.ins[i]
			HIDDEN = self.hids[i]
			OUT = self.outs[i]
		for k in range(self.DIM_OUT): #H -> O | W
			for l in range(self.NB_HIDDEN):
				MAGIE = 0.9 #TODO
				nab_e_o = OUT[k] * manche.points * c #A à déterminer, en fonction d'un tas de truc, première approx, points de la manche + signe, et c'est peut-etre trop violent la
				nab_o_z = OUT[k] * (1 - OUT[k])
				nab_z_w = HIDDEN[l]
				self.weights2[k][l] = self.weights2[k][l] - MAGIE * (nab_e_o * nab_o_z * nab_z_w)
		for k in range(self.NB_HIDDEN):
			for l in range(self.DIM_IN):
				nab_e_o = 0
				for m in range(self.DIM_OUT):
					nab_e_o += OUT[m] * (1 - OUT[m]) * self.weights2[m][k]
				nab_o_z = HIDDEN[k] * (1 - HIDDEN[k])
				nab_z_w = IN[l]
				self.weights1[k][l] = self.weights1[k][l] - MAGIE * (nab_e_o * nab_o_z * nab_z_w)

	def backpropbis(self, manche): #TODO
		if self.joueur.index % 2 == manche.winner:
			c = -1 #win -> diminution des pertes
		else:
			c = 1
		MAGIE = 0.9 #TODO
		for i in range(len(self.ins)):
			IN = self.ins[i]
			HIDDEN = self.hids[i]
			OUT = self.outs[i]
			nab_E_W2 = (c * manche.points / 162) * ( np.dot((OUT * OUT * (1 - OUT)).transpose(), HIDDEN) ) #Version produit matriciel ultra compact, plus rapide avec numpy. #TODO vérifier si il y a pas un OUT en trop (à priori non)
			self.weights2 -= MAGIE * nab_E_W2
			nab_E_W1 = np.dot((np.dot(OUT * (1 - OUT), self.weights2) * ( HIDDEN * (1 - HIDDEN) )).transpose(), IN) #TODO vérifier s'il manque pas un facteur (s - o) théorique donc un A * o pratique... (à priori oui)
			self.weights1 -= MAGIE * nab_E_W1
        
	def clear(self):
		self.ins = []
		self.outs = []
		self.hids = []

	def end(self, manche):
		self.backpropbis(manche)
		self.clear()


def sqrt_ex(z): #Dérivée infinie en 0... On suppose que ça n'arrive pas et on croise les doigts ? Oué
	a = np.sqrt(np.abs(z))
	for i in range(len(z)):
		for j in range(len(z[i])):
			if a[i][j] != 0:
				a[i][j] *= z[i][j] / np.abs(z[i][j])
	return a

class QNN:

	def __init__(self):
		self.NB_HIDDEN_1 = 100
		self.DIM_IN_1 = 113 #TODO ca va probablement changer
		self.DIM_OUT_1 = 1
		
		self.weights1_1 = np.random.randn(self.NB_HIDDEN_1, self.DIM_IN_1)

		self.weights2_1 = np.random.randn(self.DIM_OUT_1, self.NB_HIDDEN_1)

		self.Qs_1 = []
		self.ins_1 = []
		self.hids_1 = []
		self.outs_1 = []
		
		self.NB_HIDDEN_2 = 410
		self.DIM_IN_2 = 207 #TODO ca va probablement changer
		self.DIM_OUT_2 = 1
		
		self.weights1_2 = np.random.randn(self.NB_HIDDEN_2, self.DIM_IN_2)

		self.weights2_2 = np.random.randn(self.DIM_OUT_2, self.NB_HIDDEN_2)

		self.Qs_2 = []
		self.ins_2 = []
		self.hids_2 = []
		self.outs_2 = []

	def end(self, manche):
		self.backprop_1(manche)
		self.backprop2_2(manche)	

		self.Qs_2 = []
		self.ins_2 = []
		self.hids_2 = []
		self.outs_2 = []
		self.Qs_1 = []
		self.ins_1 = []
		self.hids_1 = []
		self.outs_1 = []

	def generateIN_1(self, manche, main, action):#DIM = 113
		IN = []
		colorValues = {"NoColor" : -1, "pique" : 1, "coeur" : 2, "trefle" : 3, "carreau" : 4}
		cardValues = {"7" : 1, "8" : 2, "9" : 3, "10" : 4, "valet" : 5, "dame" : 6, "roi" : 7, "1" : 8}
		IN.append(self.joueur.index)
		IN.append(action[0])
		IN.append(colorValues[action[1]])
		IN.append(manche.lePremier)
		for k in range(31):
			if k < len(manche.encheresLog):
				IN.append(manche.encheresLog[k][0])
				IN.append(manche.encheresLog[k][1])
				IN.append(colorValues[manche.encheresLog[k][2]])
			else:
				IN.append(0)
				IN.append(0)
				IN.append(0)
		for k in range(8):
			IN.append(cardValues[main[k].valeur])
			IN.append(colorValues[main[k].couleur])
		return IN
	

	def generateIN_2(self, manche, main, action): #on cree le vecteur d'entree du nn ||| len(IN) = 1 + 1 + 31 * 3 + 8 * 5 * 2 + 8 * 2 + 8 * 2 = 207 TODO : Est-ce raisonnable d'utiliser des valeurs = 0 ?
		IN = [action] #Ca retourne un tableau 1D
		colorValues = {"NoColor" : -1, "pique" : 1, "coeur" : 2, "trefle" : 3, "carreau" : 4}
		cardValues = {"7" : 1, "8" : 2, "9" : 3, "10" : 4, "valet" : 5, "dame" : 6, "roi" : 7, "1" : 8}
		IN.append(manche.lePremier)
		for k in range(31): #Encheres TODO, nbre max (en prenant en compte contre et surcontre, + 2?)
			if k < len(manche.encheresLog):
				IN.append(manche.encheresLog[k][0])
				IN.append(manche.encheresLog[k][1])
				IN.append(colorValues[manche.encheresLog[k][2]])
			else:
				IN.append(0)
				IN.append(0)
				IN.append(0)
		for k in range(8): #Les plis
			try:
				test = manche.pliEnCours #Si ca rate, go except
				if k < len(manche.plis):
					IN.append(manche.plis[k][0])
					IN.append(manche.plis[k][1])
					for l in range(4):
						IN.append(cardValues[manche.plis[k][2][l].valeur])
						IN.append(colorValues[manche.plis[k][2][l].couleur])
				elif k == len(manche.plis): #Peut etre le mettre a part (endroit fixe ?) (pli en cours)
					IN.append(manche.joueurs[0].index)
					IN.append(0)
					for l in range(4):
						if l < len(manche.pliEnCours):
							IN.append(cardValues[manche.pliEnCours[l].valeur])
							IN.append(colorValues[manche.pliEnCours[l].couleur])
						else:
							IN.append(0)
							IN.append(0)
				else:
					IN.append(0)
					IN.append(0)
					for l in range(4):
						IN.append(0)
						IN.append(0)
			except:
				IN.append(0)
				IN.append(0)
				for l in range(4):
					IN.append(0)
					IN.append(0)
		for k in range(8):#Main
			if k < len(main):
				IN.append(cardValues[main[k].valeur])
				IN.append(colorValues[main[k].couleur])
			else:
				IN.append(0)
				IN.append(0)
		for k in range(8):#Cartes jouables de la main (TODO, redondant ?) TODO le présenter différemment ?
			try: #Meme feinte que plus haut
				j = cartesJouables(self.joueur, manche)
				if k < len(j):
					IN.append(cardValues[j[k].valeur])
					IN.append(colorValues[j[k].couleur])
				else:
					IN.append(0)
					IN.append(0)
			except:
				IN.append(0)
				IN.append(0)
		return IN

	def feed_forward(self, W, IN):
		N = np.dot(W, IN.transpose()).transpose()
		return sqrt_ex(N)

	def annonce(self, main, manche):
		enchereActuelle = manche.encheresLog[-1]
		m = None
		a = None
		truc = None
		machin = None
		bidule = None
		for k in range(7, 18):
			v = k * 10
			if v >= enchereActuelle[1]:
				for c in ["pique", "carreau", "trefle", "coeur"]:
					IN = np.array([self.generateIN_1(manche, main, [v, c])])
					H = self.feed_forward(self.weights1_1, IN)
					O = self.feed_forward(self.weights2_1, H)
					q = O[0][0]
					if m == None or q > m:
						truc = IN
						machin = H
						bidule = O
						a = [v, c]
						m = q
		self.Qs_1.append(m)
		self.ins_1.append(truc)
		self.hids_1.append(machin)
		self.outs_1.append(bidule)
		return (self.joueur.index, a[0], a[1])
						
	def jouerUneCarte(self, main, manche):
		i = 0
		m = None
		truc = None
		machin = None
		bidule = None
		for k in range(len(main)):#Recherche du meilleur Q issou.
			IN = np.array([self.generateIN_2(manche, main, k + 1)]) #2D
			H = self.feed_forward(self.weights1_2, IN)
			O = self.feed_forward(self.weights2_2, H)
			v = O[0][0]
			if m == None or v > m:#lazy
				m = v
				i = k
				truc = IN
				machin = H
				bidule = O
		self.Qs_2.append(m)
		self.ins_2.append(truc)
		self.hids_2.append(machin)
		self.outs_2.append(bidule)
		carte = main[i]
		main.remove(carte)
		return carte
	
	def train_2(self, IN, T, tour):
		constante = 0.9 #TODO
		nab_E_s = self.outs_2[tour][0][0] - T
		nab_s_z = 1 / (2 * np.abs(self.outs_2[tour][0][0]))
		nab_E_w2 = self.hids_2[tour] * nab_E_s * nab_s_z
		self.weights2_2 -= constante * nab_E_w2
		for k in range(self.NB_HIDDEN_2):
			nab_E_h = self.weights2_2[0][k] * (self.outs_2[tour][0][0] - T) / (2 * np.abs(self.outs_2[tour][0][0]) )
			for l in range(self.DIM_IN_2):
				nab_h_w1 = IN[0][l] / (2 * np.abs(self.hids_2[tour][0][k]))
				nab_E_w1 = nab_E_h * nab_h_w1
				self.weights1_2[k][l] = self.weights1_2[k][l] - constante * nab_E_w1
	
	def train_1(self, IN, T, tour):
		constante = 0.9 #TODO
		nab_E_s = self.outs_1[tour][0][0] - T
		nab_s_z = 1 / (2 * np.abs(self.outs_1[tour][0][0]))
		nab_E_w2 = self.hids_1[tour] * nab_E_s * nab_s_z
		self.weights2_1 -= constante * nab_E_w2
		for k in range(self.NB_HIDDEN_1):
			nab_E_h = self.weights2_1[0][k] * (self.outs_1[tour][0][0] - T) / (2 * np.abs(self.outs_1[tour][0][0]) )
			for l in range(self.DIM_IN_1):
				nab_h_w1 = IN[0][l] / (2 * np.abs(self.hids_1[tour][0][k]))
				nab_E_w1 = nab_E_h * nab_h_w1
				self.weights1_1[k][l] = self.weights1_1[k][l] - constante * nab_E_w1

	def backprop_1(self, manche):
		decalage = np.abs(self.joueur.index - manche.lePremier)
		gamma = 0.8
		if manche.winner == self.joueur.index % 2:
			R = 300
		else:
			R = -300 
		for k in range(len(self.ins_1)):
			try:
				target = gamma * self.Qs_1[k + 1]
			except: #Dernier tour
				target = R
			E = np.abs(target - self.Qs_1[k])
			self.train_1(self.ins_1[k], target, k)
		

	def backprop1_2(self, manche): #Version avec récompense pour les plis.
		gamma = 0.8 #TODO
		for k in range(8):
			R = 0
			q = self.Qs_2[k]
			if k < 7:			
				nq = self.Qs_2[k + 1]
			else:
				nq = 0 #TODO ?? Vraiment 0 ?
				if manche.winner == self.joueur.index % 2:
					R += 300
				else:
					R -= 300	
			pli = manche.plis[k][2]
			t = manche.plis[k][1].index % 2
			if t == self.joueur.index % 2:
				signe = 1
			else:
				signe = -1
			R += signe * compteLesPuntos(pli)
			target = R + gamma * nq
			E = np.abs(target - nq) #L'erreur. (à constante multiplicative près)
			self.train_2(self.ins_2[k], target, k)	

	def backprop2_2(self, manche): #Version avec récompense uniquement sur la victoire.
		gamma = 0.8 #TODO
		for k in range(8):
			R = 0
			q = self.Qs_2[k]
			if k < 7:			
				nq = self.Qs_2[k + 1] # = max(Q(t+1,a))
			else:
				nq = 0 # TODO ?? Vraiment 0 ?
				if manche.winner == self.joueur.index % 2:
					R += 500
				else:
					R -= 500
			target = R + gamma * nq
			E = np.abs(target - q)
			self.train_2(self.ins_2[k], target, k)

class NNFactory: #TODO c'est pratique, quand même
        TYPE_RL = 0
        TYPE_QL = 1
        def __init__(self):
                pass

        


def lesJoueurs():
    j1 = Joueur(0, None, "BOT 0", QNN())
    j2 = Joueur(1, None, "BOT 1 - Sarkis", Sarkis())
    j3 = Joueur(2, j1, "BOT 2 - Sarkis", Sarkis())
    j4 = Joueur(3, j2, "BOT 3 - Sarkis", Sarkis())
    
#   j1 = Joueur(0, None, "Pedro", Human())
#   j2 = Joueur(1, None, "Vanessa", Human())
#   j3 = Joueur(2, j1, "Hilaire", Human())
#   j4 = Joueur(3, j2, "Bruce", Human())

#    j1 = Joueur(0,None, "SolidHaidar", Human())
#    j2 = Joueur(1,None, "S1 - Evry", Sarkis())
#    j3 = Joueur(2, j1, "S2 - McNuggets", Sarkis())
#    j4 = Joueur(3, j2, "S3 - Mangouste", Sarkis())

    j1.partenaire = j3
    j2.partenaire = j4
    return [j1,j2,j3,j4]


def distribution(g4m3rz,PAKET): 
     for k in range(4):
        g4m3rz[k].main = PAKET.cartes[8*k:8*(k+1)]

def getEnchere(encher, g):
    print(encher[1])
    ench = input("Nouvelle enchère")
    if ench == "Passe":
        return encher
    joueur=input("c ki?")
    couleur=input("pik/keur/karo/trefl")
    return (g[int(joueur)],int(ench),couleur)

class PasseException(Exception):
	def __init__(self):
		pass

def encheres(joueurs, manche, premier): #TODO, contre, surcontre, (capot generalise ?), redistribution
    manche.lePremier = premier #TODO c'est moche !
    passe = 0
    capot = passe
    rustine = False
    enchereActuelle = (-1, 70 , "NoColor") #( id, montant, couleur )
    encheresLog = [enchereActuelle]
    manche.encheresLog = encheresLog
    i = premier #TODO
    while (passe != 3 and capot == False):
        enchereDuJoueur = joueurs[i].annoncer(manche)
        if enchereDuJoueur[1] == enchereActuelle[1]:
            passe += 1
            if passe == 3 and enchereDuJoueur == (-1, 70 , "NoColor") and rustine == False: #TODO Rustine. Urgent.
                passe = 2 #Grosso modo, c'est pour le cas 4 passes
                rustine = True
        else:
            passe = 0
        if enchereDuJoueur[1] == 170:
            capot = True
        enchereActuelle = enchereDuJoueur
        encheresLog.append(enchereDuJoueur)
        i += 1
        if i == 4:
            i = 0
    manche.atout = encheresLog[-1][2]
    manche.enchere = encheresLog[-1]
    if manche.enchere[2] == "NoColor":
        raise PasseException

def uneCarte(g):
    ncarte = input("Quelle carte jouer ?")
    carte = g.main[int(ncarte)]
    g.main.remove(carte)
    return carte

def lejeu(joueurs, manche, premier):
    tour = 1
    plis1 = []
    plis2 = []

    
    while tour <= 8:
        #print('-'*20)
        #print("\n")
        cartesdutour = []
        manche.pliEnCours = cartesdutour
        manche.quiCommence = joueurs[premier].index
        manche.couleurdemandee = "NoColor"
        k = premier
        for machin in range(4):
            
            carte = joueurs[k].jouer(manche)
            #print(joueurs[k].name)
            #print(carte)
            #print("\n")
            if manche.couleurdemandee == "NoColor":
                manche.couleurdemandee = carte.couleur
            cartesdutour.append(carte)
            k += 1
            if k == 4:
                k = 0

        m = cartesdutour[0]
        i = 1
        j = 0
        while i <= 3:
            if cartesdutour[i] > m:
                m = cartesdutour[i]
                j = i
            i += 1
        if j % 2 == 0:
            plis2.append(cartesdutour)
        else:
            plis1.append(cartesdutour)
        manche.plis.append((joueurs[premier].index, j, cartesdutour)) #Joueur qui a commencé, Joueur qui a gagné le pli, cartes.
        premier = j
        tour += 1
    nj = manche.enchere[1] #Qui a pris ?
    #TODO, section expérimentale
    points = compteLesPuntos(plis1)
    if manche.plis[-1][1]%2 == 1:
        points+=10
    
    if nj % 2 == 0:
        if 162 - points >= manche.enchere[1]:
            manche.winner = 0
            manche.points = 162 - points
        else:
            manche.winner = 1
            manche.points = points
    else:
        if points >= manche.enchere[1]:
            manche.winner = 1
            manche.points = points
        else:
            manche.winner = 0
            manche.points = 162 - points
    for j in joueurs:
        j.end(manche)

def compteLesPuntos(desPlis):
    value = 0
    for plis in desPlis:
        for carte in plis:
            value += carte.value()
    return value

#TODO, cartesJouables(main, manche).

def cartesALaCouleur(tab, couleur):
    a = []
    for c in tab:
        if c.couleur == couleur:
            a.append(c)
    return a

def maxPli(pli): #Donne l'index de la carte maitresse
    if len(pli) == 0: #Ne sert jamais... En theorie
        return None
    m = pli[0]
    for c in pli:
        if c > m:
            m = c
    return m

def indexMaxPli(pli):
    m = pli[0]
    i = 0
    j = 0
    for c in pli:
        if c > m:
            m = c
            j = i
        i += 1
    return j

def minPliALaCouleur(pli,couleur):
    if len(pli) == 0:
        return None
    m = pli[0]
    for c in pli:
        if c < m and c.couleur == couleur:
            m = c
    if m.couleur != couleur:
        return None
    return m


def maxPliALaCouleur(pli, couleur): #Renvoie la carte la plus forte du pli à la couleur demandée, ie. de la couleur de la première carte. (Il ne faut donc pas l'utiliser avec une AUTRE couleur, la fonction est mal posée).
    if len(pli) == 0: #Dans mon implémentation, n'arrive jamais. Donc si ça plante ici, c'est probablement Benjamin...
        return None
    m = pli[0]
    for c in pli:
        if c > m and c.couleur == couleur:
            m = c
    return m

def cartesAuDessusALaCouleur(j, pli, couleur): #Renvoie les cartes supérieures au max du pli dans la couleur demandée, ie. non nécessairement de la couleur de la première carte.
    a = []
    m = maxPliALaCouleur(pli, couleur)
    for c in cartesALaCouleur(j.main, couleur):
        if c > m:
            a.append(c)
    return a

def cartesJouables(j, manche): #TODO nettoyer j.
    if manche.couleurdemandee == "NoColor": #Si tu commences.
        return j.main
    if len(cartesALaCouleur(j.main, manche.couleurdemandee)) != 0: #Si tu ne commences pas et que tu as de la couleur demandée
        if manche.couleurdemandee == manche.atout: #Si de l'atout est demandé
            cadalc = cartesAuDessusALaCouleur(j, manche.pliEnCours, manche.atout)
            if len(cadalc) != 0: #Si tu as des atouts supérieurs
                return cadalc #Tu dois jouer un atout supérieur
            else:
                return cartesALaCouleur(j.main, manche.atout) #Tu joues de l'atout
        else:
            return cartesALaCouleur(j.main, manche.couleurdemandee) #Si de l'atout n'est pas demandé, tu joues des cartes de la couleur demandée.
    else: #Si tu n'as pas la couleur demandée.
        if len(cartesALaCouleur(j.main, manche.atout)) == 0: #Si tu n'as pas d'atout
            return j.main #Tu joues n'importe quoi.
        else: #Si tu as de l'atout
            if indexMaxPli(manche.pliEnCours) == len(manche.pliEnCours) - 2: # Mon partenaire est maitre (et ca commence à 0)
                return j.main #Tu joues n'importe quoi.
            else: #Si ton partenaire n'est pas maitre.
                if len(cartesAuDessusALaCouleur(j, manche.pliEnCours, manche.atout)) != 0: #Si (de l'atout a été joué et que tu as des atouts supérieurs) OU (pas d'atout joué)
                    return cartesAuDessusALaCouleur(j, manche.pliEnCours, manche.atout) #Tu joues (un atout supérieur) OU (de l'atout)
                else: #Si il y a eu de l'atout et que tu n'as pas au-dessus
                    return cartesALaCouleur(j.main, manche.atout) #Tu joues de l'atout (sous-entendu, tu 'pisses')                    



def fitness(joueur,n=1000): #Win rate against Sarkis Team. (En théorie, ça peut faire 0 partie, lol).
	temp = joueur.index
	wins = 0
	j1 = Joueur(1, None, "S0", Sarkis())
	j2 = Joueur(2, None, "S1", Sarkis())
	j3 = Joueur(3, j1, "S2", Sarkis())
	joueur.index = 0
	joueur.partenaire = j2
	j1.partenaire = j3
	j2.partenaire = joueur
	js = [joueur, j1, j2, j3]
	for k in range(n):
		manche = Manche(js)
		p = createDeck(manche)
		manche.pack = p
		distribution(js, p)
		passe = False
		try:
			encheres(js, manche, k % 4)
		except PasseException as pe:
			passe = True
			n -= 1
		if passe == False:
			lejeu(js, manche, k % 4)
			if manche.winner == joueur.index%2:
				wins += 1
	joueur.index = temp
	return wins / n

##
#g = lesJoueurs()
#for t in range(1):
#	manche = Manche(g)
#	p = createDeck(manche)
#	manche.pack = p
#	distribution(g, p)
#	flag = False
#	try:
#		encheres(g, manche)
#	except:
#		print("4 passes")
#		flag = True
#	if not flag:	
#		lejeu(g, manche)


def training(num):
	g = lesJoueurs()
	fitnessLog = []
	for t in range(1000000): #Training
		if t % 50000 == 0:
			temp = [t]
			for k in g:
				f = fitness(k)
				temp.append((k.index, f))
			fitnessLog.append(temp)
		gc.collect()
		print(t)
		manche = Manche(g)
		p = createDeck(manche)
		manche.pack = p
		distribution(g, p)
		passe = False
		try:
			encheres(g, manche, t % 4)
		except PasseException as pe:
			passe = True
		if passe == False:
			lejeu(g, manche, t % 4)
	pack(fitnessLog, "FITNESS - TEST NO " + str(num) + ".tipe")
	pack(g, "JOUEURS - TEST NO " + str(num) + ".tipe")


#TODO passer le t % 4 en interne !

#Foot notes : Un seul Sarkis est nécessaire dans l'absolu => On peut encore optimiser en lui passant plusieurs mains.
# TEST NO 1 - 4 NNL en renforcement - 205/410/2 - 10E6 games "Vanilla" | Résultat : 8% de winrate au mieux. Bof... On remarque quand même que le winrate est croissant !
# TEST NO 2 - 1 NNL + 3 SARKIS - 205/410/2 - 10E6 games (Notes : juste après que Benjamin a modifié le code...) | Résultat : 6% de winrate à t = 0, puis environ 45% à t = 50000, puis environ 45% tout le temps. (PS : Le fichier est vachement lourd... TODO trouver pourquoi)
# TEST NO 3 - NNL/SARKIS VS NNL/SARKIS - 205/410/2 - 10E6 games | Résultats très inégaux, vraisemblablement dû au fait que les mains ne tournent pas (et au milliard d'erreurs dans le code)
#Notes : jusque là tests avec code impropre.
#A partir de là, Benjamin a touché à la relation d'ordre...
#A partir d'ici, plein de corrections ont été faites. Code pseudo-correct.
# TEST NO 4 - 1 QNN + 3 SARKIS - 10E6 games. | On remarque que c'est VRAIMENT très très lent, vivement la version produit matriciel.

