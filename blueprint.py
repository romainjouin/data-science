# coding: utf-8

# In[10]:

import matplotlib.ticker as mtick


# # functions

# In[11]:

def get_subset(df, col_de_test, valeur_cherchee):
    mask = df[col_de_test] == valeur_cherchee
    return df[mask]


def get_titulaires(df, col_de_test="TYPE_ROLE", valeur_cherchee="TIT"):
    return get_subset(df, col_de_test, valeur_cherchee)


def get_pp(df, col_de_test="Type acteur", valeur_cherchee="P"):
    return get_subset(df, col_de_test, valeur_cherchee)


def get_pm(df, col_de_test="Type acteur", valeur_cherchee="M"):
    return get_subset(df, col_de_test, valeur_cherchee)


# In[12]:

def pie(ax, serie_data, colors, xlabel=None, explode=None):
    """
    Plot a pie.
    Args:
        ax : matplotlib axe where to plot
        data : pandas series (index is used for the labelling of the pie)
        colors : list of colors (could come from get_palette)
        xlabel : useseless ?
        explode : ?
    usage :
        serie = df.groupby(col)[col]
        pie(ax, serie, get_palette(serie))
    """
    if not xlabel: xlabel = serie_data.index
    patches, texts, autotexts = ax.pie(serie_data,
                                       labels=xlabel,
                                       autopct="%1.1f%%",
                                       colors=colors,
                                       explode=explode)
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_weight("bold")
    ax.axis("equal")


# In[13]:

def pie_and_count(pc_series, pc_label,
                  count_df, count_col_y, count_label,
                  palette=None, explode=None, order=None,
                  figsize=(16, 5), orient="h"):
    """
    Call 2 functions : pie and count plot and create a new figure.

    pc_series : data for pie
    pc_label : label for pie

    count_df : df for a count
    count_col_y : col to execute the count on
    count_label :

    """

    if order:
        pc_series = pc_series.reindex(order)
    else:
        order = pc_series.index

    fig, (ax1, ax2) = get_axes_for_2_col_plot(figsize, orient)

    pie(ax1, pc_series, palette, pc_label, explode=explode)
    count_plot(count_col_y=count_col_y, count_df=count_df, count_label=count_label, ax=ax2, order=order,
               palette=palette)


# In[14]:

def draw_ybroken_lines(ax1, ax2):
    d = 0.02
    kwargs = {"transform": ax1.transAxes,
              "color": "k",
              "clip_on": False}
    x_span = (-d, +d)
    y_span = (-d, +d)
    ax1.plot(x_span, y_span, **kwargs)
    ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)
    kwargs.update(transform=ax2.transAxes)
    x_span = (-d, +d)
    y_span = (1 - d, 1 + d)
    ax2.plot(x_span, y_span, **kwargs)
    ax2.plot(y_span, y_span, **kwargs)


# In[15]:

def draw_xbroken_lines(ax1, ax2):
    d = 0.02
    kwargs = {"transform": ax1.transAxes,
              "color": "k",
              "clip_on": False}
    x_span = (1 - d, 1 + d)
    y_span = (1 - d, 1 + d)
    ax1.plot(x_span, y_span, **kwargs)
    ax1.plot(x_span, (-d, +d), **kwargs)
    kwargs.update(transform=ax2.transAxes)
    x_span = (-d, +d)
    y_span = (1 - d, 1 + d)
    ax2.plot(x_span, y_span, **kwargs)
    ax2.plot(x_span, (-d, +d), **kwargs)


# In[16]:

import seaborn as sns

sns.set(style="ticks", color_codes=True)

# In[17]:

get_ipython().magic(u'pylab inline')

# In[18]:

import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import pandas as pd
import os
from collections import Counter
import numpy as np

import seaborn as sns
import matplotlib.dates as mdates
import random
from functools import reduce
import matplotlib.pyplot as plt

np.random.seed(0)
sns.set(style="white", palette="husl")
get_ipython().magic(u'matplotlib inline')


# In[19]:

def format_euro(nombre, devise=u"€"):
    nombre = format_nombre(nombre)
    return " ".join([nombre, devise])


def format_nombre(nombre):
    import numpy as np
    if np.isnan(nombre):
        return 0

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


# In[20]:

def get_palette(series, palette="deep", palette_order=None):
    palette = sns.color_palette(palette, len(series))
    if palette_order and (len(palette_order) == len(palette)):
        return [palette[i] for i in palette_order]
    return palette


# In[21]:

def get_df(fichier):
    """
    Fetch a dataframe from an existing dataiku dataset.
    """
    import time
    debut = time.time()
    print(time.ctime())
    mydataset = dataiku.Dataset(fichier)
    mydataset_df = mydataset.get_dataframe()
    fin = time.time()
    duree = fin - debut
    print(" temps de chargement du fichier %s = %s" % (fichier, duree))
    return mydataset_df


# In[22]:

def merge_pays2(df, col, df_pays):
    var = pd.merge(df, df_pays, left_on=col, right_on="iso2", how="left")
    return var


def merge_pays3(df, col, df_pays):
    var = pd.merge(df, df_pays, left_on=col, right_on="iso3", how="left")
    return var


# # 0) imports de data

# In[23]:

df_all = get_df("DF_ALL")

# In[24]:

df_pays = get_df("risque_pays")

# In[25]:

df_all["Rating AML calcule"] = df_all["Rating AML calcule"].fillna("NC")
df_all["Rating AML calcule"] = df_all["Rating AML calcule"].astype("category", categories=["L", "M", "H", "NS", "NC"],
                                                                   ordered=True)

# # 1) Nombre de clients PP et PM par business line

# In[39]:

var = df_all[["ID client", "DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"]].drop_duplicates()
tab = var.pivot_table(index="DESCRIPTION_OBJET_HIERARCHIE_1", columns="Type acteur", values="ID client",
                      aggfunc=pd.Series.nunique, margins=True)
tab.astype(int)
tab.astype(int).applymap(format_nombre)

# In[48]:

try:
    tab = tab.drop("All")
except:
    pass
tab.index.name = "branch"
tab[["M", "P"]].plot.barh(stacked=True, title="Nombre de clients PP et PM par business line")
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

# In[44]:

# 1) Nombre de clients PP et PM par business line -> pct
var = df_all[["ID client", "DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"]].drop_duplicates()
tab = var.pivot_table(index="DESCRIPTION_OBJET_HIERARCHIE_1", columns="Type acteur", values="ID client",
                      aggfunc=pd.Series.nunique, margins=False)
tab.astype(int).applymap(format_nombre)
tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %")

# In[49]:

try:
    tab = tab.drop("All")
except:
    pass
tab2.index.name = "branch"
tab2[["M", "P"]].plot.barh(stacked=True, title="Nombre de clients PP et PM par business line (pct)")
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

# # 1.1) nb de clients par cdb

# In[691]:

df_all_0 = df_all[
    ["ID titulaire", "ID client", "DESCRIPTION_OBJET_HIERARCHIE_1", "Contrat de base", "Type acteur"]].drop_duplicates()

# In[692]:

tab = df_all_0.groupby("Contrat de base")["ID client"].size()

# In[693]:

tab2 = tab.to_frame()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8), sharex=True, )
fig.suptitle(u"Nb of actors by Contracts ", fontsize=20)
sns.countplot(x="ID client", data=tab2, ax=ax1)
sns.countplot(x="ID client", data=tab2, ax=ax2)
ax1.set_ylim(4 * mil, 150 * mil)
ax1.set_xlim(0, 25)
ax2.set_ylim(0, 4 * mil)
ax2.set_xlim(0, 25)
ax1.set_xlabel("")
ax1.set_ylabel("")
ax2.set_xlabel("Number of actors")
ax2.set_ylabel("Number of Contracts")
draw_ybroken_lines(ax1, ax2)
ax1.spines["bottom"].set_visible(False)
ax2.spines["top"].set_visible(False)

# # 2) Nombre de clients Titulaires PP et PM par business line et AUM correspondants
#

# ## 2.1) Nombre de clients Titulaires PP et PM par business line

# In[53]:

df_all_0 = df_all[["ID titulaire", "ID client", "DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"]].drop_duplicates()
var = df_all_0[df_all_0["ID titulaire"] == df_all_0["ID client"]]
tab = var.pivot_table(index="DESCRIPTION_OBJET_HIERARCHIE_1", columns="Type acteur", values="ID titulaire",
                      aggfunc=pd.Series.nunique, margins=True)
tab.astype(int).applymap(format_nombre)

# In[56]:

try:
    tab = tab.drop("All")
except:
    pass
sujet = "Nombre de clients Titulaires PP et PM par business line"
tab.index.name = "branch"
tab[["M", "P"]].plot.barh(stacked=True, title=sujet)
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

# In[55]:

