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
        self.devine = [[k,1/3,1/3,1/3] for  k in manche.pack ] #TODO , generer
        self.strategie=""
        self.flag=True  #TODO reinitialiser dans les annonces
    
    def annonce(self, main, manche):
        pass

    def jouerUneCarte(self, main, manche):
        if self.flag:
                if manche.encheres[0]%2 == self.index%2:
                        self.strategie = "atk"
                else:
                        self.strategie="def"
                flag=False
        for i in manche.plis[-1][2]:
                self.devine[i] = [0,0,0,0]
        for i in manche.pliEnCours:
                self.devine[i] = [0,0,0,0]
        couleur = manche.plis[-1][2][0].couleur
        for i in range(1,4):
                 if manche.plis[-1][2][i].couleur != couleur:
                         for k in self.paketo:
                                if k.couleur == couleur:
                                        self.devine[k][i] = 0
        if len(manche.pliEnCours) >= 2:
                couleur = manche.pliEnCours[0].couleur
                for i in range(1,4):
                         if manche.pliEnCours[i].couleur != couleur:
                                 for k in self.paketo:
                                        if k.couleur == couleur:
                                                self.devine[k][i] = 0
                
        a=self.plimaitre(main,manche)
        if self.strategie=="atk":
                if manche.couleurdemandee =="NoColor":
                        if ilrestedesatouts(self,main)==0:
                                for k in a[:-1]:
                                        if k.couleur == manche.atout:
                                                return k
                                return minPliALaCouleur(main,manche.atout)
                        else:
                                if len(a)>1:
                                        return a[0]
                                else: #Remove
                                        return self.goodplay(main,manche)
                else:
                        if len(manche.pliEnCours)==1:
                            return min(cartess)
                        elif len(manche.pliEnCours)==2:
                                if manche.couleurdemandee!=manche.atout:
                                        flag=True
                                        cartpart=manche.pliEncours[-2]
                                        for k in self.paketo:
                                                if k.couleur!=manche.atout and self.devine[(self.index+3)%4]!=0:
                                                        flag = flag and cartpart>manche.pliEnCours[-1] and cartpart>k
                                else:
                                        flag=True
                                        cartpart=manche.pliEncours[-2]
                                        for k in self.paketo:
                                                if self.devine[(self.index+3)%4]!=0:
                                                        flag = flag and cartpart>manche.pliEnCours[-1] and cartpart>k
                        else:
                                cartpart=manche.pliEnCours[-2]
                                flag=(cartpart==max(manche.pliEnCours))
                                                
                                                
##                        if flag:
##                                b = self.plimaitre(cartess, manche)#je=zjeêaijêirjiaJONEOFNâoUNROunôdnezUONôfun$FONÖUDNzind$iFN£
##                                b = b[:-1]
##                                if b!=[]:
##                                        cartess= np.intersect1d(cartess, b)
##                                        return max(pliALaCouleur(cartess,self.manche.pliEnCours))
##                                else:
##                                        return min(pliALaCouleur(cartess,self.manche.pliEnCours
                                                #return min(cartess
                                       #elif indexMaxPli(manche.pliEnCours) == (self.index + 2) % 4:
                                       
                                
                                
##    def goodplay(self, main, manche):
##        flag = False
##        a = []
##        for k in main:
##                if k.couleur != manche.atout:
##                        a.append(k)
##        if a != []:
##                return random.choice(a)
##        return random.choice(main)

    def ilrestedezatouts(self, main, manche,nbatout):
        c=0
        for k in self.paketo:
                
                if k.couleur == manche.atout and self.devine[k][(self.index+1)%4] != 0 and self.devine[(self.index+3)%4]== 0:
                        c+=1
        return c

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
    j1 = Joueur(0, None, "BOT 0", NNLBot())
    j2 = Joueur(0, None, "BOT 1", NNLBot())
    j3 = Joueur(0, None, "BOT 2", NNLBot())
    j4 = Joueur(0, None, "BOT 3", NNLBot())
    
##    j1 = Joueur(0, None, "Pedro", Human())
##    j2 = Joueur(1, None, "Chantal", Human())
##    j3 = Joueur(2, j1, "Roger", Human())
##    j4 = Joueur(3, j2, "Goya", Human())
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
        #print(enchereDuJoueur)
        #print("\n")
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
    #print(manche.enchere)
    assert manche.enchere != (-1, 70, "NoColor")

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
        #print('-'*20)
        #print("\n")
        cartesdutour = []
        manche.pliEnCours = cartesdutour
        manche.quiCommence = joueurs[0].index
        manche.couleurdemandee = "NoColor"
        for k in joueurs:
            carte = k.jouer(manche)
            #print(carte)
            #print("\n")
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
        manche.plis.append((joueurs[0].index, j, cartesdutour))
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
    #print(manche.winner)
    #print(manche.points)

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
                



g = lesJoueurs()
for t in range(1000000): #Training
    gc.collect()
    print(t)
    manche = Manche(g)
    p = createDeck(manche)
    manche.pack = p
    distribution(g, p)
    #for k in g:
         #print(k.main)
         #print("\n")
    try:
        encheres(g, manche)
        lejeu(g, manche)
        for k in g:
            k.JAIPADENOM.backpropbis(manche)
            k.JAIPADENOM.clear()
    except:
        pass
pack(g, "BOT V1.tipe")
