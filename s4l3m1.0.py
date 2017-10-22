import socket
import random

#s = socket.socket()
#s.connect(("localhost", 4321))

class Manche: #Sert a stocker des trucs

    def __init__(self, joueurs):
        self.joueurs = joueurs

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
        print("TU DU DU")

def paké(manche):        
    preskpak = []
    for k in ["7","8","9","10","valet","dame","roi","1"]:
        for l in ["Keur", "KARO", "PIK", "Tref"]:
            preskpak.append(Carte(k,l, manche))

    PAKET = Deck(preskpak)
    PAKET.everydayImShufflin()
    return PAKET

class Joueur:
    def __init__(self, index, koping, namae, JAIPADENOM):
        self.index = index
        self.main = []
        self.koping = koping
        self.name = namae
        self.JAIPADENOM = JAIPADENOM #Strategy Pattern déguisé

    def annoncer(self, onch, manche):
        return self.JAIPADENOM.annonce(onch, manche)

    def jouer(self, atout, demande, pliEncours):
        print("tour de : " + self.name)
        return self.JAIPADENOM.jouerUneCarte(self.main, atout, demande, pliEnCours)

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
        self.devine = [(k,1/3,1/3,1/3) for  k in manche.pack ] #TODO , generer
    
    def annonce(self, onch, manche):
        pass

    def jouerUneCarte(self, main, atout, demande, pliEnCours):
        if manche.enchere[0] % 2 == self.index % 2:
            if demande == "Zob":
                if self.
            

class Human:
    def __init__(self):
        pass

    def annonce(self, onch, manche):
        ench = input("Nouvelle enchère")
        if ench == "Passe":
            return onch[-1]
        couleur=input("pik/keur/karo/trefl")
        return (self,int(ench),couleur)

    def jouerUneCarte(self, main, atout, demande, pliEnCours):
        print(main)
        ncarte = input("Quelle carte jouer ?")
        carte = main[int(ncarte)]
        main.remove(carte)
        return carte

def lesG4m3rz():
    j1 = Joueur(0, None, "Pedro", Human())
    j2 = Joueur(1, None, "Chantal", Human())
    j3 = Joueur(2, j1, "Roger", Human())
    j4 = Joueur(3, j2, "Goya", Human())
    j1.koping = j3
    j2.koping = j4
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

def lézencher(g, manche):
    toutlmondapasse = 0
    capote = toutlmondapasse
    encher=(0, 79 , "NoColor")
    onch = []
    i = 0
    while toutlmondapasse != 3 and capote == False:
        onchdunjoueur = g[i].annoncer(onch, manche)
        if onchdunjoueur[1] == encher[1]:
            toutlmondapasse += 1
        else:
            toutlmondepasse = 0
        if onchdunjoueur[1] == 170:
            capote = True
        encher = onchdunjoueur
        onch.append(onchdunjoueur)
        i += 1
        if i == 4:
            i = 3
    manche.atout = onch[-1][2]
    manche.enchere = onch[-1]

def uneCarte(g):
    print("Le tour du joueur : " + g.name)
    print(g.main)
    ncarte = input("Quelle carte jouer ?")
    carte = g.main[int(ncarte)]
    g.main.remove(carte)
    return carte

def lejeu(g, manche):
    tour = 1
    plis1 = []
    plis2 = []
    while tour <= 8:
        cartesdutour = []
        couleurdemandee = "Zob"
        for k in g:
            #carte = uneCarte(k) # A faire pour chaque joueur, TODO
            carte = k.jouer(manche.atout, couleurdemandee, cartesdutour)
            if couleurdemandee == "Zob":
                manche.couleurdemandee = carte.couleur
            cartesdutour.append(carte)
        m = cartesdutour[0]
        i = 1
        j = 0
        while i <= 3:
            print(cartesdutour[i] > m)
            if cartesdutour[i] > m:
                m = cartesdutour[i]
                j = i
            i += 1
        print(j)
        if j % 2 == 0:
            plis2.append(cartesdutour)
        else:
            plis1.append(cartesdutour)
        g=g[j:]+g[0:j]
         # Benjamin-proof
        tour += 1
    nj = manche.enchere[1]
    if nj % 2 == 0:
        if compteLesPuntos(plis2) >= manche.enchere[1]:
            print("GG")
        else:
            print("Bande de merdes!")
    else:
        if compteLesPuntos(plis1) >= manche.enchere[1]:
            print("Idem")
        else:
            print("Bande de merdeux !")

def compteLesPuntos(desPlis):
    value = 0
    for plis in desPlis:
        for carte in plis:
            value += carte.value()
    return value

g = lesG4m3rz()

manche = Manche(g)
p = paké(manche)
manche.pack = p
distribution(g, p)
for k in g:
    print(k.main)
lézencher(g, manche)
lejeu(g, manche)