tab = var.pivot_table(index="DESCRIPTION_OBJET_HIERARCHIE_1", columns="Type acteur", values="ID titulaire",
                      aggfunc=pd.Series.nunique, margins=False)
tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %")

# In[58]:

try:
    tab = tab.drop("All")
except:
    pass
sujet = "Nombre de clients Titulaires PP et PM par business line (pct)"
tab2.index.name = "branch"
tab2[["M", "P"]].plot.barh(stacked=True, title=sujet)
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

# ## 2.2) Nombre de clients Titulaires PP et PM par business line et AUM correspondants
#

# In[59]:

df_all_0 = df_all[["ID titulaire", "ID client", "Contrat de base", "DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur",
                   "Total actifs sous gestion"]].drop_duplicates()
var = df_all_0.loc[df_all_0["ID client"] == df_all_0["ID titulaire"]]

# In[60]:


tab = var.pivot_table(index="DESCRIPTION_OBJET_HIERARCHIE_1", columns="Type acteur", values="Total actifs sous gestion",
                      aggfunc="sum", margins=True)
tab.astype(int).applymap(format_euro)

# In[102]:

try:
    tab = tab.drop("All")
except:
    pass
sujet = "AUM des Titulaires PP et PM par business line"
tab.index.name = "branch"
ax = tab[["M", "P"]].plot.barh(stacked=True, title=sujet)
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: format_nombre(x)))

# In[103]:

tab = var.pivot_table(index="DESCRIPTION_OBJET_HIERARCHIE_1", columns="Type acteur", values="Total actifs sous gestion",
                      aggfunc="sum", margins=False)
tab.applymap(format_euro)
tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %")

# In[106]:

try:
    tab = tab.drop("All")
except:
    pass
sujet = "AUM des Titulaires PP et PM par business line (pct)"
tab2.index.name = "branch"
ax = tab2[["M", "P"]].plot.barh(stacked=True, title=sujet)
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: format_nombre(x)))

# # 3) Répartition des CDB par score de risque AML par business line

# In[107]:

var = df_all[["Contrat de base", "DESCRIPTION_OBJET_HIERARCHIE_1", "Rating AML calcule"]].drop_duplicates()
tab = var.pivot_table(index="DESCRIPTION_OBJET_HIERARCHIE_1", columns="Rating AML calcule", values="Contrat de base",
                      aggfunc=pd.Series.nunique, margins=True)
tab.astype(int).applymap(format_nombre)

# In[190]:

try:
    tab = tab.drop("All", axis=1)
except:
    pass
sujet = U"Répartition des CDB par score de risque AML par business line"
tab.index.name = "branch"
mil = 1000
limite = 25 * mil
ymax = 200 * mil
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 4), sharex=False, )
for v in [ax1.xaxis, ax1.yaxis, ax2.xaxis, ax2.yaxis]:
    v.set_major_formatter(mtick.FuncFormatter(lambda x, _: format_nombre(x)))
tab.plot.barh(stacked=True, title=sujet, ax=ax1, rot=0, legend=False)
tab.plot.barh(stacked=True, title=sujet, ax=ax2, rot=0)
fig.suptitle(sujet)
ax2.set_xlim(limite, ymax)
ax1.set_xlim(0, limite)
for v in [ax1, ax2]:
    v.set_xlabel("")
    v.set_ylabel("")
    v.set_title("")

draw_xbroken_lines(ax1, ax2)
ax1.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
ax2.set_yticklabels("")
ax2.yaxis.set_ticks([]);

# In[160]:

margin = False
var = df_all[["Contrat de base", "DESCRIPTION_OBJET_HIERARCHIE_1", "Rating AML calcule"]].drop_duplicates()
tab = var.pivot_table(index="DESCRIPTION_OBJET_HIERARCHIE_1", columns="Rating AML calcule", values="Contrat de base",
                      aggfunc=pd.Series.nunique, margins=margin)
tab.astype(int)
tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %")

# In[175]:

try:
    tab = tab.drop("All")
except:
    pass
suje_tab2 = sujet + "(pct)"
tab2.index.name = "branch"
ax = tab2.plot.barh(stacked=True, title=suje_tab2, figsize=(7, 4))
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: format_nombre(x)))

# # 4 ) Combien d'acteurs rattachés aux contrats NS / blanc => appréhender "l'angle mort" -> les acteurs dont ils ne regardent pas le risque + type de ces acteurs -> PP ou PM ?

# # 4.1) total

# In[240]:

# 4 ) Combien d'acteurs rattachés aux contrats NS / blanc => appréhender "l'angle mort" -> les acteurs dont ils ne regardent pas le risque + type de ces acteurs -> PP ou PM ?
var = df_all[["ID client", "Type acteur", "Rating AML calcule"]].drop_duplicates()
tab = var.pivot_table(index="Type acteur", columns="Rating AML calcule", values="ID client", aggfunc=pd.Series.nunique,
                      margins=True)
tab.astype(int).applymap(format_nombre)

# In[241]:

mil = 1000


def horizontal(tab, sujet, limite=50 * mil, ymax=300 * mil):
    for axe in [0, 1]:
        try:
            tab = tab.drop("All", axis=axe)
        except Exception as e:
            print(e)
            pass

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 4), sharex=False, )
    for v in [ax1.xaxis, ax1.yaxis, ax2.xaxis, ax2.yaxis]:
        v.set_major_formatter(mtick.FuncFormatter(lambda x, _: format_nombre(x)))
    tab.plot.barh(stacked=True, title=sujet, ax=ax1, rot=0, legend=False)
    tab.plot.barh(stacked=True, title=sujet, ax=ax2, rot=0)
    fig.suptitle(sujet)
    ax2.set_xlim(limite, ymax)
    ax1.set_xlim(0, limite)
    for v in [ax1, ax2]:
        v.set_xlabel("")
        v.set_ylabel("")
        v.set_title("")

    draw_xbroken_lines(ax1, ax2)
    ax1.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    ax2.set_yticklabels("")
    ax2.yaxis.set_ticks([]);


# In[242]:

sujet = U"Nombre d'acteurs rattachés par type de risque des contrats. "
tab.index.name = "Type d'acteur"
horizontal(tab, sujet)

# In[243]:

# 4 ) Combien d'acteurs rattachés aux contrats NS / blanc => appréhender "l'angle mort" -> les acteurs dont ils ne regardent pas le risque + type de ces acteurs -> PP ou PM ?
var = df_all[["ID client", "Type acteur", "Rating AML calcule"]].drop_duplicates()
tab = var.pivot_table(index="Type acteur", columns="Rating AML calcule", values="ID client", aggfunc=pd.Series.nunique,
                      margins=False)
tab.astype(int)
tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %")


# In[244]:

def horizontal_pct(tab2, sujet_tab2):
    ax = tab2.plot.barh(stacked=True, title=sujet_tab2, figsize=(7, 4))
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: format_nombre(x)))


# In[245]:

try:
    tab = tab.drop("All")
except:
    pass
sujet_tab2 = sujet + "(pct)"
tab2.index.name = "Type d'acteur"
horizontal_pct(tab2, sujet_tab2)

# # 4.2) par business line

# In[246]:

