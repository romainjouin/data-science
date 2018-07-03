# -*- coding: utf-8 -*-
def analyse_df(df):
    import pandas as pd
    r = pd.DataFrame()
    for col in df.columns:
        try:
            r = r.append(analyse_column(df[col], col))
        except: pass

    return r
def analyse_column(X, nom_col="coucou"):
    """
    Calcul des statistiques descriptives sur une série (min, max, moyenne).

    Input:
        X : pandas series
            \-> supposed to be numeric
    Output: str

    """
    import pandas as pd
    try:
        df              = pd.DataFrame()
        df["nb_ligne"]  = pd.Series(X.shape[0])
        df["min"]       = X.min()
        df["max"]       = X.max()
        df["min_index"] = X.index.min()
        df["max_index"] = X.index.max()
        df["mean"]      = X.mean()
        df["median"]    = X.median()


        try     :df["var"]= X.var()
        except Exception as e  : print("pbm var : %s"%e)
        try     :df["ecart_type"]= X.std()
        except Exception as e  : print("pbm srtd : %s"%e)
        try     :df["EcAbs"]= EcAbs(X)
        except Exception as e  : print("pbm Ecabs : %s"%e)
        try     :df["Kolmogorov stat"], df["Kolmogorov pvalue"]= Kolmogorov(X)
        except Exception as e  : print("pbm Kolmogorov : %s"%e)
        try     : df["Indice_de_Gini"] = Indice_de_Gini(X)
        except Exception as e  : print("pbmm gini :  %s" %e)

    except Exception as e:
        print("analyse_column: pbm = {%s}%s" % (e, eol))
    df.index = [nom_col]

    return df
def calculate_unique_by_files(array_path: "tableau") -> "pd.df":
    """
    Pour chaque fichier passer en paramètre, calcul calculate_unique_null_not_null
    et renvoie une df avec toutes les infos.
    return : df
    """
    import pandas as pd
    result = False
    for path in array_path:
        try:
            df = calculate_unique_by_file(path)
            if isinstance(result, bool):
                result = df
            else:
                result = result.append(df)
        except Exception as e:
            print(path)
            print(e)
            df = False
            pass
    return result
def calculate_unique_by_file(csv_path: "str", **kwg) -> "pd.df":
    """
    Créer une df et Appelle calculate_unique_null_not_null dessus.
    return : df
    """
    import pandas as pd
    from jr_data_science.functions_pour_analyser_des_df import calculate_unique_null_not_null
    df = get_df(csv_path, **kwg)
    df = calculate_unique_null_not_null(df)
    df["file"] = csv_path
    df["column"] = df.index
    return df
def get_df(csv_path:"str", sep:"bool"=False, index_col:"bool"=False)->"df":
    """
    Renvoie une dataframe.
    """
    import pandas as pd
    from jr_data_science.functions_de_decouverte_de_fichiers import find_delimiter
    if not sep:
        sep = find_delimiter(csv_path)
    if not index_col:
        index_col = None
    df  = pd.DataFrame.from_csv(csv_path, index_col=index_col, sep=sep)
    return df
def tendances_centrales(Y, eol="\n"):
    """
    Retourne une chaine de caractère décrivant la tendance centrale d'une série

    Input : pandas series

    Ouput : string
    """
    moyenne, mediane = Y.mean(),  Y.median()

    try:
        mode =  Y.mode()
    except:
        mode = False

    return moyenne, mediane , mode
def dispersion(X, eol="\n"):
    """
    Retourne une chaine de caractère décrivant la dispersion d'une série

    Input : pandas series

    Ouput : string

    """

    to_print  = "Dispersion%s"%eol
    to_print  += "Variance : %.2f%s"%(X.var(), eol)
    to_print  += "Ecart type : %.2f%s"%(X.std(), eol)
    to_print  += "Etendue : [%.2f, %.2f]%s"%(X.min(), X.max(), eol)
    to_print  += "Ecart absolu moyen : %s %s"%(EcAbs(X), eol)
    return to_print
def Indice_de_Gini(Y):
    """
    Retourne une chaine de caractère décrivant l'indice de gini' d'une série (concentration)

    Input : pandas series

    Ouput : string

    """

    return gini(Y)
