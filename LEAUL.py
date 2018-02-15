#import socket
import random
import math
import numpy as np
import pickle
import gc
gc.enable()

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

def send(text):
    s.send(text)

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
        #print("tour de : " + self.name)
        return self.JAIPADENOM.jouerUneCarte(self.main, manche)

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
        self.start=True
        self.monannonce='NoColor'

    def end(self, gagnant, points):
        self.start = True
    
    def debut(self,main,manche):
        self.paketo = manche.pack
        self.devine = {}
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
        if self.start:
            self.debut(main,manche)
            self.start=False
        self.dico={}
        self.appel={}
        for couleur in ["coeur","carreau","pique","trefle"]:
            manche.atout=couleur
            self.o=self.plimaitre(main,manche)
            self.o.append(self.atout_main(main,manche))
            self.dico[couleur]=self.o
        for couleur in ["coeur","carreau","pique","trefle"]:
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
        self.theappel = (self.appel["coeur"],"coeur")
        for couleur in ["carreau","pique","trefle"]:
            if self.appel[couleur] >= self.theappel[0]:
                self.theappel = (self.appel[couleur], couleur)
        if len(manche.encheresLog)>=3:
            if manche.encheresLog[-2][2]!=self.monannonce and manche.encheresLog[-2][0]%2==self.joueur.index:
                if manche.encheresLog[-2][0]!=self.joueur.index:
                    manche.atout=manche.encheresLog[-2][2]
                    b=self.plimaitre(main,manche)
                
                    self.encherepart=manche.encheresLog[-2][1]
                    self.encherepart+=10*(len(b))
                    if self.theappel[0]<=self.encherepart:
                        self.theappel=(self.encherepart,manche.atout)
        if manche.encheresLog[-1][1]<self.theappel[0]:
            self.monannonce=self.theappel[1]
            return(self.joueur.index,)+(self.theappel)
        else:
            return manche.encheresLog[-1]

    def plimaitre(self,main,manche):
        try:
            self.zob=manche.couleurdemandee
        except:
            self.zob="rien"
        self.plimaitres=[]
        for k in main:
            self.A=True
            for i in self.paketo.cartes:
            
                if k.couleur==i.couleur and i not in main:
                    manche.couleurdemandee=k.couleur
                    self.A= self.A and k>i
            if self.A:
                self.plimaitres.append(k)
        manche.couleurdemandee=self.zob
        return self.plimaitres
        
    def jouerUneCarte(self, main, manche):
        if self.ilrestedezatouts(manche)==0:
            self.strategie="atk"
            
        if self.flag:
            if manche.enchere[0]%2 == self.joueur.index%2:
                self.strategie = "atk"
            else:
                self.strategie="def"
            self.flag=False
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
        self.untableau=[]
        self.cartatou=cartesALaCouleur(main,manche.atout)    
        
        
        if manche.couleurdemandee =="NoColor":
            if self.strategie=="atk" and  self.ilrestedezatouts(manche)!=0 and self.cartatou!=[]:
                for k in self.materpli[:-1]:
                    if k.couleur == manche.atout:
                        main.remove(k)
                        return k
                j = minPliALaCouleur(main,manche.atout)
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
        couleur=input("pik/keur/karo/trefl")
        return (self.joueur,int(ench),couleur)

    def jouerUneCarte(self, main, manche):
        print(main)
        print("Cartes jouables :")
        print(cartesJouables(self.joueur, manche))
        ncarte = input("Quelle carte jouer ?")
        carte = main[int(ncarte)] #TODO Pick among playable cards
        main.remove(carte)
        return carte

def sigmoid(z): #sigmoid function, faut peut-être l'étaler... z / alpha, alpha > 1, alpha(z);
        return 1 / ( 1 + np.exp(-1 * np.clip(z, -35, 35)))