var = df_all[["ID client", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1", "Rating AML calcule"]].drop_duplicates()
tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"], columns="Rating AML calcule",
                      values="ID client", aggfunc=pd.Series.nunique, margins=True)
tab.applymap(format_nombre)

# In[247]:

sujet = U"Nombre d'acteurs rattachés par type de risque des contrats, par BL. "
tab.index.name = "branch"
horizontal(tab, sujet, limite=40 * mil)

# In[248]:

var = df_all[["ID client", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1", "Rating AML calcule"]].drop_duplicates()
tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"], columns="Rating AML calcule",
                      values="ID client", aggfunc=pd.Series.nunique)
tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %")

# In[249]:

try:
    tab = tab.drop("All")
except:
    pass
sujet_tab2 = sujet + "(pct)"
tab2.index.name = "Type d'acteur"
horizontal_pct(tab2, sujet_tab2)

# # 5) Répartition de la clientèle entre résidents et non-résidents (critère de résidence fiscale) et entre nationaux et étrangers (critère de nationalité)

# In[352]:

var = df_all[["ID client", "Pays residence fiscale", "Nationalite 1"]].drop_duplicates()
var["Fiscalite"] = (var["Pays residence fiscale"] == "LUX").map({True: "Luxembourg", False: "Non Luxembourg"})
var["Nationalite"] = (var["Nationalite 1"] == "LUX").map({True: "Luxembourg", False: "Non Luxembourg"})
tab = var.pivot_table(index="Fiscalite", columns="Nationalite", values="ID client", aggfunc=pd.Series.nunique,
                      margins=True)
tab.applymap(format_nombre)

# In[357]:

tab = try_drop_all(tab)
sujet = U"Répartition de la clientèle entre résidents et non-résidents (critère de résidence fiscale)"
tab.plot.barh(title=sujet, figsize=(7, 4))

# In[358]:

var = df_all[["ID client", "Pays residence fiscale", "Nationalite 1"]].drop_duplicates()
var["Fiscalite"] = (var["Pays residence fiscale"] == "LUX").map({True: "Luxembourg", False: "Non Luxembourg"})
var["Nationalite"] = (var["Nationalite 1"] == "LUX").map({True: "Luxembourg", False: "Non Luxembourg"})
tab = var.pivot_table(index="Fiscalite", columns="Nationalite", values="ID client", aggfunc=pd.Series.nunique)
tab2 = tab / tab.sum().sum() * 100
tab2.applymap(lambda x: str(int(x)) + " %")

# In[359]:

df = pd.DataFrame()
current_ligne = -1
for ligne in tab2.values:
    current_ligne = current_ligne + 1
    current_index = tab2.index.values[current_ligne]
    current_col = -1
    for v in ligne:
        current_col = current_col + 1
        current_col_name = tab2.columns[current_col]
        legend = "nationalite : " + current_col_name + " , \n fiscalite : " + current_index + "(" + format_nombre(
            v) + " pct)"
        df = pd.concat([df, pd.DataFrame({"V": v}, index=[legend])])

# In[360]:

ax = df.plot.pie("V", legend=False, title=sujet)
ax.axis("equal");

# # 5) sur hub -  Répartition de la clientèle entre résidents et non-résidents (critère de résidence fiscale) et entre nationaux et étrangers (critère de nationalité)
#

# In[566]:

var = df_all[["ID client", "Pays residence fiscale", "Nationalite 1"]].drop_duplicates()
pays_hub = ["LUX", "FRA", "BEL", "DEU"]
var["Fiscalite"] = (var["Pays residence fiscale"].isin(pays_hub)).map({True: "Hub", False: "Non hub"})
var["Nationalite"] = (var["Nationalite 1"].isin(pays_hub)).map({True: "Hub", False: "Non hub"})
tab = var.pivot_table(index="Fiscalite", columns="Nationalite", values="ID client", aggfunc=pd.Series.nunique,
                      margins=True)
tab.applymap(format_nombre)


# In[567]:

def try_drop_all(tab):
    """
    tab : result d'un pivot table
    Return : tab
    """
    for axe in [0, 1]:
        try:
            tab = tab.drop("All", axis=axe)
        except Exception as e:
            print(e)
            pass
    return tab


# In[568]:

tab = try_drop_all(tab)
sujet = U"Répartition de la clientèle entre résidents hub local et non-résidents fiscaux dans le hub local"
tab.plot.barh(title=sujet, figsize=(7, 4))

# In[569]:

tab = var.pivot_table(index="Fiscalite", columns="Nationalite", values="ID client", aggfunc=pd.Series.nunique,
                      margins=False)
tab2 = tab / tab.sum().sum() * 100
tab2.applymap(lambda x: "{:.1f} %".format(float(x)))

# In[365]:

df = pd.DataFrame()
current_ligne = -1
for ligne in tab2.values:
    current_ligne = current_ligne + 1
    current_index = tab2.index.values[current_ligne]
    current_col = -1
    for v in ligne:
        current_col = current_col + 1
        current_col_name = tab2.columns[current_col]
        legend = "nationalite : " + current_col_name + " , \n fiscalite : " + current_index + "(" + format_nombre(
            v) + " pct)"
        df = pd.concat([df, pd.DataFrame({"V": v}, index=[legend])])
ax = df.plot.pie("V", legend=False, title=sujet)
ax.axis("equal");

# # 6) résidence / non résident + nationaux / nationaux => tableau a 4 entrée + par bl  (nb et % )
#

# In[473]:

var = df_all[
    ["ID client", "DESCRIPTION_OBJET_HIERARCHIE_1", "Pays residence fiscale", "Nationalite 1"]].drop_duplicates()
var["Fiscalite"] = (var["Pays residence fiscale"] == "LUX").map({True: "Luxembourg", False: "Non Luxembourg"})
var["Nationalite"] = (var["Nationalite 1"] == "LUX").map({True: "Luxembourg", False: "Non Luxembourg"})
tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Fiscalite"], columns="Nationalite", values="ID client",
                      aggfunc=pd.Series.nunique)
tab.applymap(format_nombre)

# In[474]:

sujet = U"Nrésidents / non résidents Vs nationaux / nationaux par BL "
tab.index.name = "branch"
horizontal(tab, sujet, limite=30 * mil, ymax=150 * mil)


# In[556]:

def pct_by_group(tab, colonne):
    """
    tab : pivot table (2 niveaux)
    colonne : nom de la colonne en second niveau des x
    """
    tab = tab.unstack(colonne)
    tab = tab.div(tab.sum(axis=1), axis=0).stack().applymap(lambda x: "{:.1f}%".format(x * 100) if x > 0 else "0 %")
    return tab


# # pas mis dans correction ci dessous

# In[476]:

tab = pct_by_group(tab, "Fiscalite")
tab

# # 6) sur hub :  résidence / non résident + nationaux / nationaux => tableau a 4 entrée + par bl  (nb et % )
#

# In[429]:

var = df_all[
    ["ID client", "DESCRIPTION_OBJET_HIERARCHIE_1", "Pays residence fiscale", "Nationalite 1"]].drop_duplicates()
var["Fiscalite"] = (var["Pays residence fiscale"].isin(pays_hub)).map({True: "Hub", False: "Non Hub"})
var["Nationalite"] = (var["Nationalite 1"].isin(pays_hub)).map({True: "Hub", False: "Non Hub"})
tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Fiscalite"], columns="Nationalite", values="ID client",
                      aggfunc=pd.Series.nunique, margins=True)
tab.applymap(format_nombre)

# In[430]:

tab = try_drop_all(tab)
tab = pct_by_group(tab, "Fiscalite")
tab

# # 7) résidents / non résidents Vs nationaux / nationaux par type d'acteurs et  BL

# In[431]:

var = df_all[["ID client", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1", "Pays residence fiscale",
              "Nationalite 1"]].drop_duplicates()
var["Fiscalite"] = (var["Pays residence fiscale"] == "LUX").map({True: "Luxembourg", False: "Non Luxembourg"})
var["Nationalite"] = (var["Nationalite 1"] == "LUX").map({True: "Luxembourg", False: "Non Luxembourg"})
tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur", "Fiscalite"], columns="Nationalite",
                      values="ID client", aggfunc=pd.Series.nunique, margins=True)
tab.applymap(format_nombre)

# In[432]:

tab = try_drop_all(tab)
tab = pct_by_group(tab, "Fiscalite")
tab

# # 7) sur hub : résidents / non résidents Vs nationaux / nationaux par type d'acteurs et  BL

# In[433]:

var = df_all[["ID client", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1", "Pays residence fiscale",
              "Nationalite 1"]].drop_duplicates()
var["Fiscalite"] = (var["Pays residence fiscale"].isin(pays_hub)).map({True: "Hub", False: "Non Hub"})
var["Nationalite"] = (var["Nationalite 1"].isin(pays_hub)).map({True: "Hub", False: "Non Hub"})
tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur", "Fiscalite"], columns="Nationalite",
                      values="ID client", aggfunc=pd.Series.nunique, margins=True)
tab.applymap(format_nombre)

# In[434]:

tab = try_drop_all(tab)
tab = pct_by_group(tab, "Fiscalite")
tab

# # 8) Nombre d'acteurs PP et PM avec une résidence fiscale dans un pays à risque élevé

# In[435]:

