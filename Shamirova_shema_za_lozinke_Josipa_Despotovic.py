# Student : Josipa Despotović
# Diplomski rad : Metode podjele tajni
# studeni 2020.godine
#
# Implementacija Shamirove sheme podjele tajni u generiranju i rekonstrukciji lozinke

import random

# Pomoćne funkcije : definirat ćemo funkcije koje nam pomažu u koracima generiranja
#                    i rekonstruiranja LOZINKE

# Kako bi izbjegli računanje sa prevelikim brojevima, uvest ćemo neka ograničenja.

# LOZINKA : - mora biti niz znakova, velikih slova (eng.abecede) i/ili brojeva 0-9
#           - duljina mora biti između 4-8
#           - ne smije sadržavati razmake

def provjeraLozinke(lozinka):
    if(len(lozinka) < 4 or len(lozinka) > 8):
        lozinka = ""
    else:
        for znak in lozinka:
            if(ord(znak) < 48 or (ord(znak) > 57 and ord(znak) < 65) or ord(znak) > 90):
                lozinka = ""
    return lozinka

# Definiramo funkciju koja će maskirati unesenu lozinku na način da :
# - generira tajni pomak ( nasumičan broj između 0-9, uključujući krajeve)
# - svakom znaku u lozinci pridruži odgovarajući ASCII kod
# - svakom ASCII kodu svakog znaka pridoda tajni pomak
# - dobivenu maskiranu lozinku dalje dijeli po Shamirovoj shemi

def split(word): 
    return [char for char in word]

def maskirajLozinku(lozinka):
    pomak = random.randint(0,9)
    niz_simbola = split(lozinka)
    rez = []
    for el in niz_simbola:
        temp = ord(el) + pomak
        rez.append(str(temp))
    return [int("".join(rez)),pomak] #funkcija nam vraća maskiranu lozinku i tajni pomak koji je poznat samo djelitelju tajne


# Dobivena maskirana lozinka je neki pozitivan cijeli broj te ćemo prema njemu generirati prosti broj p
# kako bi provodili daljnji račun u Zp.
# Za odabir prostog broja p uzet ćemo prvi prosti broj veći od lozinke.

def isPrime(n):
    """
    Pretpostavljamo da je n prirodan broj
    """
    # Znamo da 1 nije prost broj
    if n == 1:
        return False

    i = 2
    # Petlja se vrti od 2 do int(sqrt(x)) 
    while i*i <= n:
        # Provjera da li i dijeli x bez ostatka
        if n % i == 0:
            # To znači da n ima faktor između 2 i sqrt(n)
            # Stoga nije prost broj
            return False
        i += 1
    # Ako nismo pronašli nijedan faktor u gornjoj petlji
    # onda je n prost broj
    return True

def generirajProsti_p(lozinka):
    prosti = lozinka + 1
    while(isPrime(prosti) != True):
        prosti = prosti + 1
    return prosti

# Odaberimo n različitih ne-nul elemenata iz Zp, u oznaci x_i
def random_Xi(n,prost):
    lista = []
    for i in range(0,n):
        lista.append(random.randint(0,prost))
    return lista

# Odaberimo t-1 elemenata iz Zp u oznaci a_i
def random_Ai(t, prost):
    lista = []
    for i in range(0,t-1):
        lista.append(random.randint(0,prost))
    return lista

# Pomoću polinoma za izabrane x_i i a_i, generiramo pripadne vrijednosti y_i
def a_Funkcija(lozinka,t,x_i,a_i,p): # polinom a(x) = K + sum_{j=1}^{t-1} a_j * x^j mod(p)
    rez_yi = []
    for x in x_i: # prvo odredimo sumu iz polinoma a(x)
        suma = 0
        for i in range(1,t):
            suma += a_i[i-1]*pow(x,i)
        rez_yi.append((lozinka+suma)%p)
    return rez_yi

# Generirajmo dijelove tako da budu oblika [x1,y1],...[xn,yn]
def generirajDionice(x_i,y_i):
    rez = []
    for i in range(0,len(x_i)):
        rez.append([x_i[i],y_i[i]])
    return rez

# Za nasumičan odabir dionica za rekonstrukciju
def odaberi_Dionice(dionice,t,n):
    nasumicni = random.sample(range(0, n), t)
    rez = []
    for el in nasumicni:
        rez.append(dionice[el])
    return rez

# Funkcija za pravilno računanje modula negativnog broja
def modulo_negativni(a,m):
    return (a%m + m)% m

