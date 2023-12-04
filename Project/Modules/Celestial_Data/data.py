import spiceypy as sp

def getPlanetPos(planetName:str,ephemerisTime:float):
    return sp.spkpos(planetName,ephemerisTime,"J2000","NONE","Sun")[0]

def getCelestialObjectSpecs(planetName:str,ephemerisTime:float,scaleCoff:int):
    diameter = sp.bodvrd(planetName,"RADII",3)[1][0]*2/scaleCoff
    pos1 = getPlanetPos(planetName,ephemerisTime)
    pos = []
    for i in pos1:
        pos.append(i/scaleCoff)
    return [tuple(pos),diameter,planetName]