risque_pays = get_df("risque_pays")
var = df_all[["ID client", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1", "Pays residence fiscale"]].drop_duplicates()
var["Pays residence fiscale"] = var["Pays residence fiscale"].fillna("NC")
var = pd.merge(var, risque_pays, left_on="Pays residence fiscale", right_on="code bil", how="left")
var["risque watchlist"] = var["risque watchlist"].fillna("NC")
tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"], columns="risque watchlist",
                      values="ID client", aggfunc=pd.Series.nunique, margins=True)
tab.applymap(format_nombre)

# In[437]:

tab = try_drop_all(tab)
tab = pct_by_group(tab, "Type acteur")
tab

# # 8 bis) top 10 des pays

# In[438]:

var = df_all[["ID client", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1", "Pays residence fiscale"]].drop_duplicates()
# Fill residence fiscale vide
var["Pays residence fiscale"] = var["Pays residence fiscale"].fillna("NC")
# Merge risque pays
var = pd.merge(var, risque_pays, left_on="Pays residence fiscale", right_on="code bil", how="left")
# Fill risque vide
var["risque watchlist"] = var["risque watchlist"].fillna("NC")
# filtre sur pays C
var2 = var.loc[var["risque watchlist"] == "C"]
# nb de clients uniaue
var3 = var2.pivot_table(index=["risque watchlist", "code bil", "pays watchlist"], columns="Type acteur",
                        values="ID client", aggfunc=pd.Series.nunique, margins=True)

var4 = var3.sort_values("All", ascending=False)[:10]
var4.applymap(format_nombre)

# # 9) Nombre de titulaires PP et PM et "Actifs Bruts" correspondants

# In[439]:

df_all_0 = df_all[["ID titulaire", "ID client", "Contrat de base", "DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur",
                   "Total actifs sous gestion", "Pays residence fiscale"]].drop_duplicates()
var = df_all_0.loc[df_all_0["ID client"] == df_all_0["ID titulaire"]]

# In[440]:

print(var.shape, var["Total actifs sous gestion"].sum())
var["Pays residence fiscale"] = var["Pays residence fiscale"].fillna("NC")
var = pd.merge(var, risque_pays, left_on="Pays residence fiscale", right_on="code bil", how="left")
var["risque watchlist"] = var["risque watchlist"].fillna("NC")
print(var.shape, var["Total actifs sous gestion"].sum())

# In[441]:

tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"], columns="risque watchlist",
                      values="Total actifs sous gestion", aggfunc="sum", margins=True)
tab.applymap(format_euro)

# In[442]:

tab = try_drop_all(tab)
tab = pct_by_group(tab, "Type acteur")
tab

# # top 10

# In[42]:

df_all_0 = df_all[["ID titulaire", "ID client", "Contrat de base", "DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur",
                   "Total actifs sous gestion", "Pays residence fiscale"]].drop_duplicates()
var = df_all_0.loc[df_all_0["ID client"] == df_all_0["ID titulaire"]]

# In[43]:

# Fill residence fiscale vide
var["Pays residence fiscale"] = var["Pays residence fiscale"].fillna("NC")
# Merge risque pays
var = pd.merge(var, risque_pays, left_on="Pays residence fiscale", right_on="code bil", how="left")
# Fill risque vide
var["risque watchlist"] = var["risque watchlist"].fillna("NC")
# filtre sur pays C
var2 = var.loc[var["risque watchlist"] == "C"]

# In[44]:

# nb de clients uniaue
var3 = var2.pivot_table(index=["risque watchlist", "code bil", "pays watchlist"], columns="Type acteur",
                        values="Total actifs sous gestion", aggfunc="sum", margins=True)

var4 = var3.sort_values("All", ascending=False)[:10]
var4.applymap(format_euro)


# # 10) Distribution des clients (sauf mandataire) PP selon leur âge (+ donner âge moyen)

# In[468]:

def get_palette(series, palette="deep", palette_order=None):
    palette = sns.color_palette(palette, len(series))
    if palette_order and (len(palette_order) == len(palette)):
        return [palette[i] for i in palette_order]
    return palette


def histo_log10(series, xlibelle, ylibelle, bins=None):
    fig, ax = plt.subplots(1, figsize=(5, 4))
    histo_log10_on_ax(series, xlibelle, ylibelle, bins=None, ax=ax)


def histo_log10_on_ax(series, xlibelle, ylibelle, ax, bins=None):
    mean_ = series.mean()
    log10_mean = np.log10(mean_)
    series = series[series >= 1]
    series = np.log10(series.clip(1, None))
    mini = int(series.min())
    maxi = int(series.max())
    puissances = range(max(mini, 2), maxi + 2 + 1)
    labels_ = [u"", u"", u"", u"1K€", u"10K€", u"100K€", u"1M€", u"10M€", u"100M€", u"1G€", u"10G€", u"100G€"]
    labels = [labels_[i] for i in puissances]
    fig = sns.distplot(series, kde=False, ax=ax, bins=bins)
    ax.set_xlim(puissances[0], puissances[-1])
    ax.set_xticklabels(labels)
    ax.set_xlabel(xlibelle + "\n Moy. = " + format_euro(mean_) + u" échelle log", fontsize=10)
    ax.set_ylabel(ylibelle, fontsize=11)
    return fig


def histo_log(series, xlibelle, ylibelle, title, bins=None):
    fig, ax = plt.subplots(1, figsize=(5, 4))
    histo_on_ax(series, xlibelle, ylibelle, title, bins=None, ax=ax)


def histo_on_ax(series, xlibelle, ylibelle, title, ax, bins=None):
    mean_ = series.mean()
    log10_mean = np.log10(mean_)
    mini = int(series.min())
    maxi = int(series.max())
    fig = sns.distplot(series, kde=False, ax=ax, bins=bins)
    ax.set_xlabel(xlibelle + "\n Moy. = " + format_nombre(mean_), fontsize=10)
    ax.set_ylabel(ylibelle, fontsize=11)
    ax.set_title(title)
    return fig


# In[472]:

var = df_all.loc[~df_all["LIBELLE_FR"].isin(["MANDATAIRE"])]
var = var.loc[var["Type acteur"] == "P"]
var = var[["ID client", "AGE"]].drop_duplicates()
title = "Distribution des ages des PP \n hors mandataires. "
histo_log(var.AGE, "age", "Frequence", title)


# # 11) Distribution des clients selon leur âge et présence de mandataires => double courbe de gauss
#

# In[479]:

def disp_col(df):
    """
    Print df's columns, one at a time.
    """
    i = -1
    for col in df.columns:
        i += 1
        print("%s) %s" % (i, col))


# In[480]:

id_contrats_avec_mandataires = df_all.loc[df_all["LIBELLE_FR"] == "MANDATAIRE", "Contrat de base"]
cdb_avec_mandataire = df_all.loc[df_all["Contrat de base"].isin(id_contrats_avec_mandataires)]
cdb_sans_mandataire = df_all.loc[~df_all["Contrat de base"].isin(id_contrats_avec_mandataires)]
cdb_sans_mandataire.shape, cdb_avec_mandataire.shape

# In[481]:

cdb_sans_mandataire = cdb_sans_mandataire.loc[~cdb_sans_mandataire["LIBELLE_FR"].isin(["MANDATAIRE"])]
cdb_avec_mandataire = cdb_avec_mandataire.loc[~cdb_avec_mandataire["LIBELLE_FR"].isin(["MANDATAIRE"])]

# In[482]:

cdb_sans_mandataire = cdb_sans_mandataire.loc[cdb_sans_mandataire["Type acteur"] == "P"]
cdb_avec_mandataire = cdb_avec_mandataire.loc[cdb_avec_mandataire["Type acteur"] == "P"]
cdb_avec_mandataire.shape, cdb_sans_mandataire.shape

# In[483]:

cdb_sans_mandataire = cdb_sans_mandataire[["ID client", "AGE"]].drop_duplicates()
cdb_avec_mandataire = cdb_avec_mandataire[["ID client", "AGE"]].drop_duplicates()
cdb_sans_mandataire.shape[0] + cdb_avec_mandataire.shape[0]

# In[489]:

age_moyen = cdb_avec_mandataire.AGE.mean()

cdb_avec_mandataire.AGE.plot.hist(alpha=0.65, bins=30,
                                  title="Contrats avec mandataires \n Distribution des ages de tous les PP \n hors mandataires. Age moyen = {:.1f}".format(
                                      age_moyen))
titre = "cdb avec mandataire, age moyen des acteurs : {:.1f} ".format(age_moyen)
# histo_log(cdb_avec_mandataire.AGE, "age", "Frequence",titre, bins=30)


# In[490]:

age_moyen = cdb_sans_mandataire.AGE.mean()
cdb_sans_mandataire.AGE.plot.hist(alpha=0.65, bins=30,
                                  title="Contrats sans mandataires \n Distribution des ages des PP \n hors mandataires. Age moyen = {:.1f}".format(
                                      age_moyen))
titre = titre + "\n cdb sans mandataire, age moyen des acteurs : {:.1f}".format(age_moyen)


# In[491]:

def get_palette(series, palette="deep", palette_order=None):
    palette = sns.color_palette(palette, len(series))
    if palette_order and (len(palette_order) == len(palette)):
        return [palette[i] for i in palette_order]
    return palette


# In[492]:

ax = sns.distplot(cdb_sans_mandataire.AGE.dropna(), kde=False, bins=30, hist_kws={"alpha": 0.65})
sns.distplot(cdb_avec_mandataire.AGE.dropna(), kde=False, color="blue", bins=30, ax=ax, hist_kws={"alpha": 0.3})
ax.set_title(titre)
ax.set_xlim(-1, 110)


# # 11) sur le wealth =>  Distribution des clients selon leur âge et présence de mandataires => double courbe de gauss
#

# In[827]:

def disp_col(df):
    """
    Print df's columns, one at a time.
    """
    i = -1
    for col in df.columns:
        i += 1
        print("%s) %s" % (i, col))


# In[829]:

df_wealth = get_subset(df_all, "DESCRIPTION_OBJET_HIERARCHIE_1", "WEALTH MANAGEMENT")
df_wealth.shape

# In[830]:

id_contrats_avec_mandataires = df_wealth.loc[df_wealth["LIBELLE_FR"] == "MANDATAIRE", "Contrat de base"]
cdb_avec_mandataire = df_wealth.loc[df_wealth["Contrat de base"].isin(id_contrats_avec_mandataires)]
cdb_sans_mandataire = df_wealth.loc[~df_wealth["Contrat de base"].isin(id_contrats_avec_mandataires)]
cdb_sans_mandataire.shape, cdb_avec_mandataire.shape

# In[831]:

cdb_sans_mandataire = cdb_sans_mandataire.loc[~cdb_sans_mandataire["LIBELLE_FR"].isin(["MANDATAIRE"])]
cdb_avec_mandataire = cdb_avec_mandataire.loc[~cdb_avec_mandataire["LIBELLE_FR"].isin(["MANDATAIRE"])]

# In[832]:

cdb_sans_mandataire = cdb_sans_mandataire.loc[cdb_sans_mandataire["Type acteur"] == "P"]
cdb_avec_mandataire = cdb_avec_mandataire.loc[cdb_avec_mandataire["Type acteur"] == "P"]
cdb_avec_mandataire.shape, cdb_sans_mandataire.shape

# In[833]:

cdb_sans_mandataire = cdb_sans_mandataire[["ID client", "AGE"]].drop_duplicates()
cdb_avec_mandataire = cdb_avec_mandataire[["ID client", "AGE"]].drop_duplicates()
cdb_sans_mandataire.shape[0] + cdb_avec_mandataire.shape[0]

# In[838]:

age_moyen = cdb_avec_mandataire.AGE.mean()

cdb_avec_mandataire.AGE.plot.hist(alpha=0.65, bins=30,
                                  title="Contrats Wealth avec mandataires \n Distribution des ages de tous les PP \n hors mandataires. Age moyen = {:.1f}".format(
                                      age_moyen))
titre = "cdb Wealth avec mandataire, age moyen des acteurs : {:.1f} ".format(age_moyen)
# histo_log(cdb_avec_mandataire.AGE, "age", "Frequence",titre, bins=30)


# In[839]:

age_moyen = cdb_sans_mandataire.AGE.mean()
cdb_sans_mandataire.AGE.plot.hist(alpha=0.65, bins=30,
                                  title="Contrats Wealth sans mandataires \n Distribution des ages des PP \n hors mandataires. Age moyen = {:.1f}".format(
                                      age_moyen))
titre = titre + "\n cdb sans mandataire, age moyen des acteurs : {:.1f}".format(age_moyen)


# In[840]:

def get_palette(series, palette="deep", palette_order=None):
    palette = sns.color_palette(palette, len(series))
    if palette_order and (len(palette_order) == len(palette)):
        return [palette[i] for i in palette_order]
    return palette


# In[841]:

ax = sns.distplot(cdb_sans_mandataire.AGE.dropna(), kde=False, bins=30, hist_kws={"alpha": 0.65})
sns.distplot(cdb_avec_mandataire.AGE.dropna(), kde=False, color="blue", bins=30, ax=ax, hist_kws={"alpha": 0.3})
ax.set_title(titre)
ax.set_xlim(-1, 110)


# # 12) Distribution des clients selon l'ancienneté de la relation PP /PM par business line

# In[493]:

def draw_xbroken_lines(ax1, ax2):
    d = 0.02
    kwargs = {"transform": ax1.transAxes,
              "color": "k",
              "clip_on": False}
    x_span = (1 - d, 1 + d)
    y_span = (1 - d, 1 + d)
    ax1.plot(x_span, y_span, **kwargs)
    ax1.plot(x_span, (-d, +d), **kwargs)
    kwargs.update(transform=ax2.transAxes)
    x_span = (-d, +d)
    y_span = (1 - d, 1 + d)
    ax2.plot(x_span, y_span, **kwargs)
    ax2.plot(x_span, (-d, +d), **kwargs)


def remove_p(x):
    return re.sub("\s*\(.*", "", x)


# In[587]:

var = df_all[
    ["ID client", "Date entree relation affaires", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1"]].drop_duplicates()

# In[588]:

var["Date entree relation affaires"] = pd.to_datetime(var["Date entree relation affaires"], format="%d/%m/%Y")

# In[589]:

var["anciennete"] = 2018 - var["Date entree relation affaires"].dt.year

# In[604]:

type_acteur = "P"
sub = var.loc[var["Type acteur"] == type_acteur]

to_plot = sub[sub.anciennete < 24].anciennete
mean_ = to_plot.mean()
title_ = "Years of relation with P" + type_acteur + "\n (mean {:.1f} years)".format(mean_)
ax = to_plot.plot.hist(title=title_, alpha=0.65, bins=50)
ax.axvline(mean_, ls="--")
ax.set_ylabel("Number of person")
ax.set_xlabel("Years of relation")

# In[606]:

df = sub
col_branch = "DESCRIPTION_OBJET_HIERARCHIE_1"
branches = ('BRANCH NETWORK', "CIB", 'WEALTH MANAGEMENT')
kwargs = {"title": "test", "sujet": "test2"}
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)
current_axe = -1
for branch in branches:
    current_axe = current_axe + 1
    ax = axes[current_axe]
    sub_df = df[df[col_branch] == branch]
    title = "%s (P%s)" % (branch, type_acteur)
    to_plot = sub_df[sub_df.anciennete < 24].anciennete
    ax = to_plot.plot.hist(title=title_, alpha=0.65, bins=50, ax=ax)
    mean_ = to_plot.mean()
    title_ = "Years of relation with P" + type_acteur + "\n (mean {:.1f} years)".format(mean_)
    ax.set_title(title_)
    ax.axvline(mean_, ls="--")
    ax.set_ylabel("Number of person")
    ax.set_xlabel("Years of relation")

# In[608]:

type_acteur = "M"
sub_df = var.loc[var["Type acteur"] == type_acteur]
title_ = "Anciennete des P" + type_acteur
to_plot = sub_df[sub_df.anciennete < 24].anciennete
ax = to_plot.plot.hist(title=title_, alpha=0.65, bins=50)
mean_ = to_plot.mean()
title_ = "Years of relation with P" + type_acteur + "\n (mean {:.1f} years)".format(mean_)
ax.set_title(title_)
ax.axvline(mean_, ls="--")
ax.set_ylabel("Number of person")
ax.set_xlabel("Years of relation")

# In[612]:

type_acteur = "M"
sub = var.loc[var["Type acteur"] == type_acteur]
df = sub
col_branch = "DESCRIPTION_OBJET_HIERARCHIE_1"
branches = ('BRANCH NETWORK', "CIB", 'WEALTH MANAGEMENT')
kwargs = {"title": "test", "sujet": "test2"}
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)
current_axe = -1
for branch in branches:
    current_axe = current_axe + 1
    ax = axes[current_axe]
    sub_df = df[df[col_branch] == branch]
    title = "%s (P%s)" % (branch, type_acteur)
    to_plot = sub_df[sub_df.anciennete < 24].anciennete
    ax = to_plot.plot.hist(title=title_, alpha=0.65, bins=50, ax=ax)
    mean_ = to_plot.mean()
    title_ = "Years of relation with P" + type_acteur + "\n (mean {:.1f} years)".format(mean_)
    ax.set_title(title_)
    ax.axvline(mean_, ls="--")
    ax.set_ylabel("Number of person")
    ax.set_xlabel("Years of relation")

# # 13) Distribution des clients selon l'ancienneté d’immatriculation des PM par business line -> on n'a pas la donnée ?

# In[509]:

var = df_all[["ID client", "Date entree relation affaires", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1",
              "AGE"]].drop_duplicates()

# In[510]:




# In[886]:

df_all["Type acteur"].value_counts()

# In[894]:

a = df_all[df_all["TYPE_ROLE"].isin(["MAN", "REP"])]["ID client"].drop_duplicates()

# # 13 ) répartition des PP par nationalité (effectifs par nom de pays)

# In[735]:

var = df_all[["ID client", "Nationalite 1", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1"]].drop_duplicates()
pp = get_pp(var)
pivot = pp.pivot_table(index="Nationalite 1", values="ID client", aggfunc=pd.Series.nunique, margins=True)
pivot.sort_values("ID client", ascending=False).plot.hist()

# In[745]:

pivot.sort_values("ID client", ascending=False)

# # 14) Répartition des PM par pays d'immatriculation  (effectifs par nom de pays)

# In[513]:

var = df_all[["ID client", "Pays immatriculation", "Type acteur"]].drop_duplicates()
pm = get_pm(var)
pivot = pm.pivot_table(index="Pays immatriculation", values="Type acteur", aggfunc=pd.Series.count, margins=True)
pivot.sort_values("Type acteur", ascending=False)[90:120]

# # 15) Distribution des PM selon le chiffre d'affaires

# In[514]:

risque_pays = get_df("risque_pays")
var = df_all[["ID client", "Type acteur", "Pays residence fiscale", "Pays immatriculation"]].drop_duplicates()
var["Pays immatriculation"] = var["Pays immatriculation"].fillna("NC")
var = pd.merge(var, risque_pays, left_on="Pays immatriculation", right_on="code bil", how="left")
var["risque watchlist"] = var["risque watchlist"].fillna("NC")
var = get_pm(var)
tab = var.pivot_table(index=["Type acteur"], columns="risque watchlist", values="ID client", aggfunc=pd.Series.nunique,
                      margins=True)
tab.applymap(format_nombre)

# In[515]:

tab = var.pivot_table(index=["Type acteur"], columns="risque watchlist", values="ID client", aggfunc=pd.Series.nunique,
                      margins=False)

tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %")


# # 16) Résidence fiscale des UBO (top 10 pays à risque élevé et effectifs correspondant)

# In[29]:

def get_ubo(df, col_de_test="origine", valeur_cherchee="UBO"):
    return get_subset(df, col_de_test, valeur_cherchee)


# In[517]:

risque_pays = get_df("risque_pays")
var = df_all[["ID client", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1", "Pays residence fiscale",
              "origine"]].drop_duplicates()
var["Pays residence fiscale"] = var["Pays residence fiscale"].fillna("NC")
var = pd.merge(var, risque_pays, left_on="Pays residence fiscale", right_on="code bil", how="left")
var["risque watchlist"] = var["risque watchlist"].fillna("NC")
var = get_ubo(var)
tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"], columns="risque watchlist",
                      values="ID client", aggfunc=pd.Series.nunique, margins=True)
tab.applymap(format_nombre)

# ## 16.1) top 10 des pays ä risques

# In[847]:

var = df_all[["ID client", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1", "Pays residence fiscale",
              "origine"]].drop_duplicates()
# Fill residence fiscale vide
var["Pays residence fiscale"] = var["Pays residence fiscale"].fillna("NC")
# Merge risque pays
var = pd.merge(var, risque_pays, left_on="Pays residence fiscale", right_on="code bil", how="left")
# Fill risque vide
var["risque watchlist"] = var["risque watchlist"].fillna("NC")
# filtre sur pays C
var2 = var.loc[var["risque watchlist"] == "C"]
# nb de clients uniaue
var2 = get_ubo(var2)
var3 = var2.pivot_table(index=["risque watchlist", "code bil", "pays watchlist"], columns="Type acteur",
                        values="ID client", aggfunc=pd.Series.nunique, margins=True)

var4 = var3.sort_values("All", ascending=False)[:10]
var4.applymap(format_nombre)

# In[854]:

var5 = var4.reset_index()

# In[857]:

var5.index = var5["code bil"]

# In[862]:

var5[["code bil"]].join(classement_pays_iso3_par_liste).fillna("")

# In[21]:

classement_pays_iso3_par_liste = get_df("classement_pays_iso3_par_liste")
classement_pays_iso3_par_liste.index = classement_pays_iso3_par_liste["ISO 3"]

# # 17) Pays de nationalité des UBOs (top 10 pays à risque élevé et effectifs correspondants)

# In[519]:

risque_pays = get_df("risque_pays")

# In[520]:


var = df_all[["ID client", "Type acteur", "Nationalite 1", "origine"]].drop_duplicates()
var["Nationalite 1"] = var["Nationalite 1"].fillna("NC")
var = pd.merge(var, risque_pays, left_on="Nationalite 1", right_on="code bil", how="left")
var["risque watchlist"] = var["risque watchlist"].fillna("NC")
var = get_ubo(var).drop_duplicates()

# In[521]:

tab = var.pivot_table(index=["risque watchlist"], columns="Type acteur", values="ID client", aggfunc=pd.Series.nunique,
                      margins=True)
s = tab.sort_values("All", ascending=False)
s.applymap(format_nombre)

# In[522]:

tab = var.pivot_table(index=["nom pays iso fr"], columns="Type acteur", values="ID client", aggfunc=pd.Series.nunique,
                      margins=True)
s = tab.sort_values("All", ascending=False)
s.applymap(format_nombre)

# In[523]:

var2 = var.loc[var["risque watchlist"] == "C"]
# nb de clients uniaue
var2 = get_ubo(var2).drop_duplicates()
var3 = var2.pivot_table(index=["risque watchlist", "code bil", "pays watchlist"], columns="Type acteur",
                        values="ID client", aggfunc=pd.Series.nunique, margins=True)
var4 = var3.sort_values("All", ascending=False)[:10]
var4.applymap(format_nombre)


# # 18) Ratio UBO par personnes morale et personne morale par UBO
#

# In[140]:

def draw_ybroken_lines(ax1, ax2):
    d = 0.02
    kwargs = {"transform": ax1.transAxes,
              "color": "k",
              "clip_on": False}
    x_span = (-d, +d)
    y_span = (-d, +d)
    ax1.plot(x_span, y_span, **kwargs)
    ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)
    kwargs.update(transform=ax2.transAxes)
    x_span = (-d, +d)
    y_span = (1 - d, 1 + d)
    ax2.plot(x_span, y_span, **kwargs)
    ax2.plot(y_span, y_span, **kwargs)


# In[151]:

ubos = get_ubo(df_all)
ubos = ubos.drop_duplicates(subset=["Contrat de base", "ID titulaire", "ID client"])

# In[152]:

tab = ubos.groupby(["ID client"])[["ID titulaire"]].size()
tab2 = tab.value_counts()
fig = plt.figure()
plt.scatter(x=tab2.index.values, y=tab2.values)
fig.suptitle("Nb de PM par UBO", fontsize=20)
ax = plt.gca()
ax.set_xlabel("Nb  de PM")
ax.set_ylabel("Nb  de UBO")

# # on cherche les UBO avec beacoup de PM => ce sont des acteurs avec beaucoup de contrats

# In[143]:

tab.sort_values()[-10:]

# In[160]:

test = df_all[df_all["ID client"].isin(tab.sort_values()[-10:].index)][
    ["ID client", "DESCRIPTION_OBJET_HIERARCHIE_1", "Contrat de base", "Type acteur", "ID titulaire",
     "Secteur activites", "Total actifs sous gestion"]]
test.sample(10)

# # Nb d'ubo par contrat

# In[153]:

tab = ubos.groupby(["Contrat de base"])[["ID client"]].size()
tab2 = tab.value_counts()
fig = plt.figure()
plt.scatter(x=tab2.index.values, y=tab2.values)
fig.suptitle("Nb d'ubo par contrat", fontsize=20)
ax = plt.gca()
ax.set_xlabel("Nb  de PM")
ax.set_ylabel("Nb  de UBO")

# # nb de PM par UBO -> zoom

# In[154]:

tab = ubos.groupby(["ID client"])[["ID titulaire"]].size()

# tab2 = tab.value_counts()[2:25]
tab2 = tab.to_frame()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8), sharex=True, )
fig.suptitle(u"Nb de PM par UBO  - zoom ", fontsize=20)
sns.countplot(x=0, data=tab2, ax=ax1)
sns.countplot(x=0, data=tab2, ax=ax2)
ax1.set_ylim(100, 13000)
ax1.set_xlim(0, 25)
ax2.set_ylim(0, 100)
ax2.set_xlim(0, 25)
ax1.set_xlabel("")
ax1.set_ylabel("")
draw_ybroken_lines(ax1, ax2)
ax1.spines["bottom"].set_visible(False)
ax2.spines["top"].set_visible(False)
# ax1.spines["top"].set_visible(False)
# ax1.scatter(tab2.index.values, tab2.values)
# ax2.scatter(x=tab2.index.values, y=tab2.values)


