def get_n_indices_set(df, n,  classe, colonne = -1):
    """
        Create an array of len(n) dataset containing lines number (ie defining datasets)
        
        df      : serie
        n       : number of wanted datasets
        classe  : value wanted in the serie
        colonne : useless ?
        
        Return a shuffled array of indices.
    """
    import random
    import numpy as np
    try:
        datasets = []
        for i in range(n):
            indices_classe = df[df==classe ].index 
            indices_classe = indices_classe.values 
            
            not_in_classe  = df[df!=classe ].index 
            not_in_classe  = not_in_classe.values  
            
            random.shuffle(indices_classe)
            random.shuffle(not_in_classe )                          
            
            smallest_n     = min(len(indices_classe), len(not_in_classe))
            indices        = np.concatenate([indices_classe[:smallest_n], not_in_classe[:smallest_n]])
            
            if smallest_n > 5:
                datasets.append(indices)
    except Exception as e :
        print("pbm in get_n_indices_set : %s"%e)
    return datasets
"""
    SVM grid search
"""
def svm_grid_search(df, Y):
    import sys
    from sklearn                   import grid_search
    from sklearn.svm               import SVC
    import pickle
    parameters = {  "C"              : [1.0, 0.5, 0.1, 2]                , 
                    "kernel"         : ['rbf', 'poly', 'sigmoid']        ,
                    "degree"         : [2, 3, 4,5,6]                     , 
                    "gamma"          : [0.01, 0.1, 0.001, 0.5]           , 
                    "coef0"          : [0.0]                             , 
                    "shrinking"      : [True]                            , 
                    "probability"    : [True]                            , 
                    "tol"            : [0.001]                           , 
                    "cache_size"     : [10]                              , 
                    "class_weight"   : [None]                            , 
                    "verbose"        : [False]                           , 
                    "max_iter"       : [-1]                              , 
                    "random_state"   : [None]                            }
    
    print("-"*30, "\n svm_grid_search"); sys.stdout.flush()
    
    """
        Search Grid
    """
    grid    = grid_search.GridSearchCV(SVC(), parameters, verbose=0, scoring='f1_weighted')
    try :grid.fit(df, Y)
    except Exception as e : print("[svm_grid_search - 2] : %s"%e) ; print("x_train, y_train : ", x_train, y_train)

    print(" best_score_ = %.2f with =  %s "%(grid.best_score_, grid.best_estimator_ )) ; sys.stdout.flush()    
    return grid.best_estimator_
"""
    KNN grid search
"""
def knn_grid_search(df, Y):
    import sys
    from sklearn                   import grid_search
    from sklearn.neighbors         import KNeighborsClassifier
    
    import pickle

    parameters = {  "n_neighbors"    : [2, 3, 5, 8 , 10]                         , 
                    "weights"         : ['uniform', 'distance']                  ,
                    "algorithm"      : ['auto', 'ball_tree', 'kd_tree', 'brute'] , 
                    "leaf_size"      : [1,3 ]                                    }
                    
    grid_type = "knn_grid_search"
    print("-"*30, "\n %s"%grid_type); sys.stdout.flush()
    """
        Search Grid
    """
    grid    = grid_search.GridSearchCV(KNeighborsClassifier(), parameters, verbose=0, scoring='f1_weighted')
    try :grid.fit(df, Y)
    except Exception as e : print("[%s - 2] : %s"%(grid_type,e)) ; print("x_train, y_train : ", x_train, y_train)

    print(" best_score_ = %.2f with =  %s "%(grid.best_score_, grid.best_estimator_ )) ; sys.stdout.flush()    
    return grid.best_estimator_
"""
    Random Forest
"""
def RandomForest_grid_search(df, Y):
    import sys, pickle
    from sklearn.ensemble          import RandomForestClassifier
    from sklearn                   import grid_search
    from sklearn.metrics           import make_scorer
    from sklearn.preprocessing     import label_binarize
    from sklearn.multiclass        import OneVsRestClassifier
    #grid search :
    parameters_nas1 = {  "n_estimators"    : [ 1000]                 , 
                    "min_samples_leaf"     : [3]                     ,
                    "criterion"            : ["gini", "entropy"]     ,
                    "max_features"         : ["auto"]                ,
                    "max_depth"            : [None]                  , 
                    "n_jobs"               : [ -1]                   ,  
                    "class_weight"         : ["auto"]                ,
                    "warm_start"           : [False]                 }
    
    parameters = {  "n_estimators"    : [ 500, 1000,2000, ]          , 
                    "min_samples_leaf"     : [3,1, 7 ]               ,
                    "criterion"            : ["gini", "entropy"]     ,
                    "max_features"         : ["auto"]                ,
                    "max_depth"            : [None]                  , 
                    "n_jobs"               : [ -1]                   }#,  
                    #"class_weight"         : ["auto"]          }
                    #"warm_start"           : [False]           }
    grid_type = "RandomForestClassifier"
    
    print("-"*30, "\n %s"%grid_type); sys.stdout.flush()
    """
        Search 
    """
    #model_to_set = OneVsRestClassifier(RandomForestClassifier())
    #grid         = grid_search.GridSearchCV(model_to_set, parameters, verbose=1, scoring='r2')

    grid         = grid_search.GridSearchCV(RandomForestClassifier(), parameters, verbose=1, scoring='f1')
    
    try :grid.fit(df, Y)
    except Exception as e : print("[%s - 2] : %s"%(grid_type,e)) 
    
    print(" best_score_ %s with =  %s "%( grid.best_score_,  grid.best_estimator_ )) ; sys.stdout.flush()    
    return grid.best_estimator_
