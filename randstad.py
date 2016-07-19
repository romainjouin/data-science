#coding: utf-8
def read_randstad_csv(path, debug=False, nrows= None):
	"""
	lit des csvs randstad et retourne des csvs
	"""
	import time
	deb = time.time()
	import useful_functions as useful
	import pandas as pd
	import datetime
	import extra_pandas
	
	
	csvs_dir = "/Users/romain/Informatique/randstad/randstad_local/zz_data/zz_tous_en_csv/"
	if csvs_dir not in path:
		path = csvs_dir + path
	df = None
	if path.endswith("Apache - marché captable sur ZdC 2015.xlsx_marché captable.csv"):
		
		col_date	= "DT_test"
		parse_dates = {col_date : [2]}
		date_parser = lambda x: datetime.datetime.strptime(x, "%Y")
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)

	if path.endswith("BAPI-activite_unites.csv"):
		
		col_date	= "Annee_mois"
		parse_dates = {col_date : [1,2]}
		date_parser = lambda x,y: None if str(x) == 'nan' or str(y)=='nan' else datetime.datetime.strptime("%s%s"%(x,y), "%Y%m")
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)

	if path.endswith("BtoC - infos TT.csv"):
		
		col_date	= "DT_test"
		parse_dates = {col_date : [5, 9, 10]}
		date_parser = None
		delimiter   = useful.find_delimiter(path)
		df		    = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates)#, date_parser=date_parser)

	if path.endswith("contrats_merged.csv"):
		from dateutil.parser import parse
		parse_dates  = [6, 7]
		date_parser  = lambda x: datetime.datetime.strptime(x, "%d%b%Y:%H:%M:%S")
		delimiter    = useful.find_delimiter(path)
		df		     = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)
		default_date = parse("2020-01-01")
		date_9999    = df.DT_FIN_REELLE.map(lambda x: x.year == 9999)
		df.loc[date_9999, "DT_FIN_REELLE"] = default_date

	if path.endswith("DAFO ANALYSE - histo clients.xlsx_2013_merged_4_files.csv"):
		
		
		col_date	= "Annee_mois"
		parse_dates = {col_date : [3, 4]}
		date_parser = lambda x,y: datetime.datetime.strptime("%s%s"%(x,y), "%Y%m")
		delimiter   = useful.find_delimiter(path)
		df		    = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)

	if path.endswith("DAFO ANALYSE - histo TT 2013 - copie_merged_4_files.csv"):
		
		col_date	= "DT_test"
		parse_dates = {col_date : [2, 3]}
		date_parser = lambda x,y: datetime.datetime.strptime("%s%s"%(x,y), "%Y%m")
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)

	if path.endswith("histo - Comptes CC v2.xlsx_2016_merged_2_files.csv"):
		
		col_date	= "DT_test"
		parse_dates = {col_date : [1]}
		date_parser = lambda x: datetime.datetime.strptime("%s"%(x), "%Y-%m-%d")
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)



	if path.endswith("histo maturitÇ.xlsx_Feuil1.csv"):
		
		col_date	= "DT_maturite"
		parse_dates = {col_date : [2, 3]}
		date_parser = lambda x,y: datetime.datetime.strptime("%s%s"%(x,y), "%Y%m")
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)


	if path.endswith("histo_actions.csv"):
		parse_dates = [0, 17]
		def t(x): 
		    if x=='nan':return None 
		    else:
		        try    : return datetime.datetime.strptime(x, "%d/%m/%y") 
		        except : return datetime.datetime.strptime(x,       "%Y%m")
		
		#parse_dates = {"u'DT_action": [0],"Date_de_debut_action": [17]}
		
		date_parser = t
		delimiter   = useful.find_delimiter(path)
		df		    = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)
		

	if path.endswith("historique baux.xlsx_Feuil1.csv"):
		col_date	= "Annee_mois"
		parse_dates = {col_date : [1,2]}
		date_parser = lambda x,y: datetime.datetime.strptime("%s%s"%(x,y), "%Y%m")
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)

	if path.endswith("P4S 2013.xlsx_SQLT0090_merged_4_files.csv"):
		col_date	= "DT_test"
		parse_dates = {col_date : [3]}
		date_parser = lambda x: datetime.datetime.strptime("%s"%(x), "%d.%m.%Y")
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)


	if path.endswith("portefeuille comptes.csv"):
		col_date	= "DT_test"
		parse_dates = {col_date : [14]}
		date_parser = lambda x: datetime.datetime.strptime("%s"%(x), "%Y-%m-%d")
		delimiter   = useful.find_delimiter(path)
		#df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter)
		
	if path.endswith("ZE - historique marchÇ intÇrim - copie.csv"):
		col_date	= "annee_mois"
		parse_dates = {col_date : [2,3]}
		date_parser = lambda x,y: datetime.datetime.strptime("%s%s"%(x,y), "%Y%m")
		delimiter   = useful.find_delimiter(path)
		dtype = {"cd_ze" : str}
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser, dtype =dtype )

	if path.endswith("GEO - inscriptions candidats.csv"):
		col_date	= "DT_test"
		parse_dates = {col_date : [3]}
		date_parser = lambda x: None if x=='nan' else datetime.datetime.strptime("%s"%x, "%d%b%Y:%H:%M:%S")
		
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)
		#df		  = pd.read_csv(path)
		
	if path.endswith("histo_commandes_recrut.csv"):
		
		parse_dates = [9,10,11,12]
		date_parser = lambda x: None if x=='nan' else datetime.datetime.strptime("%s"%x, "%d%b%Y:%H:%M:%S")
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)
		col_date	= df.columns[9]
	
	if path.endswith("LIMON - BCI.csv"):
		col_date	= "DT_test"
		parse_dates = {col_date : [1]}
		date_parser = lambda x: None if x=='nan' else datetime.datetime.strptime("%s"%(x), "%Y%m")
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)
		
	
	
	if path.endswith("histo_fe.csv"):
		parse_dates = [1]
		date_parser = lambda x: None if x=='nan' else datetime.datetime.strptime("%s"%x, "%Y-%m-%d")
		delimiter   = useful.find_delimiter(path)
		dtype       = {"Code_INSEE_Ville"    : str   , 
			            "Code_Postal"        : str   ,
		                "Code_Unite_Service" : str   }
		df		    = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser, dtype=dtype)
		df["Date_de_Creation"] = map(lambda x: datetime.datetime.strptime("%s"%x, "%d/%m/%Y"), df["Date_de_Creation"])
		df.index =  df["Date_de_Creation"]
	
	if path.endswith("Fichier concurrents.csv"):
		def t(x): 
		    if x=='nan':return None 
		    else:
		        try    : return datetime.datetime.strptime(x, "%d/%m/%Y") 
		        except : return datetime.datetime.strptime(x,       "%Y")
		        
		date_parser = t
		parse_dates = ["Date de création"]
		delimiter   = useful.find_delimiter(path)
		df		    = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)
	
	if path.endswith("perimetre.csv"):
		df		    = pd.read_csv(path)
		df["code_agence"] = df.x
		df 			= df.drop("x", axis=1)

	if path.endswith("histo_commandes_TT.csv"):
		parse_dates = [5, 6, 7]
		date_parser = lambda x:  None if str(x)=='nan' else datetime.datetime.strptime("%s"%x, "%d%b%Y:%H:%M:%S") 
		delimiter   = useful.find_delimiter(path)

		df		    = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)		

	if path.endswith("evenements_marketing.csv"):
		delimiter   = useful.find_delimiter(path)
		col_date    = "Annee_mois"
		parse_dates = {col_date: [0,1]}
		date_parser = lambda x, y: None if str(x) == 'nan' or str(y) == 'nan' else datetime.datetime.strptime("%s%s" % (x, y), "%Y%m")
		pd.read_csv(path, delimiter=delimiter)
		nrows = None
		df          = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)

	if path.endswith("Zone_emploi 2010_new(PLM).txt"):
		delimiter   = useful.find_delimiter(path)
		df 			= pd.read_csv(path, dtype={"cd_cmn":str, "cd_ze":str,"Lib_ze":str}, delimiter=delimiter)
		print "removing null rows on cd_ze ( %s rows)"%(sum(df.cd_ze.isnull()))
		df = df[~df.cd_ze.isnull()]
		

	if path.endswith("R100 classement.csv"):
		delimiter   = useful.find_delimiter(path)
		col_date    = "Annee_mois"
		parse_dates = {col_date: [0]}
		date_parser = lambda x: None if str(x) == 'nan' else datetime.datetime.strptime("%s" % (x), "%Y")
		df          = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)


	if path.endswith("Fichier_concurrents_details.csv"):
		delimiter   = useful.find_delimiter(path)
		col_date    = "Annee_mois"
		parse_dates = {"date_creation": [11 ],"annee_tranche_ca": [13], "annee_n" : [16] }
		def t(x): 
		    if x=='nan':return None 
		    else:
		        try    : return datetime.datetime.strptime(x, "%d/%m/%Y") 
		        except : return datetime.datetime.strptime(x,       "%Y")
		        
		date_parser = t
		df          = pd.read_csv(path, nrows     = nrows, 
		                                delimiter = delimiter, 
		                              parse_dates = parse_dates,
		                              date_parser = date_parser,
		                              dtype       = {"SIREN" : str, "SIRET":str, 'Si\x8fge':bool})
	if path.endswith("Fichier_concurrents_adresse.csv"):
		delimiter   = useful.find_delimiter(path)
		col_date    = "Annee_mois"
		parse_dates = {"date_creation": [8 ],"annee_tranche_ca": [10]}

		def t(x): 
		    if x=='nan':return None 
		    else:
		        try    : return datetime.datetime.strptime(x, "%d/%m/%Y") 
		        except : return datetime.datetime.strptime(x,       "%Y")
		        
		date_parser = t
		df          = pd.read_csv(path, nrows     = nrows, 
		                                delimiter = delimiter, 
		                              parse_dates = parse_dates,
		                              date_parser = date_parser,
		                              dtype       = {"id_fichier" : str, "SIRET":str, 'Si\x8fge':bool})

	if path.endswith("DAFO_correspondances_qualifications_et_metiers.csv"):
		delimiter   = useful.find_delimiter(path)
		df = pd.read_csv(path, delimiter=delimiter)

	if path.endswith("BAPI_activite_unites_v2.csv"):
		delimiter   = useful.find_delimiter(path)
		parse_dates = {"annee_mois": [1,2]}
		date_parser = lambda x, y: None if str(x) == 'nan' or str(y) == 'nan' else datetime.datetime.strptime("%s%s" % (x, y), "%Y%m")

		df          = pd.read_csv(	path 					 , 
		                            nrows     	= nrows		 , 
		                            delimiter 	= delimiter  , 
		                            parse_dates = parse_dates ,
		                            date_parser = date_parser ,
		                            dtype       = {'Si\x8fge':bool})
		float_col = df.columns[[2,3,4,5,6,7,8,9,10,11,]]
		for col in float_col:
		    try:
		        df[col] = df[col].map(lambda x: x if isinstance(x, int) else float(0 if str(x)=='nan' else "%s"%x.replace(",",".")))
		    except Exception as e:
		        print col, ":", e

	if path.endswith("commandes et annonces.txt"):	
		delimiter   = useful.find_delimiter(path)
		parse_dates = {"annee_mois": [3,4]}
		date_parser = lambda x, y: None if str(x) == 'nan' or str(y) == 'nan' else datetime.datetime.strptime("%s%s" % (x, y), "%Y%m")

		df          = pd.read_csv(path, nrows     = nrows, 
		                                delimiter = delimiter, 
		                              parse_dates = parse_dates,
		                              date_parser = date_parser,
		                              dtype       = {})
	if path.endswith("Liste clients avec logiciels specifiques.txt"):
		delimiter = useful.find_delimiter(path)
		df        = pd.read_csv(path, nrows     = nrows, delimiter=delimiter)

	if path.endswith("Liste clients parametres avec N de CDE obligatoire.txt"):
		delimiter = useful.find_delimiter(path)
		df        = pd.read_csv(path, nrows     = nrows, delimiter=delimiter)

	if path.endswith("motifs recours.txt"):
		delimiter = useful.find_delimiter(path)
		df        = pd.read_csv(path, nrows     = nrows, delimiter=delimiter)
	
	if path.endswith("zdc_unite_ua260216.txt"):
		delimiter = useful.find_delimiter(path)
		df        = pd.read_csv(path, nrows     = nrows, delimiter=delimiter)
		df.code_commune_zdc = df.code_commune_zdc.apply(lambda x : str(x) if len(str(x)) == 5 else "0"+str(x))


	if path.endswith("correspondance-code-insee-code-postal-dedoublonne.csv"):
		delimiter = useful.find_delimiter(path)
		df        = pd.read_csv(path, nrows     = nrows, delimiter=delimiter)
		df["Code Postal"]  =df["Code Postal"].apply(lambda x : str(x) if len(str(x)) == 5 else "0"+str(x))
		df = df.drop_duplicates()

	if path.endswith("ciblage_MKT_BtoB_contacts_comptes.csv"):
		delimiter = useful.find_delimiter(path)
		df        = pd.read_csv(path, nrows     = nrows, delimiter=delimiter)

	if path.endswith("UnitP.csv") or path.endswith("UnitT.csv"):
		"""
		Informations géographiques sur les unités du périmètre
		"""
		parse_dates = ["date_extract_fe","Date_de_Creation"]
		def t(x): 
		    if x=='nan':return None 
		    return datetime.datetime.strptime(x, "%Y-%m-%d") 
		date_parser = t
		df          = pd.read_csv(path,  
		                          parse_dates = parse_dates,
		                          date_parser = date_parser)
	if path.endswith("unite_cp_cd_insee.csv"):
		delimiter = useful.find_delimiter(path)
		df          = pd.read_csv(path, delimiter=delimiter)
	
	if path.endswith("insee_zone_emploi_cp.csv"):
		delimiter = useful.find_delimiter(path)
		df          = pd.read_csv(path, delimiter=delimiter)

	if path.endswith("locations.csv"):
		# latitude / longitude des agences
		delimiter = useful.find_delimiter(path)
		df          = pd.read_csv(path, delimiter=delimiter)


	if path.endswith("locations_avec_XY_lambert93.txt"):
		import random
		lambert   = pd.read_csv(path)
		df        = lambert
		mask_lon  = (      0 < df["X_lambert93"] ) & (df["X_lambert93"] < 1300000 )
		mask_lat  = (6000000 < df["Y_Lambert93"] ) & (df["Y_Lambert93"] < 7300000 )
		lambert   = lambert[mask_lon & mask_lat]
		lambert.X_lambert93 = lambert.X_lambert93.apply(lambda x : x+ random.randint(1000,2000 ))
		lambert.Y_Lambert93 = lambert.Y_Lambert93.apply(lambda x : x+ random.randint(1000,2000 ))
		df        = lambert

	if path.endswith("Nombre contrats et avenant par origine.csv"):
		pass
	if path.endswith("dafo_histo_contrats_avec_mb.csv"):
		col_date	= "Annee_mois"
		parse_dates = {col_date : [2,3]}
		date_parser = lambda x,y: datetime.datetime.strptime("%s%s"%(x,y), "%Y%m")
		delimiter   = useful.find_delimiter(path)
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)
		df['Marge Brute'] = df['Marge Brute'].apply(lambda x: x.replace(",", "."))


	if path.endswith('histo_permanents_agence_randstad_perf_unite.csv'):
	    delimiter   = useful.find_delimiter(path)
	    dtype       = {"MAT_RH"           : str   , 
	                   "MAT_RHPI"         : str   ,
	                   "C_SEXE"           : str   , 
	                   "FTE_PAYE"         : float ,
	                   "pourc_ana_defaut" : float ,
	                   "pourc_ana_1"      : float }
	    converters  = {"FTE_PAYE"         : extra_pandas.enforce_float_for,
	                   "pourc_ana_defaut" : extra_pandas.enforce_float_for,
	                   "pourc_ana_1"      : extra_pandas.enforce_float_for,
	                   "% analytique 2"   : extra_pandas.enforce_float_for,
	                   "% analytique 3"   : extra_pandas.enforce_float_for,
	                   "% analytique 4"   : extra_pandas.enforce_float_for,
	                   "% analytique 5"   : extra_pandas.enforce_float_for}
	    parse_dates = [0, 9, 10]
	    def time_converter(x): 
	        if x=='nan':return None 
	        else:
	            try    : return datetime.datetime.strptime(x, "%d/%m/%Y" )  
	            except : return datetime.datetime.strptime(x, "%Y%m"     )

	    df          = pd.read_csv(path                           , 
	                              nrows          = nrows         , 
	                              delimiter      = delimiter     , 
	                              parse_dates    = parse_dates   , 
	                              date_parser    = time_converter,
	                              dtype          = dtype         ,
	                              converters     = converters    )
	    df["year"] = df.MOIS_COMPTABLE.apply(lambda x: x.year)
	    df["QS"  ] = df.MOIS_COMPTABLE.apply(lambda x: x.quarter)
	    df["trim"] = df.MOIS_COMPTABLE.apply(lambda x: pd.Period("%sQ%s"%(x.year,x.quarter)).start_time)

	if path.endswith("salaires_variables.csv"):
	    dtype = {"MOIS_COMPTABLE":str}
	    df    = pd.read_csv(path, useful.find_delimiter(path), index_col=0, dtype=dtype)
	    df.MOIS_COMPTABLE = df.MOIS_COMPTABLE.apply(lambda x: datetime.datetime.strptime(x, "%Y%m"     ))
	    df["year"] = df.MOIS_COMPTABLE.apply(lambda x: x.year)
	    df["QS"  ] = df.MOIS_COMPTABLE.apply(lambda x: x.quarter)
	    df["trim"] = df.MOIS_COMPTABLE.apply(lambda x: pd.Period("%sQ%s"%(x.year,x.quarter)).start_time)


	if path.endswith("cibleH.txt"):
	    converters = {"trim" : lambda x: pd.Period(x.replace(" ", "")).start_time}
	    df      = pd.read_csv(path, index_col=0, converters=converters)

	duree = time.time() -deb
	if debug:
		print "_"*10
		import decouverte
		print decouverte.get_file_name(path)
		print df.shape
		print df.dtypes
	print "fichier loade en %s" %(duree)
	

	if "Unnamed: 0" in df.columns:
		return df.drop("Unnamed: 0", axis = 1)
	else:
		return df
	