# # Nb d'UBO par PM

# In[155]:

tab = ubos.groupby(["ID titulaire"])[["ID client"]].size()
tab2 = tab.value_counts()
fig = plt.figure()
plt.scatter(x=tab2.index.values, y=tab2.values)
fig.suptitle("Nb d'UBO par PM", fontsize=20)
ax = plt.gca()
ax.set_xlabel("Nb  de UBO")
ax.set_ylabel("Nb  de PM")

# In[156]:

tab.sort_values()[-10:]

# In[159]:

test = df_all[df_all["ID titulaire"].isin(tab.sort_values()[-10:].index)][
    ["ID client", "DESCRIPTION_OBJET_HIERARCHIE_1", "Contrat de base", "Type acteur", "ID titulaire",
     "Secteur activites", "Total actifs sous gestion"]]
test.sample(10)

# In[135]:

tab = ubos.groupby(["ID titulaire"])[["ID client"]].size()
# tab2 = tab.value_counts()[2:25]
tab2 = tab.to_frame()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8), sharex=True, )

fig.suptitle(u"Nb de d'UBO par PM  - zoom ", fontsize=20)

sns.countplot(x=0, data=tab2, ax=ax1)
sns.countplot(x=0, data=tab2, ax=ax2)
ax1.set_ylim(100, 12000)
ax1.set_xlim(0, 25)
ax2.set_ylim(0, 100)
ax2.set_xlim(0, 25)
ax1.set_xlabel("")
ax1.set_ylabel("")
draw_ybroken_lines(ax1, ax2)
ax1.spines["bottom"].set_visible(False)
ax2.spines["top"].set_visible(False)
# ax1.spines["top"].set_visible(False)
# ax1.scatter(tab2.index.values, tab2.values)
# ax2.scatter(x=tab2.index.values, y=tab2.values)