class NNLBot:
    def __init__(self):
        self.NB_HIDDEN = 410
        self.DIM_IN = 205 #TODO ca va probablement changer
        self.DIM_OUT = 2 # 3 ?
        
        self.weights1 = np.random.randn(self.NB_HIDDEN, self.DIM_IN)
        self.bias1 = np.random.randn(self.NB_HIDDEN, 1)

        self.weights2 = np.random.randn(self.DIM_OUT, self.NB_HIDDEN)
        self.bias2 = np.random.randn(self.DIM_OUT, 1)
        self.ins = []
        self.hids = []
        self.outs = []

    def generateIN(self, manche, main): #on cree le vecteur d'entree du nn ||| len(IN) = 31 * 3 + 8 * 5 * 2 + 8 * 2 + 8 * 2 = 205
        IN = []
        colorValues = {"NoColor" : -1, "pique" : 0, "coeur" : 1, "trefle" : 2, "carreau" : 3}
        cardValues = {"7" : 0, "8" : 1, "9" : 2, "10" : 3, "valet" : 4, "dame" : 5, "roi" : 6, "1" : 7}
        for k in range(31): #Encheres TODO, nbre max (en prenant en compte contre et surcontre, + 2?)
            if k < len(manche.encheresLog):
                try: #TODO, déberkifier
                    IN.append(manche.encheresLog[k][0].index)
                except:
                    IN.append(-1)
                IN.append(manche.encheresLog[k][1])
                IN.append(colorValues[manche.encheresLog[k][2]])
            else:
                IN.append(-1)
                IN.append(-1)
                IN.append(-1)
        for k in range(8):
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
                    IN.append(-1)
                    for l in range(4):
                        if l < len(manche.pliEnCours):
                            IN.append(cardValues[manche.pliEnCours[l].valeur])
                            IN.append(colorValues[manche.pliEnCours[l].couleur])
                        else:
                            IN.append(-1)
                            IN.append(-1)
                else:
                    IN.append(-1)
                    IN.append(-1)
                    for l in range(4):
                        IN.append(-1)
                        IN.append(-1)
            except:
                IN.append(-1)
                IN.append(-1)
                for l in range(4):
                    IN.append(-1)
                    IN.append(-1)
        for k in range(8):
            if k < len(main):
                IN.append(cardValues[main[k].valeur])
                IN.append(colorValues[main[k].couleur])
            else:
                IN.append(-1)
                IN.append(-1)
        for k in range(8):
            try: #Meme feinte que plus haut
                j = cartesJouables(self.joueur, manche)
                if k < len(j):
                    IN.append(cardValues[j[k].valeur])
                    IN.append(colorValues[j[k].couleur])
                else:
                    IN.append(-1)
                    IN.append(-1)
            except:
                IN.append(-1)
                IN.append(-1)
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
        return (self.joueur, v, c)
        
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

    def backprop(self, manche): #TODO
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
            nab_E_W2 = (c * manche.points / 162) * ( np.dot((OUT * OUT * (1 - OUT)).transpose(), HIDDEN) ) #Version produit matriciel ultra compact, plus rapide avec numpy.
            self.weights2 -= MAGIE * nab_E_W2
            nab_E_W1 = np.dot((np.dot(OUT * (1 - OUT), self.weights2) * ( HIDDEN * (1 - HIDDEN) )).transpose(), IN)
            self.weights1 -= MAGIE * nab_E_W1
        
    def clear(self):
        self.ins = []
        self.outs = []
        self.hids = []

class NNFactory:
        TYPE_RL = 0
        TYPE_QL = 1
        def __init__(self):
                pass

        


def lesJoueurs():
#    j1 = Joueur(0, None, "BOT 0", NNLBot())
#    j2 = Joueur(0, None, "BOT 1", NNLBot())
#    j3 = Joueur(0, j1, "BOT 2", NNLBot())
#    j4 = Joueur(0, j2, "BOT 3", NNLBot())
    
#   j1 = Joueur(0, None, "Pedro", Human())
#   j2 = Joueur(1, None, "Chantal", Human())
#   j3 = Joueur(2, j1, "Roger", Human())
#   j4 = Joueur(3, j2, "Goya", Human())

    j1 = Joueur(0,None, "S0", Sarkis())
    j2 = Joueur(1,None, "S1", Sarkis())
    j3 = Joueur(2, j1, "S2", Sarkis())
    j4 = Joueur(3, j2, "S3", Sarkis())

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

def encheres(joueurs, manche): #TODO, contre, surcontre, (capot generalise ?)
    passe = 0
    capot = passe
    enchereActuelle = (-1, 70 , "NoColor") #( id, montant, couleur )
    encheresLog = [enchereActuelle]
    manche.encheresLog = encheresLog
    i = 0 #TODO
    while (passe != 3 and capot == False): #Redistribution + 4 passes TODO
        enchereDuJoueur = joueurs[i].annoncer(manche)
        print(enchereDuJoueur)
        print("\n")
        if enchereDuJoueur[1] == enchereActuelle[1]:
            passe += 1
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
        raise Exception

def uneCarte(g):
    print("Le tour du joueur : " + g.name)
    print(g.main)
    ncarte = input("Quelle carte jouer ?")
    carte = g.main[int(ncarte)]
    g.main.remove(carte)
    return carte

