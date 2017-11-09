# -*- coding: utf-8 -*-
def has_been_checked(adresse):
    """
    verifie si un fichier en .txt a déjà été enregistré pour cette addresse
    retourne booléen
    """
    import os.path    
    return os.path.isfile("./"+adresse+".txt")
def save_adresse(data_json, adresse):
    """
    crée un fichier .txt avec le json encodé dedans
    retourne le json
    """
    import json
    with open(adresse+".txt", "w") as f:
        json.dump(data_json, f)
    return data_json
def get_adresse(adresse):
    """
    load le json associé à l'adresse
    et le retourne
    """
    assert has_been_checked(adresse)
    import json
    with open(adresse+".txt", "r") as f:
        return json.load(f)
def get_gmap_json(adresse):
    """
    récupère les infos sur une adresse, soit auprès de google, soit dans le système de fichier local
    """
    import urllib.request, urllib.parse, urllib.error
    import json 
    try:
        adresse  = urllib.parse.quote_plus(adresse)
        if has_been_checked(adresse):
            print(" . ", end=' ') 
            return get_adresse(adresse)
        else:       
            print(" GG ", end=' ')
            key      = "&key=AIzaSyBxELVjNecufswtilfW8XqOmj-fJLuUiiA"
            serveur  = "https://maps.googleapis.com/maps/api/geocode/json?address="
            
            url      = serveur+adresse+key
            response = urllib.request.urlopen(url)
            return save_adresse(json.loads(response.read()), adresse)
    except Exception as e :
        print("pbm [%s] sur [%s]"%(e, adresse))
        raise e
def lat_lon(adresse):
    """
    extrait la latitude et la longitude du json récupéré
    """
    
    try:
        data = get_gmap_json(adresse)
        lat = data ['results'][0]['geometry']['location']['lat']
        lon = data ['results'][0]['geometry']['location']['lng']
    except Exception as e:
        print("\n", e, "for [%s]"%adresse)
        return -1,-1

    return lat, lon
def get_lat(adresse):
    return lat_lon(adresse)[0]
def get_lon(adresse):
    return lat_lon(adresse)[1]