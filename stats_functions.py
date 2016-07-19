# -*- coding: utf-8 -*-
__author__ = 'nouveau'
def analyse_column(X, eol="\n"):
    """
    Calcul des statistiques descriptives sur une série (min, max, moyenne).

    Input:
        X : pandas series
            \-> supposed to be numeric
    Output: str

    """
    try:
        to_print  ="-"*15+"%s"%eol
        to_print  += "Quantitatif"
        to_print  += "shape : %s%s"%(X.shape, eol)
        to_print  += "min : %s%s"%(X.min(), eol)
        to_print  += "max : %s%s"%(X.max(), eol)
        to_print  += "min index: %s%s"%(X.index.min(), eol)
        to_print  += "max index: %s%s"%(X.index.max(), eol)

    except Exception as e:
        print "analyse_column: pbm = {%s}%s"%(e, eol)
    try: to_print  += tendances_centrales(X, eol)
    except Exception as e: print "analyse_column, analyse centrale error = %s"%e
    try : to_print  += dispersion(X, eol)
    except Exception as e: print "analyse_column, dispersion error = %s"%e

    try : to_print  += concentration(X, eol)
    except Exception as e: print "analyse_column, concentration error = %s"%e

    try : to_print  += test_lois(X, eol)
    except Exception as e: print "analyse_column, test_loiserror = %s"%e

    try : to_print  += EcAbs(X.values, eol)
    except Exception as e: print "analyse_column, EcAbs(X.values) error = %s"%e


    return to_print
def tendances_centrales(Y, eol="\n"):
    """
    Retourne une chaine de caractère décrivant la tendance centrale d'une série

    Input : pandas series
    
    Ouput : string
    """

    to_print  = "Tendances centrales%s"%eol
    to_print  += "mean : %.2f %s"%(Y.mean(), eol)
    to_print  += "median : %.2f%s"%(Y.median(), eol)
    try:
        to_print  += "mode : %.2f%s"%(Y.mode(), eol)
    except:
        to_print  += "mode : undetermined %s"%(eol)

    return to_print
# In[609]:
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

def concentration(Y, eol="\n"):
    """
    Retourne une chaine de caractère décrivant l'indice de gini' d'une série

    Input : pandas series
    
    Ouput : string

    """    
    to_print  = "Concentration%s"%eol
    to_print  += "Indice de Gini : %.2f%s"%(gini(Y), eol)
    return to_print

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

def test_lois(X, eol="\n"):
    """
    Calcul le test de Kolmogorov

    Input : pandas series
    
    Ouput : string

    """
    from scipy import stats
    to_print   = "Loi (Kolmogorov)%s"%eol
    a,b        = stats.kstest(X, 'norm')
    to_print  += "norm = (%.2f, %.2f)%s" % (a,b, eol)
    return to_print

def EcAbs(L, eol="\n"):
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
    to_print  = "Ecart Absolu moyen%s"%eol
    to_print  += "%s%s"%(EcAbs_, eol)
    return to_print


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
    print nb
    proba = [ar.count(v)/nb for v in values]
    return dict(zip(values, proba))

def RunLinearModel(data, cible, temps ):
    import statsmodels.formula.api as smf
    import numpy as np
    import pandas
    print cible in data.columns
    print temps in data.columns
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