# Za izračun inverza u mod
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modularni inverz ne postoji !',a)
    else:
        return x % m

# Izračun b_j-ova ( b_j = prod_{k=1,..,t,k!=t} x_k / (x_k - x_j)  mod(p) )
def izracunaj_b(dionice,t,p):
    x_k = []
    for el in dionice: # uzmemo sve xi vrijednosti iz dionica [xi,yi]
        x_k.append(el[0])
    b_rez = []
    produkt_j = 1
    for j in range(0,t): # odvajamo produk brojnika i nazivnika radi lakšeg računanja sa modulom
        produkt_j_brojnik = 1
        produkt_j_nazivnik = 1
        for k in range(0,t):
            if(k!=j):
                produkt_j_brojnik = produkt_j_brojnik * x_k[k]
                produkt_j_nazivnik = produkt_j_nazivnik * (x_k[k]-x_k[j])

        predznak = 1 # predznak ćemo odvojiti u posebnu varijablu, brojnik i nazivnik  će nam biti pozitivni brojevi
        if(produkt_j_brojnik < 0 and produkt_j_nazivnik < 0):
            predznak = 1
            produkt_j_brojnik = produkt_j_brojnik *(-1)
            produkt_j_nazivnik = produkt_j_nazivnik *(-1)
        elif(produkt_j_brojnik < 0 and produkt_j_nazivnik > 0):
            predznak = -1
            produkt_j_brojnik = produkt_j_brojnik *(-1)
        elif(produkt_j_brojnik > 0 and produkt_j_nazivnik < 0):
            predznak = -1
            produkt_j_nazivnik = produkt_j_nazivnik *(-1)
        else:
            predznak = 1
            
        b_j = modulo_negativni(predznak * produkt_j_brojnik * modinv(produkt_j_nazivnik,p),p)
        b_rez.append(b_j)
    return b_rez

# REKONSTRUKCIJA LOZINKE K = sum_{j=1}^{t} b_j * y_j  mod(p) 
def rekonstrukcija_Lozinke(b,dionice,t,p):
    y = []
    for el in dionice: # izvučemo yi vrijednosti iz dionica [xi,yi]
        y.append(el[1])
    suma = 0
    rez = []
    for j in range(0,t):
        suma = suma + y[j]*b[j]
        rez.append(y[j]*b[j])
    return suma%p

# Vratimo maskiranu lozinku u početni oblik
def odmaskiraj_Lozinku(lozinka,tajni_pomak):
    lozinka_str = str(lozinka)
    lista_slova = [lozinka_str[i:i+2] for i in range(0, len(lozinka_str), 2)] # podijelimo lozinku po 2 broja
    prazna = []
    kodovi = []
    for el in lista_slova:
        kodovi.append(int(el)-tajni_pomak)
    rez = []
    for el in kodovi:
        rez.append(chr(el))
    return "".join(rez)

def unos_Podataka():
    print("*************************************************************")
    print("  S H  A M I R O V A    S H E M A    Z A    L O Z I N K E")
    print("*************************************************************")

    lozinka = ""
    print("Lozinka mora biti niz od velikih slova eng.abecede i/ili brojeva 0-9, duljine 4-8 te ne smije sadržavati razmake.")
    print("")
    while(lozinka == ""):
        lozinka = input("Unesite Vašu lozinku : ")
        lozinka = provjeraLozinke(lozinka)

    lozinka_pomak = maskirajLozinku(lozinka)
    lozinka = lozinka_pomak[0]
    tajni_pomak = lozinka_pomak[1]

    # Generirajmo prosti broj p za Zp, na temelju kojega ćemo provjeriti potrebne uvjete za n i t
    p = generirajProsti_p(lozinka)

    # Korisnik zatim unosi broj n koji predstavlja ukupan broj dijelova na koje želi podijeliti tajnu.
    # uvjet za n : 0 < n+1 <= p
    n = 0
    while(n <= 0 or n+1 > p):
        n = int(input("Unesite na koliko dijelova želite podijeliti Vašu lozinku: "))
        
    # Zatim se unosi minimalan broj dionica potreban za rekonstrukciju tajne( t mora biti veći od 0, ali i manji od n).
    t = 0
    while(t <= 0 or t > n):
        t = int(input("Unesite minimalan broj dionica potrebnih za rekonstrukciju lozinke: "))
    return [lozinka,tajni_pomak,p,n,t]
    