# # 19) Répartition des comptes numérotés par business line

# In[531]:

var = df_all[["Contrat de base", "Indicateur Compte Numerote", "DESCRIPTION_OBJET_HIERARCHIE_1"]].drop_duplicates()

var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1"],
                columns="Indicateur Compte Numerote",
                values="Contrat de base", aggfunc="count")

# # 20) Répartition des PP et PM par  secteur d'activité sensible et par business line (Top 10 activités sensibles et effectifs correspondants)
#

# In[162]:

activites = get_df("Classification_de_risque_activite_NACE_1")

# In[163]:

s1 = activites.drop_duplicates(["Code NACE", "Classification"]).copy()

# In[164]:

s1.Classification = s1.Classification.astype("category", categories=["other", "l", "m-", "m+", "h-", "h+"],
                                             ordered=True)


# In[165]:

def max_classif(group):
    return group["Classification"].max()


nace = s1.groupby("Code NACE").apply(max_classif).reset_index()

# In[166]:

nace.rename(columns={0: "Classification"}, inplace=True)

# In[171]:

df_all_0 = df_all[df_all["ID titulaire"] == df_all["ID client"]]
print(df_all_0.shape)
df_all_0 = pd.merge(df_all_0, nace, left_on="Code NACE", right_on="Code NACE", how="left")
print(df_all_0.shape)
df_all_0 = df_all_0[["Contrat de base", "ID titulaire", "Code NACE", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1",
                     "Classification"]].drop_duplicates()
