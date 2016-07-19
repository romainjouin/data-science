#coding: utf-8
def read_randstad_csv(path, nrows= None):
	"""
	lit des csvs randstad et retourne des csvs
	"""
	import useful_functions as useful
	import pandas as pd
	import datetime
	
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
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates)#, date_parser=date_parser)

	if path.endswith("contrats_merged.csv"):
		parse_dates = [6, 7]
		date_parser = lambda x: datetime.datetime.strptime(x, "%d%b%Y:%H:%M:%S")
		delimiter   = useful.find_delimiter(path)
		df		    = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)

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
		df		  = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)

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
		df		    = pd.read_csv(path, nrows=nrows, delimiter=delimiter, parse_dates=parse_dates, date_parser=date_parser)
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

	if path.endswith("Zone_emploi 2010_new(PLM).csv"):
		delimiter   = useful.find_delimiter(path)
		df 			= pd.read_csv(path, index_col=0, dtype={"cd_cmn":str, "cd_ze":str,"Lib_ze":str}, delimiter=delimiter)
		df["cd_ze"] = df["cd_ze"].map(lambda x: None if str(x)=='nan' else x[:-2])

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


	if "Unnamed: 0" in df.columns:
		return df.drop("Unnamed: 0", axis = 1)
	else:
		return df
	