def lejeu(joueurs, manche):
    tour = 1
    plis1 = []
    plis2 = []
    while tour <= 8:
        print('-'*20)
        print("\n")
        cartesdutour = []
        manche.pliEnCours = cartesdutour
        manche.quiCommence = joueurs[0].index
        manche.couleurdemandee = "NoColor"
        for k in joueurs:
            carte = k.jouer(manche)
            print(carte)
            print("\n")
            if manche.couleurdemandee == "NoColor":
                manche.couleurdemandee = carte.couleur
            cartesdutour.append(carte)
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
        manche.plis.append((joueurs[0].index, j, cartesdutour)) #Joueur qui a commencé, Joueur qui a gagné le pli, cartes.
        joueurs = joueurs[j:] + joueurs[0:j]
         # Benjamin-proof
        tour += 1
    nj = manche.enchere[1] #Qui a pris ?
    #TODO, section expérimentale
    points = compteLesPuntos(plis1)
    
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
    for k in joueurs:
        k.JAIPADENOM.end(manche.winner, manche.points) #TODO NN
    print(manche.winner)
    print(manche.points)

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

def maxPli(pli):
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
    return m


def maxPliALaCouleur(pli, couleur):
    if len(pli) == 0:
        return None
    m = pli[0]
    for c in pli:
        if c > m and c.couleur == couleur:
            m = c
    return m

def cartesAuDessusALaCouleur(j, pli, couleur):
    a = []
    m = maxPliALaCouleur(pli, couleur)
    for c in cartesALaCouleur(j.main, couleur):
        if c > m:
            a.append(c)
    return a

def cartesJouables(j, manche):
    if manche.couleurdemandee == "NoColor":
        return j.main
    if len(cartesALaCouleur(j.main, manche.couleurdemandee)) != 0:
        if manche.couleurdemandee == manche.atout:
            cadalc = cartesAuDessusALaCouleur(j, manche.pliEnCours, manche.atout)
            if len(cadalc) != 0:
                return cadalc
            else:
                return cartesALaCouleur(j.main, manche.atout)
        else:
            return cartesALaCouleur(j.main, manche.couleurdemandee)
    else:
        if len(cartesALaCouleur(j.main, manche.atout)) == 0:
            return j.main
        else:
            if indexMaxPli(manche.pliEnCours) == len(manche.pliEnCours) - 2: # Mon partenaire est maitre (et ca commence à 0)
                return j.main
            else:
                if len(cartesAuDessusALaCouleur(j, manche.pliEnCours, manche.atout)) != 0:
                    return cartesAuDessusALaCouleur(j, manche.pliEnCours, manche.atout)
                else:
                    return j.main #C est bizarre, mais c est les regles.                       



def fitness(joueur): #Win rate against Sarkis Team.
	wins = 0
	n = 30
	for k in range(30):
		j1 = Joueur(0, None, "S0", Sarkis())
		j2 = Joueur(1, None, "S1", Sarkis())
		j3 = Joueur(2, j1, "S2", Sarkis())
		joueur.index = 3
		joueur.partenaire = j2
		
		j1.partenaire = j3
		j2.partenaire = joueur
		g = [j1, j2, j3, joueur]
		manche = Manche(g)
		p = createDeck(manche)
		manche.pack = p
		distribution(g, p)
		try:
			encheres(g, manche)
			lejeu(g, manche)
			if manche.winner % 2 == 0:
				wins += 1
		except:
			n -= 1
	return wins / n


##Side note à la volée : Approximation de l'algo de Qlearning grâce à un réseau de neurones
##Le but est de fournir une approximation de la fonction Q (obviously)
##On décide de comment jouer par une simple recherche de max sur Q, après ça.


##
g = lesJoueurs()
for t in range(50):
	manche = Manche(g)
	p = createDeck(manche)
	manche.pack = p
	distribution(g, p)
	flag = False
	try:
		encheres(g, manche)
	except:
		print("4 passes")
		flag = True
		for k in g:#Scotch TOD
			k.JAIPADENOM.end(1,4)
	if not flag:	
		lejeu(g, manche)
#for t in range(1000000): #Training
#    gc.collect()
#    print(t)
#    manche = Manche(g)
#    p = createDeck(manche)
#    manche.pack = p
#    distribution(g, p)
    #for k in g:
         #print(k.main)
         #print("\n")
#    try:
#        encheres(g, manche)
#        lejeu(g, manche)
#        for k in g:
#            k.JAIPADENOM.backpropbis(manche)
#            k.JAIPADENOM.clear()
#    except:
#        pass
#pack(g, "BOT V1.tipe")