print(df_all_0.shape)
df_all_0["Classification"] = df_all_0["Classification"].fillna("NC")
tab = df_all_0.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"], columns="Classification",
                           values="Contrat de base", aggfunc=pd.Series.nunique, margins=True)
tab.fillna(0)
tab.applymap(format_nombre)

# In[550]:

tab = df_all_0.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"], columns="Classification",
                           values="Contrat de base", aggfunc=pd.Series.nunique, margins=False)
tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %" if x > 0 else "0 %")

# In[557]:

tab = df_all_0.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1", "Type acteur"], columns="Classification",
                           values="Contrat de base", aggfunc=pd.Series.nunique, margins=False)

tab = try_drop_all(tab)
tab = pct_by_group(tab, "Type acteur")
tab
# tab.applymap(lambda x: str(int(x))+" %" if x>0 else "0 %")


# In[876]:

# var = pd.merge(df_all, activites, left_on="Code NACE", right_on="Code NACE", how="left")
# var = var[["ID client", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1", "Classification", "Code NACE", "Description"]].drop_duplicates()
# var["Classification"] = var["Classification"].fillna("NC")
# filtre sur pays C
var2 = df_all_0.loc[df_all_0["Classification"] == "h+"]
# nb de clients uniaue
var3 = var2.pivot_table(index=["Classification", "Code NACE"], columns="Type acteur", values="ID titulaire",
                        aggfunc=pd.Series.nunique, margins=True)

var4 = var3.sort_values("All", ascending=False)[:10]
var4.applymap(format_nombre)

# # 21) Répartition des PM non-résidentes par type de structure juridique

# In[108]:

var = get_pm(df_all)

# In[117]:

var = var.loc[~ (var["Pays residence fiscale"] == "LUX")]

# # nb de pm par type de structure

# In[120]:

var = var[["Type de structure", "ID client"]].drop_duplicates()

# In[123]:

pd.DataFrame(var["Type de structure"].value_counts())

# In[82]:

s = df_all[["Type de structure"]]

# In[83]:

pm = get_pm(df_all)

# In[84]:

s = pm["Type de structure"]

# In[85]:

s.value_counts()

# # 22) Répartition des clients PP par canal d'entrée en relation par business line

# # 22.1) sur pp

# In[877]:

var = get_pp(df_all)
var = var[["ID titulaire", "ID client", "Contrat de base", "Type introduction client",
           "DESCRIPTION_OBJET_HIERARCHIE_1"]]  # .drop_duplicates()
var = var[var["ID titulaire"] == var["ID client"]]
var["Type introduction client"].value_counts(dropna=False)
tab = var.pivot_table(index=["Type introduction client"], columns="DESCRIPTION_OBJET_HIERARCHIE_1",
                      values="Contrat de base", aggfunc=pd.Series.count, margins=True)
tab.fillna(0)
tab.applymap(format_nombre)

# In[211]:

var = get_pp(df_all)
var = var[["ID titulaire", "ID client", "Contrat de base", "Type introduction client",
           "DESCRIPTION_OBJET_HIERARCHIE_1"]]  # .drop_duplicates()
var = var[var["ID titulaire"] == var["ID client"]]
var["Type introduction client"].value_counts(dropna=False)
tab = var.pivot_table(index=["Type introduction client"], columns="DESCRIPTION_OBJET_HIERARCHIE_1",
                      values="Contrat de base", aggfunc=pd.Series.count, margins=False)
tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %" if x > 0 else "0 %")

# # 22.2) sur pm

# In[229]:

var = get_pm(df_all)
var = var[var["ID titulaire"] == var["ID client"]]
var = var[
    ["ID titulaire", "Contrat de base", "Type introduction client", "DESCRIPTION_OBJET_HIERARCHIE_1"]].drop_duplicates()
tab = var.pivot_table(index=["Type introduction client"], columns="DESCRIPTION_OBJET_HIERARCHIE_1",
                      values="Contrat de base", aggfunc=pd.Series.count, margins=True)
tab.fillna(0)
tab.applymap(format_nombre)

# In[231]:

tab = var.pivot_table(index=["Type introduction client"], columns="DESCRIPTION_OBJET_HIERARCHIE_1",
                      values="Contrat de base", aggfunc=pd.Series.count, margins=False)
tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %" if x > 0 else "0 %")

# # test

# In[884]:

df_all[df_all["Type introduction client"] == "INTERMEDIAIRE"]["TYPE_ROLE"].value_counts()

# # 23) Répartition des personnes morales par finalité économique (structure patrimoniale versus structure opérationnelles) de la ligne métier wealth management

# In[231]:

finalites = get_df("finalite_des_structures")

# In[240]:

pm = get_pm(df_all)

# In[241]:

var = pd.merge(pm, finalites, left_on="Type de structure", right_on="type de structure", how="left")

# In[242]:

var = var[["ID client", "type de structure", "DESCRIPTION_OBJET_HIERARCHIE_1", "finalite"]].drop_duplicates()

# In[255]:

tab = var.pivot_table(index=["finalite", "type de structure"], columns=["DESCRIPTION_OBJET_HIERARCHIE_1"],
                      values=["ID client"], aggfunc=pd.Series.count, margins=True)
tab = tab.fillna(0)

tab = tab.sort_values(("ID client", "All"), ascending=False)
tab.applymap(format_nombre)

# # 24) Nombre des contrats de base gérés par des mandataires par business line, par PP et PM

# In[279]:

# "ID client", "Contrat de base", ,
var = df_all.loc[df_all["LIBELLE_FR"] == "MANDATAIRE", ["ID client", "Contrat de base", "Type acteur",
                                                        "DESCRIPTION_OBJET_HIERARCHIE_1"]].drop_duplicates()
pd.crosstab(var["DESCRIPTION_OBJET_HIERARCHIE_1"], var["Type acteur"]).applymap(format_nombre)

# In[282]:

tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1"], columns="Type acteur", values="Contrat de base",
                      aggfunc=pd.Series.count, margins=True)
tab

# In[278]:

tab = var.pivot_table(index=["DESCRIPTION_OBJET_HIERARCHIE_1"], columns="Type acteur", values="Contrat de base",
                      aggfunc=pd.Series.count, margins=False)