def main():
    podaci = unos_Podataka()
    print("")
    print("********************************************************")
    print("MASKIRANA LOZINKA: ",podaci[0])
    print("TAJNI POMAK: ", podaci[1])
    print("GENERIRANI PROSTI BROJ (za Zp): ", podaci[2])
    print("UKUPAN BROJ DIONICA: ",podaci[3])
    print("MINIMALAN BROJ DIONICA POTREBNIH ZA REKONSTRUKCIJU: ", podaci[4])
    print("********************************************************")
    print("")

    lozinka = podaci[0]
    tajni_pomak = podaci[1]
    p = podaci[2]
    n = podaci[3]
    t = podaci[4]

    # Nasumično odaberemo vrijednosti za xi iz Zp, i=1,2,...,n
    x_evi = random_Xi(n,p)
    print("Nasumični xi : ",x_evi)

    # Nasumično odaberemo vrijednosti za ai iz Zp, i=1,..,t-1
    a_evi = random_Ai(t,p)
    print("Nasumični ai : ",a_evi)

    # Izračunamo vrijednosti a(xi) = yi
    y = a_Funkcija(lozinka,t,x_evi,a_evi,p)
    print("Dobiveni yi : ",y)

    # Generirajmo dobivene dionice
    dionice = generirajDionice(x_evi,y)
    print("********************************************************")
    print(" DOBIVENE DIONICE ")
    for i in range(0,len(dionice)):
        print(dionice[i])
    print("********************************************************")
    print("")
    
    #######################################################################
    # REKONSTRUKCIJA LOZINKE
    #######################################################################
    pitanje = ""
    while(pitanje != "y" and pitanje != "Y" and pitanje != "n" and pitanje != "N"):
        pitanje = input("Da li želite rekonstruirati lozinku (y/n)? ")
    if(pitanje == "Y" or pitanje == "y"):
        print("")
        print("")
        print("********************************************************")
        print("R E K O N S T R U K C I J A    L O Z I N K E")
        print("********************************************************")
        '''
        # Nasumično odabrane dionice ( za provjeru izračuna ):
        # Nasumično odaberimo t dionica od njih n, koje su nam potrebne za rekonstrukciju.
        
        dionice_nasumicno = odaberi_Dionice(dionice,t,n)
        print("Nasumično su odabrane sljedeće dionice:")
        for i in range(0,len(dionice_nasumicno)):
            print(i+1,". ", dionice_nasumicno[i])
        '''

        
        print("")
        print("Morate unijeti ",t," od mogućih ",n," dionica kako bi otkrili Vašu lozinku.")
        print("-----------------------------------------------------------------------")
        print("")
        
        
        # Korisnik unosi t dionica
        dionica_xi = -1
        dionica_yi = -1
        t_dionica = []
        
        for i in range(0,t):
            provjera = False
            while(provjera != True):
                xi = int(input(f"Unesite x{i+1}: "))
                yi = int(input(f"Unesite y{i+1}: "))

                if([xi,yi] not in dionice):
                    provjera = False
                    print("Nepostojeća dionica !")
                elif([xi,yi] in t_dionica):
                    provjera = False
                    print("Već ste unijeli tu dionicu.")
                else:
                    provjera = True
                    t_dionica.append([xi,yi])
        
        print("")
        print("Odabrane su sljedeće dionice za rekonstrukciju tajne")
        print("-----------------------------------------------------------------------")
        for i in range(0,len(t_dionica)):
            print(i+1,".  ",t_dionica[i])
        print("")                
        

        # Za rekonstrukciju koristimo Lagrangeov interp.formulu
        # K = sum_{j=1}^{t} b_j * y_j  mod(p)
        # gdje su b_j = prod_{k=1,..,t,k!=t} x_k / (x_k - x_j)  mod(p)

        # Prvo dakle računamo b_j-ove
        b = izracunaj_b(t_dionica,t,p)
        print("Dobiveni b_j-ovi : ", b)
        print("")

        # Rekonstruirajmo lozinku (rezultat je maskirana lozinka)
        print("-----------------------------------------------------------------------")
        LOZINKA = rekonstrukcija_Lozinke(b,t_dionica,t,p)
        print("Vaša maskirana lozinka je: ", LOZINKA)

        # Vratimo dobivenu maskiranu lozinku u početno stanje
        print("VAŠA IZVORNA LOZINKA JE: ",odmaskiraj_Lozinku(LOZINKA,tajni_pomak))
        print("-----------------------------------------------------------------------")
    else:
        print("Doviđenja !")
        exit
        
        
if __name__ == "__main__":
    main()
    
