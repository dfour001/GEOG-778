from requests import get, exceptions
import json

def get_CURVES_distance(dBu, HAAT, ERP):
    """ Uses the CURVES api from the FCC to estimate the distance
        that the FM signal will decay to the input dBu value, given
        the Hight Above Average Terrain (HAAT) and Effective Radiation 
        Power (ERP).  Returns the distance in KM.

        Inputs:
            dBu - Field strength to which the distance will be estimated
            HAAT - Hight above average terrain
            ERP - Effective radiation power
    """

    try:
        url = f'https://geo.fcc.gov/api/contours/distance.json?computationMethod=0&serviceType=fm&haat={HAAT}&field={dBu}&erp={ERP}&curve=0&outputcache=true'
        r = get(url)
        r.raise_for_status()
        rDict = json.loads(r.text)
        print(r.text)
        distance = rDict['distance']

        return distance
    except exceptions.HTTPError as e:
        print(e)
        return None

    

print(get_CURVES_distance('a', 229, 3.2))