tab2 = tab.div(tab.sum(axis=1), axis=0) * 100
tab2.applymap(lambda x: str(int(x)) + " %" if x > 0 else "0 %")

# # 29) Distribution du nombre de CdB par mandataires

# In[582]:

var = df_all.loc[df_all["LIBELLE_FR"] == "MANDATAIRE"]
tab = var.groupby(["ID client"])[["Contrat de base"]].size()
tab2 = tab.value_counts()
fig = plt.figure()
plt.scatter(x=tab2.index.values, y=tab2.values)
fig.suptitle("Nb de Contrat par Mandataires", fontsize=20)
ax = plt.gca()
ax.set_xlabel("Nb  de Contrats")
ax.set_ylabel("Nb  de Mandataires");

# In[583]:

# tab  = ubos.groupby(["ID client"])[["ID titulaire"]].size()

# tab2 = tab.value_counts()[2:25]
tab2 = tab.to_frame()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8), sharex=True, )
fig.suptitle(u"Nb de Contrat par Mandataires  - zoom ", fontsize=20)
sns.countplot(x=0, data=tab2, ax=ax1)
sns.countplot(x=0, data=tab2, ax=ax2)
ax1.set_ylim(500, 40000)
ax1.set_xlim(0, 25)
ax2.set_ylim(0, 500)
ax2.set_xlim(0, 25)
ax1.set_xlabel("")
ax1.set_ylabel("")
draw_ybroken_lines(ax1, ax2)
ax1.spines["bottom"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax2.set_xlabel("Nb de contrat")
ax2.set_ylabel("Nb de Mandataires")
# ax1.spines["top"].set_visible(False)
# ax1.scatter(tab2.index.values, tab2.values)
# ax2.scatter(x=tab2.index.values, y=tab2.values)


# In[584]:

var = df_all.loc[df_all["LIBELLE_FR"] == "MANDATAIRE"]
tab = var.groupby(["Contrat de base"])[["ID client"]].size()
tab2 = tab.value_counts()
fig = plt.figure()
plt.scatter(x=tab2.index.values, y=tab2.values)
fig.suptitle("Nb de Mandataires par Contrat", fontsize=20)
ax = plt.gca()
ax.set_xlabel("Nb  de Mandataires")
ax.set_ylabel("Nb  de Contrats");

# In[585]:

tab2 = tab.to_frame()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8), sharex=True, )
fig.suptitle(u"Nb de Mandataires par Contrat  - zoom ", fontsize=20)
sns.countplot(x=0, data=tab2, ax=ax1)
sns.countplot(x=0, data=tab2, ax=ax2)
ax1.set_ylim(500, 40000)
ax1.set_xlim(0, 25)
ax2.set_ylim(0, 500)
ax2.set_xlim(0, 25)
ax1.set_xlabel("")
ax1.set_ylabel("")
ax2.set_ylabel("Nb de contrat")
ax2.set_xlabel("Nb de Mandataires")
draw_ybroken_lines(ax1, ax2)
ax1.spines["bottom"].set_visible(False)
ax2.spines["top"].set_visible(False)
# ax1.spines["top"].set_visible(False)
# ax1.scatter(tab2.index.values, tab2.values)
# ax2.scatter(x=tab2.index.values, y=tab2.values)


# # suite réunion du 12/04 :

# In[ ]:




# In[29]:


# liste des cdbs non scored


# In[34]:

cdb_rating_non_connu = df_all[df_all["Rating AML calcule"] == "NC"]["Contrat de base"]

# In[41]:

cdb_rating_non_connu.shape

# In[37]:

len(cdb_rating_non_connu.head(100).values

# In[38]:

cdb = get_df("Export_CDB")

# In[48]:

cdb[cdb["Contrat de base"].isin(["10169504"])].head()

# In[ ]:




# # 33) Pays de résidence fiscale des PP et PM dans les pays de la liste grise et noire de l’UE (top 10 pays de la liste noire et effectifs correspondants)

# ## A) on charge les listes pays

# In[795]:

classement_pays_iso3_par_liste = get_df("classement_pays_iso3_par_liste")
classement_pays_iso3_par_liste.index = classement_pays_iso3_par_liste["ISO 3"]

# In[796]:

classement_pays_iso3_par_liste.head()

# In[797]:




# In[802]:

classement_pays_iso3_par_liste.loc["SRB"]

# In[822]:

classement_pays_iso3_par_liste.gafi.value_counts()


# ## B) on réduits aux acteurs équivalents à des titualires

# In[28]:


def get_subsets(df, valeur_cherchee, col_de_test="LIBELLE_FR"):
    import pandas as pd
    assert (type(valeur_cherchee) == list)
    r = []

    for v in valeur_cherchee:
        r.append(get_subset(df, col_de_test, v))

    return pd.concat(r)


# In[699]:

df_all["TYPE_ROLE"].value_counts()

# In[696]:

df_all["LIBELLE_FR"].value_counts()

# In[727]:

main_actors = get_subsets(df_all, ["SET", "PRO", "TRS", "BEN", "CTP", "TITULAIRE", "BENEFICIAIRE ECONOMIQUE"])

# In[728]:

ubos = get_ubo(df_all)
ubos.shape

# In[729]:

main_actors.shape

# In[730]:

local_scope = pd.concat([ubos, main_actors])
local_scope.shape

# In[731]:

local_scope = local_scope.drop_duplicates("ID client")
local_scope.shape

# In[819]:

local_scope["LIBELLE_FR"].value_counts()

# ## C) Nationalité !! On compte les personnes  par type derisque  pays

# In[161]:

1

# In[803]:

var = local_scope[["ID client", "Nationalite 1", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1"]].drop_duplicates()
pp = get_pp(var)
pivot = pp.pivot_table(index="Nationalite 1", values="ID client", aggfunc=pd.Series.nunique, margins=True)
p = pivot.sort_values("ID client", ascending=False)

# In[811]:




# In[808]:

classement_pays_iso3_par_liste

# In[809]:

x = p.join(classement_pays_iso3_par_liste).sort_values("ID client", ascending=False)

# In[810]:

x.shape

# In[813]:

x.reset_index()

# # 34) Pays de résidence fiscale CRS versus pays non CRS des clients (top 10 pays non CRS et effectifs correspondants)

# In[823]:

var = local_scope[
    ["ID client", "Pays residence fiscale", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1"]].drop_duplicates()
pp = get_pp(var)
pivot = pp.pivot_table(index="Pays residence fiscale", values="ID client", aggfunc=pd.Series.nunique, margins=True)
p = pivot.sort_values("ID client", ascending=False)
print(p.shape)
x = p.join(classement_pays_iso3_par_liste).sort_values("ID client", ascending=False)
x.shape

# In[816]:

x.reset_index()

# # 34.1) sur domicile
#

# In[824]:

var = local_scope[["ID client", "Pays domicile", "Type acteur", "DESCRIPTION_OBJET_HIERARCHIE_1"]].drop_duplicates()
pp = get_pp(var)
pivot = pp.pivot_table(index="Pays domicile", values="ID client", aggfunc=pd.Series.nunique, margins=True)
p = pivot.sort_values("ID client", ascending=False)
print(p.shape)
x = p.join(classement_pays_iso3_par_liste).sort_values("ID client", ascending=False)
x.shape

# In[826]:

x.reset_index()

# # 34.2) sur l'immatriculation des PM
#

# In[19]:

pm = get_pm(df_all)

# In[844]:

var = pm[["ID client", "Pays immatriculation"]].drop_duplicates()

pivot = var.pivot_table(index="Pays immatriculation", values="ID client", aggfunc=pd.Series.nunique, margins=True)
p = pivot.sort_values("ID client", ascending=False)
print(p.shape)
x = p.join(classement_pays_iso3_par_liste).sort_values("ID client", ascending=False)
x.shape

# In[846]:

x.reset_index()

# ## 34.3) idem sur Pays secteur d'activite des PM

# In[60]:

risque_pays = get_df("risque_pays")

# In[63]:

risque_pays = get_df("risque_pays")
risque_pays.set_index("iso3", inplace=True)

# In[108]:

col = "Pays secteur activites PM"
var = pm[["ID client", col]].drop_duplicates()
var.set_index(col, inplace=True)
var = var.join(risque_pays)
var.groupby("risque watchlist")["ID client"].count().apply(format_nombre)

# ## 34.4) idem sur Pays secteur d'activite des PP

# In[111]:

pp = get_pp(df_all)
col = "Pays secteur activites PM"
var = pp[["ID client", col]].drop_duplicates()
print(var.shape)
var.fillna("NC", inplace=True)
var.set_index(col, inplace=True)
var = var.join(risque_pays)
var.groupby("risque watchlist")["ID client"].nunique().apply(format_nombre)

# In[112]:

var["risque watchlist"].value_counts(dropna=False).apply(format_nombre)


# In[ ]:



