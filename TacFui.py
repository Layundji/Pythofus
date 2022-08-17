import math



def CalcOptimalLock(dodge, init_p, final_p) :
    """Renvoie la valeur de tacle limite pour que l'opposant detacle avec un nombre de points donnes
    Args :
        - dodge   (int) la fuite de l'opposant
        - init_p  (int) le nombre de points (action/mouvements) avant detacle
        - final_p (int) le nombre de points (action/mouvements) apres detacle
    """
    tac = (init_p * (dodge+2))/((final_p+0.5)*2) -2
    if tac.is_integer() and final_p%2: tac+=1
    tac = math.ceil(tac)
    return int(tac)

def CalcOptimalDodge(lock, init_p, final_p):
    """Renvoie la valeur de fuite limite pour detacler un opposant en concervant un nombre de points donnes
    Args :
        - lock    (int) le tacle de l'opposant
        - init_p  (int) le nombre de points (action/mouvements) avant detacle
        - final_p (int) le nombre de points (action/mouvements) apres detacle
    """
    fui = (final_p-0.5)*(2*(lock+2))/(init_p) -2
    if fui.is_integer() and final_p%2 : fui += 1
    fio = math.ceil(fui)
    return int(fui)

def CalcRemainingP(dodge, lock, init_p) :
    """ Renvoie le nombre de points apres detacle
    Args :
        - dodge  (int) la fuite de fuyard
        - lock   (int) le tacle du tacleur
        - init_p (int) le nombre de points (action/mouvement) du fuyard
    """
    final_p = ((dodge+2)*init_p) / (2*(lock+2))
    final_p = round(final_p)
    return int(final_p)



if __name__ == '__main__' :

    pm_init = 6

    print()
    print("#"*25)
    print()

    dodge = 70
    print(f"PM initiaux : {pm_init}")
    print(f"fuite : {dodge}")

    print("PM detacle".rjust(12),"Tacle".rjust(8),sep='')
    for pm_end in range(pm_init+1) :
        opti_lock = CalcOptimalLock(dodge, pm_init, pm_end)
        print(f"{pm_end:>12}{opti_lock:>8}")

    print()
    print("#"*25)
    print()

    lock = 70
    print(f"PM initiaux : {pm_init}")
    print(f"tacle : {lock}")

    print("PM detacle".rjust(12),"Fuite".rjust(8),sep='')
    for pm_end in range(pm_init+1) :
        opti_dodge = CalcOptimalDodge(lock, pm_init, pm_end)
        print(f"{pm_end:>12}{opti_dodge:>8}")
