def createEclipseShadowMapping(earthSpecs,moonSpecs,sunSpecs,frame,penumbraRadius):
        solarEclipseCenterPos = City_EclipseChecker.calculateRayIntersection(sunSpecs[0],moonSpecs[0],earthSpecs[0],earthSpecs[1]/2,1)
        if solarEclipseCenterPos != None:
            penumbraRadius = City_EclipseChecker.calculatePenumbraRadius(moonSpecs,earthSpecs,sunSpecs)
        listOfIntersections,radiusDecrease = eclipseFinder.fullRayCast(earthSpecs,moonSpecs,sunSpecs,penumbraRadius,"Full")
        return listOfIntersections, radiusDecrease