"""
    Affinity Propagation
"""
def Affinityscorer(estimator, X, y):
    return float(sum(estimator.predict(X)==y))/len(y)
def AffinityPropagation_grid_search(df, Y):
    import sys, pickle
    from sklearn.cross_validation   import cross_val_score, train_test_split
    from sklearn                    import grid_search
    from sklearn.cluster            import AffinityPropagation
    from sklearn.metrics            import make_scorer
    
    parameters = {  "damping"    : [0.5,0.7,0.8,0.9]                       , 
                    "convergence_iter"         : [5,10,15]  ,
                    "max_iter"      : [10,20,50,100,150,200]    }
                    
    grid_type = "AffinityPropagation"
    print("-"*30, "\n %s"%grid_type); sys.stdout.flush()

    """
        Search 
    """
    scorer  = make_scorer(Affinityscorer)
    grid    = grid_search.GridSearchCV(AffinityPropagation(), parameters, verbose=0, scoring=scorer)

    
    try :
        grid.fit(df, Y)
        print("fitted"); sys.stdout.flush()
    except Exception as e : print("[%s - 2] : %s"%(grid_type,e)) 
    
        
    print(" best_score_ %s with =  %s "%( grid.best_score_,  grid.best_estimator_ )) ; sys.stdout.flush()    
    return grid.best_estimator_
def draw_confusion_matrix(y_test, predictions, title):
    cm    = confusion_matrix(y_test, predictions)
    accur = accuracy_score  (y_test, predictions)
    
    plt.matshow  (cm)
    plt.ylabel   ('True Label')
    plt.xlabel   ('Predicted Label')
    plt.suptitle ('Confusion matrix (Accuracy of %.2f) for [%s]'%(accur,title))
    plt.colorbar ()
    plt.show     ()
def draw_roc_curve(fitted_c, x_test, y_test, title):
    from sklearn.metrics import roc_curve, auc
    c                                        = fitted_c
    probas                                   = c.predict_proba(x_test)
    false_positive_rate, recall_, thresholds = roc_curve(y_test, probas[:,1])
    roc_auc                                  = auc(false_positive_rate, recall_)
    
    plt.title  ('ROC %.2f %s'%(roc_auc, title))
    plt.legend (loc="lower right")
    plt.plot   ([0,1],[0,1], "r--")
    plt.plot   (false_positive_rate, recall_, 'b', label='AUC = %.2f'%roc_auc)
    plt.xlim   ([0.0,1.1])
    plt.ylim   ([0.0,1.1])
    plt.ylabel ('Recall')
    plt.xlabel ('Fall-out')
    plt.show()
def multi_class_roc(c, X, y, classes, title):
    # imports 
    import numpy                  as     np
    import matplotlib.pyplot      as     plt
    
    from sklearn                  import svm, datasets
    from sklearn.metrics          import roc_curve, auc
    from sklearn.cross_validation import train_test_split
    from sklearn.preprocessing    import label_binarize
    from sklearn.multiclass       import OneVsRestClassifier
    # Binarize the output
    y         = label_binarize(y, classes=classes)
    n_classes = y.shape[1]
    X         = np.c_[X]

    # shuffle and split training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2,random_state=0)

    # Learn to predict each class against the other
    classifier = OneVsRestClassifier(c)
    y_score    = classifier.fit(X_train, y_train).predict(X_test)

    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"]              = auc(fpr["micro"], tpr["micro"])

    # Plot ROC curve
    plt.figure()
    plt.plot(fpr["micro"], 
             tpr["micro"],
             label='micro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc["micro"]))
    for i in range(n_classes):
        plt.plot(fpr[i], tpr[i], label='ROC curve of class {0} (area = {1:0.2f})'
                                       ''.format(i, roc_auc[i]))

    plt.plot   ( [ 0   , 1   ], [0, 1], 'k--')
    plt.xlim   ( [ 0.0 , 1.0 ] )
    plt.ylim   ( [ 0.0 , 1.05] )
    plt.xlabel ( 'False Positive Rate')
    plt.ylabel ( 'True Positive Rate')
    plt.title  ( title)
    plt.legend ( loc="lower right")
    plt.show   ( )
def binary_multi_roc_curve(c, X, y, t ):
    import numpy                    as      np
    from   scipy                    import interp
    import matplotlib.pyplot        as     plt
    from   sklearn                  import svm, datasets
    from   sklearn.metrics          import roc_curve, auc
    from   sklearn.cross_validation import StratifiedKFold
    
    
    X.index = list(range(0, X.shape[0]))
    y.index = list(range(0, y.shape[0]))
    n_samples, n_features = X.shape
    X          = np.c_[X]
    cv         = StratifiedKFold(y, n_folds=6)
    classifier = c
    mean_tpr   = 0.0
    mean_fpr   = np.linspace(0, 1, 100)
    all_tpr    = []
    
    plt.figure(figsize=(10,5))
    plt.xlim([-0.05, 1.05])                       ; plt.xlabel('False Positive Rate')
    plt.ylim([-0.05, 1.05])                       ; plt.ylabel('True Positive Rate')
    plt.title('binary_multi_roc_curve for predicting [%s]'%t) ; plt.legend(loc="best")
    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
    
    for i, (train, test) in enumerate(cv):
        #cross prediction
        probas_              = classifier.fit(X[train], y[train]).predict_proba(X[test])
        fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
        #means
        mean_tpr            += interp(mean_fpr, fpr, tpr)
        mean_tpr[0]          = 0.0
        #ROC 
        roc_auc              = auc(fpr, tpr)
        #plot ROC
        plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))
    
    #mean accuracy
    mean_tpr /= len(cv); mean_tpr[-1] = 1.0; mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, 'r--',label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)
    plt.show()
    
        