# coding: utf-8
import pandas as pd


class extra(pd.DataFrame):
    def give_categorical_columns(self, limite=50):
        """
        Retourne la liste des colonnes de la df qui contient moins de 'limite' modalités.

        Parameters :
            limit : int, nombre de modalité limite (exclusif) que doivent avoir les colonnes retournées

        Return:
            Array of strings : each string is a column name

        """
        return [col for col in self.columns if len(self[col].unique()) < limite and "DT_" not in col]

    def histo(self, cols):
        """
        S'appuie sur la df contenue dans l'objet actuel
        Pour chaque colonne :
            \-> Compte le nombre de modalité dans chacune des colonnes
                \-> Crée :
                    \-> un graphique en bar avec ce compte par modalité
                    \-> des graphiques de zoom s'il y a assez de modalités :
        Parameters:
            cols : array of string
                \-> chaque string est un nom de colonne du tableau

        """
        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.style.use('ggplot')
        for col in cols:
            try:
                count_ = self.groupby(col)[col].count()
                count_.sort_values(inplace=True, ascending=False)
                count_.index = [" %s " % x for x in count_.index]

                for kind in ['bar', 'pie'][0:count_.shape[0] - 1]:
                    plt.figure()
                    count_.plot(kind=kind, title="%s - %s valeurs" % (col, count_.shape[0]))
                    if count_.shape[0] > 8:
                        plt.figure()
                        count_[1:5].plot(kind=kind, title="%s - valeurs 2 à 4 " % (col))
                        plt.figure()
                        count_[5:].plot(kind=kind, title="%s - valeurs 4 et plus " % (col))

            except Exception as e:
                print("Pbm sur col [%s] -> %s" % (col, e))

    def get_time_col(self):
        """
        Retourne la liste des colonnes contenant "DT_" dans leur nom.
        """
        return [col for col in self.columns if "DT_" in col]

    @staticmethod
    def timeline(path, col_date, debug=False):
        """
        Créer des graphs de séries temporelles à partir d'un csv :
            - créer une pandas df depuis le chemin
            - trouve les colonnes catégorielles
                - pour chacune
                    \-> crée un graphique pour chaque valeur de la colonne
                    \-> enregistre le graphique sur le disque
        Parameters:
            path : string, chemin vers le csv de datframe
            col_date : string, colonne de date sur laquelle se baser pour le temps
            debug : boolean

        Return: None

        """
        import os
        table = extra(pd.read_csv(path, delimiter=useful.find_delimiter(path)))
        timeline2(table, path, col_date, debug=False)

    @staticmethod
    def timeline2(df, path, col_date, debug=False):
        """
        Créer des graphs de séries temporelles à partir d'un csv :
            - créer une pandas df depuis le chemin
            - trouve les colonnes catégorielles
                - pour chacune
                    \-> crée un graphique pour chaque valeur de la colonne
                    \-> enregistre le graphique sur le disque
        Parameters:
            path : string, chemin vers le csv de datframe
            col_date : string, colonne de date sur laquelle se baser pour le temps
            debug : boolean

        Return: None

        """
        import os

        test2 = extra(df)

        modalities, binary, continuous, dates = extra_pandas.select_columns_based_on_names(test2)

        cat_col = test2.give_categorical_columns()

        # extra_pandas.enforce_date(test2, col_date, "%d%b%Y:00:00:00", debug=True)
        index = test2[col_date]
        nom_table = path[path.rfind("/") + 1:path.rfind(".")]
        for col in cat_col:
            if debug: print("col = ", col)
            categories = list(test2[col].value_counts().keys())
            if debug: print("categories = ", categories)
            for cat in categories:
                test5 = test2[col]
                test5.index = index
                test6 = pd.DataFrame(test5)
                test6["date"] = test6.index
                test6["one"] = 1
                print("cat=", cat)
                year_mini = 2013
                year_maxi = 2016
                maxi1 = test6[test6[col] == cat]
                vrai_maxi = maxi1["%s" % year_mini:"%s" % year_maxi].groupby("date").count()['one'].max()
                maxi = vrai_maxi * 1.05
                mini = vrai_maxi * 0.05

                # for year in range(2014,2017):
                try:
                    plt.figure(figsize=(20, 5))
                    n1 = test6["%s" % year_mini:"%s" % year_maxi]
                    n2 = n1[n1[col] == cat]
                    n3 = n2.groupby("date").count()
                    n4 = n3.resample('d')
                    nom_table_utf8 = to_Str(nom_table)
                    col_utf8 = to_Str(col)
                    cat_utf8 = to_Str(cat)
                    col_date_utf8 = to_Str(col_date)
                    title_ = "TABLE_[%s]_COLONNE_[%s]_CATEGORIE_[%s]_nombre_par_jour_par_date_de_[%s]" % (
                    nom_table_utf8, col_utf8, cat_utf8, col_date_utf8)
                    ax = n4["one"].sum().plot(style='o', title=title_)
                    ax.set_axis_bgcolor('w')
                    ax.set_ylim(-mini, maxi)

                    ax.plot()
                    title_ = title_.replace("/", "").replace(" ", "_")
                    savedir = "./../images/table_%s/col_%s/" % (
                    nom_table_utf8.replace("/", "").replace(" ", "_"), col_utf8.replace("/", "").replace(" ", "_"))
                    print(savedir)
                    try:
                        os.makedirs(savedir)
                    except OSError:
                        if not os.path.isdir(savedir):
                            raise
                    plt.savefig(savedir + "%s.jpg" % title_)
                    plt.show()

                    # ax.set_ylim(maxi)
                except Exception as e:
                    print("e=", e)
                    pass


