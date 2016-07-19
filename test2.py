def loop_for():
    deb = time.time()
    gpd    = df.groupby([pd.TimeGrouper(freq="QS-JAN"), 'CD_PDP'])
    result = []
    for (quarter, unite), data in gpd:
        nb_MAT_RH   = data["MAT_RH"  ].nunique()
        nb_MAT_RHPI = data["MAT_RHPI"].nunique()
        result.append({"unite": unite, "quarter": quarter, "nb_MAT_RH" : nb_MAT_RH, "nb_MAT_RHPI" : nb_MAT_RHPI})
    duree = time.time()-deb
    print duree
