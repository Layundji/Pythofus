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
def CalcOptimalLock_Wrapper(dodge, init_p) :
    def CalcOptimalLock_Nested(final_p) :
        tac = (init_p * (dodge+2))/((final_p+0.5)*2) -2
        if tac.is_integer() and final_p%2: tac+=1
        tac = math.ceil(tac)
        return int(tac)
    return CalcOptimalLock_Nested

def CalcOptimalDodge(lock, init_p, final_p):
    """Renvoie la valeur de fuite limite pour detacler un opposant en concervant un nombre de points donnes
    Args :
        - lock    (int) le tacle de l'opposant
        - init_p  (int) le nombre de points (action/mouvements) avant detacle
        - final_p (int) le nombre de points (action/mouvements) apres detacle
    """
    fui = (final_p-0.5)*(2*(lock+2))/(init_p) -2
    if fui.is_integer() and final_p%2 : fui += 1
    fui = math.ceil(fui)
    return int(fui)
def CalcOptimalDodge_Wrapper(lock, init_p) :
    def CalcOptimalDodge_Nested(final_p) :
        fui = (final_p-0.5)*(2*(lock+2))/(init_p) -2
        if fui.is_integer() and final_p%2 : fui += 1
        fui = math.ceil(fui)
        return int(fui)
    return CalcOptimalDodge_Nested

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
    tacle = 70
    fuite = 70

    p = list(range(pm_init+1))

    OptiTac = CalcOptimalLock_Wrapper(dodge = fuite, init_p = pm_init)
    OptiFui = CalcOptimalDodge_Wrapper(lock = tacle, init_p = pm_init)

    opti_tac = list(map(OptiTac,p))
    opti_fui = list(map(OptiFui,p))

    print(f"PM finaux : {p}")
    print(f"fuite opti: {opti_fui}")
    print(f"tacle opti: {opti_tac}")
