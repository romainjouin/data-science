
import pandas               as      pd
import numpy                as      np
import matplotlib.pyplot    as      plt
import matplotlib.ticker    as      mtick

from jr_data_science        import  functions_de_decouverte_de_fichiers
from jr_data_science        import  useful_functions
from collections            import  OrderedDict

weekdays = OrderedDict({0: "lundi", 1:"mardi", 2:"mercredi", 3:"jeudi", 4:"vendredi", 5:"samedi", 6:"dimanche"})
mois     = OrderedDict({1:"janvier", 2:"février", 3:"mars", 4:"avril", 5: "mai", 6:"juin", 7:"juillet", 8:"août", 9:"septembre", 10:"octobre", 11:"novembre", 12:"décembre"})


def format_euro(nombre, devise=u"€"):
    nombre = format_nombre(nombre)
    return " ".join([nombre, devise])


def format_nombre(nombre):
    import numpy as np
    if np.isnan(nombre):
        return "0"

    nombre = float(nombre)
    if nombre < 1e3:
        return "{:.1f}".format(nombre)
    if nombre < 1e6:
        return "{:.1f}K".format(nombre / 1e3)
    if nombre < 1e9:
        return "{:.1f}M".format(nombre / 1e6)
    if nombre < 1e12:
        return "{:.1f}G".format(nombre / 1e9)
    return str(nombre)

def print_list_as_dict(liste):
    print("dico = {")
    for key in liste:
        print("\"{key}\" : str ,".format(key=key))
    print("}")
    

def print_col_as_dict(df):
    """
    Générateur de code : affiche à l'écran la liste des colonnes d'une DF sous forme de dico.
    """
    print("dtypes = {")
    for col in df.columns:
        print("\"{col}\" : str ,".format(col=col))
    print("}")
    print("""
# => changez les types dans les colonnes, et mettez les dates et colonnes de catégories dans les tableaux ci dessous")
dayfirst = -1
parse_dates = []
categories = []
# rechargez la df avec les colonnes indiquées
df = pd.read
df = pd.read_csv(path, sep=sep, dtype=dtypes, parse_dates=parse_dates, dayfrist=dayfirst)
df.shape, df.dtypes
# vous pouvez aussi générer du code ensuite pour les colonnes catégorielles
for col in categories:
code_for_cat_col(df, col)    
    """)

def analyse_to_excel(df, filename, output_dir="."):
    """
    Construit un fichier csv avec une analyse de chaque colonne de la df => à importer dans excel en tant que tsv.

    """
    import os
    output_file = os.path.join(output_dir, "%s_analyse.csv"%filename)
    
    fichier = [" "]*15
    nz      = 0
    n_col   = 0
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("%s lignes, %s col"%df.shape)

    for col in df.columns:
            print(col)
            n_col        += 1
            nb_valeur     = df[col].value_counts().shape[0]
            nb_null       = df[col].isnull().sum()
            n             = 10
            top_n         = df[col].value_counts().sort_values(ascending=False).reset_index()[:n].values
            pct_top_n     = [x[1]/df.shape[0] for x in top_n]
            fichier[0]   += "\t%s\t  _ \t  _ "%(col)
            fichier[1]   += "\tnb_valeur \t%s \t _"%nb_valeur
            fichier[2]   += "\tnb_null \t %s \t _"%(nb_null)
            current_ligne = 2
            for ((x,y),z) in zip(top_n, pct_top_n):
                current_ligne += 1
                fichier[current_ligne] += "\t%s\t %s \t %.2f"%(x,y,z)
            while current_ligne<14:
                current_ligne += 1
                fichier[current_ligne] += "\t%s\t %s \t %s"%("_","_","_")
            if n_col>0:
                if n_col %4==0:        
                    print(n_col)
                    with open(output_file, "a", encoding="utf-8") as f:
                        for line in fichier:
                            f.write(line+"\n")
                    fichier = [" "]*15
    with open(output_file, "a", encoding="utf-8") as f:
        for line in fichier:
            f.write(line+"\n")
            
    print("Wrote into %s"%(output_file))

def code_for_cat_col(df, col):
    """
    Generate a python string to help transforming a pandas column into a categorie.
    """
    print("from pandas.api.types import CategoricalDtype")
    to_print = "cat = CategoricalDtype(categories=["
    try:
        tri = sorted(df[col].unique())
    except:
        tri = df[col].unique()
    for x in tri:
        to_print += "\'%s\',"%x
    to_print += "], ordered=True)"
    print(to_print)
    print("#df['%s'] = df['%s'].astype(cat)"%(col, col))

def plot_pivot(graph):
    tab = graph["df"].pivot_table(**graph["pivot"])
    sns.heatmap(tab.sort_index(), cmap="PiYG", center=0)
    plt.title(graph["title"]);

def print_cols(liste):
    for i,x in enumerate(liste):
        print("%s : %s"%(i,x))



def get_filename(path):
    import os
    return os.path.basename(path).split(".")[0]


def decompose_date(df, analyse_col):
    print(analyse_col)
    import pandas as pd
    clean_col = analyse_col.replace(" ", "_")
    from collections import OrderedDict
    weekdays = OrderedDict(
        {0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi", 4: "vendredi", 5: "samedi", 6: "dimanche"})
    mois = OrderedDict({1: "janvier", 2: "février", 3: "mars", 4: "avril", 5: "mai", 6: "juin", 7: "juillet", 8: "août",
                        9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"})
    #
    new_col = "%s_jour_semaine" % clean_col
    df[new_col] = df[analyse_col].map(lambda x: x.weekday()).map(weekdays)
    df[new_col] = pd.Categorical(df[new_col], categories=weekdays.values(), ordered=True)
    #
    new_col = "%s_jour_semaine_int" % clean_col
    df[new_col] = df[analyse_col].map(lambda x: x.weekday())

    #
    new_col = "%s_jour_mois" % clean_col
    df[new_col] = df[analyse_col].map(lambda x: x.day)
    df[new_col] = pd.Categorical(df[new_col], categories=range(32), ordered=True)

    #
    new_col = "%s_mois" % clean_col
    df[new_col] = df[analyse_col].map(lambda x: x.month).map(mois)
    df[new_col] = pd.Categorical(df[new_col], categories=mois.values(), ordered=True)
    #
    new_col = "%s_nth_mois" % clean_col
    df[new_col] = df[analyse_col].map(lambda x: x.month)
    df[new_col] = pd.Categorical(df[new_col], categories=range(1, 13), ordered=True)
    #
    new_col = "%s_week" % clean_col
    df[new_col] = df[analyse_col].map(lambda x: int(x.week))
    df[new_col] = pd.Categorical(df[new_col], categories=range(53), ordered=True)

    #
    new_col = "%s_year" % clean_col
    df[new_col] = df[analyse_col].map(lambda x: int(x.year))
    df[new_col] = pd.Categorical(df[new_col], categories=sorted(list(df[new_col].unique())), ordered=True)
    #
    new_col = "%s_nth_day" % clean_col
    df[new_col] = df[analyse_col].map(lambda x: x.timetuple().tm_yday)
    df[new_col] = pd.Categorical(df[new_col], categories=range(366), ordered=True)
    print("fini")



def fetch_devise(string):
    """
    cherche les mots ["EUR", "$", "£"] dans la string et le renvoie si trouvé.
    """
    devises = ["EUR", "$", "£"]
    default = "unknown"
    for devise in devises:
        if devise in string:
            return devise
    return default
def fetch_value(string):
    """
    Cherche les nombres dans la string.
    """
    import re
    regex = re.compile("\d+(?:\.\d+)*")
    return regex.findall(string)    
        