def gini(list_of_values):
    """
    Calcul l'indice de gini d'une série

    Input : pandas series

    Ouput : float

    """
    sorted_list = sorted(list_of_values)
    height, area = 0, 0
    for value in sorted_list:
        height += value
        area += height - value / 2.
        fair_area = height * len(list_of_values) / 2

    return (fair_area - area) / float(fair_area)
def Kolmogorov(X):
    """
    Calcul le test de Kolmogorov

    Input : pandas series

    Ouput : string

    """
    from scipy import stats
    r = stats.kstest(X, 'norm')
    print (r)
    return r
def EcAbs(L):
    """
    Calcul de l'écart absolu moyen
    L : np.ndarray
    Ouput : string
    """
    import numpy as np
    if isinstance(L, np.ndarray) :
        L[np.isnan(L)] = L[~np.isnan(L)].mean()
    m = L.sum() / len(L)
    M = [abs(x - m) for x in L]
    EcAbs_ = sum(M, 0.0) / len(M)

    return EcAbs_
def smooth(x,window_len=125,window='hamming'):
    """
    Smooth a serie thanks to hamming method.
    """
    if x.ndim != 1:
            raise Exception(ValueError, "smooth only accepts 1 dimension arrays.")
    if x.size < window_len:
            raise Exception(ValueError, "Input vector needs to be bigger than window size.")
    if window_len<3:
            return x
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise Exception(ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")
    s=np.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
    if window == 'flat': #moving average
            w=np.ones(window_len,'d')
    else:
            w=eval('np.'+window+'(window_len)')
    y=np.convolve(w/w.sum(),s,mode='same')
    return y[window_len:-window_len+1]
def MSE(target, predictions):
    """
    Test predictor quality with Mean Square Error
    input :
        target : array of real values
        prediction : array of predicted values
    """
    squared_deviation = np.power(target-predictions, 2)
    return np.mean(squared_deviation)
def MAD(target, predictions):
    """
    Function to test predictor quality : Return Mean Average Deviation
    input :
        target : array of real values
        prediction : array of predicted values
    """
    absolute_deviation = np.abs(target-predictions)
    return np.mean(absolute_deviation)
def proba(ar):
    """
    Calculate the probability of each element in an array.
    Param :
        ar : array of value
    Return :
        dictionnary : [value : proba]

    """
    values = set(ar)
    nb = len(ar)
    print(nb)
    proba = [ar.count(v)/nb for v in values]
    return dict(list(zip(values, proba)))
def RunLinearModel(data, cible, temps ):
    import statsmodels.formula.api as smf
    import numpy as np
    import pandas
    print(cible in data.columns)
    print(temps in data.columns)
    requete = "%s ~ %s"%(cible, temps)
    model = smf.ols(requete, data=data)
    results = model.fit()
    return model, results
def get_needed_sample_size(original_pop, accepted_error=0.05):
    """
    Calculate Bienayme tchebiechef minimum sample size to get a defined acceptable error rate out of an original population size.
    inputs :
        original_pop : size of the pop
        accepted_error : max error we want to have
    """
    a = 1.96**2
    b = accepted_error**2
    c = a * original_pop
    e = original_pop-1
    d = a+b*e
    return  c/d
def get_confidence(original_pop, sample_size):
    """
    According to a reference population size and a test sample size, return the confidence we can have on the result.

    inputs :
        original_pop : size of the pop

    """

    from math import sqrt
    x = 1.96**2
    a = x * original_pop
    b = (original_pop-1) * sample_size * x
    c = float(a)/b
    d = sqrt(c)
    return  float(d)
def min_max(time_serie):
    """
    return a tuple with the min and max of time serie index
    """
    return (time_serie.index.min(), time_serie.index.max())
def reject_outliers(data, m=2.):
    import numpy as np
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    return data[s < m]
def get_outliers(data, m=2.):
    import numpy as np
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    return data[s > m]
def frange(start, stop, step):
    """
    Create an array containing numbers from [start] to [stop] with a step of [step]

    Parameters:
        start: int
        stop : int
        step : int

    Return:
        r : array of int
    """
    r = [start]
    i = start
    while i < stop:
        i += step
        r.extend([i])
    return r
