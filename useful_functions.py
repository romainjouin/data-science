#-*- coding: utf-8 -*-
def transform_csv_into_excel(path_csv):
    """
    
    """
    import pandas as pd
    output_path = path_csv[:-4]+".xls"
    writer = pd.ExcelWriter(output_path)
    df = pd.read_csv(path_csv)
    df.to_excel(writer)
    writer.save()

def reject_outliers(data, m = 2.):
    import numpy as np
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<m]

def get_outliers(data, m = 2.):
    import numpy as np
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s>m]

def describe_table(table, sqlContext):
    """
    Print to screen the fields name of a table (one by line)
    
    parameter:
        table : string
    
    return : none (print on screen)
        
    """
    print "describing table : %s"%table
    for field_ in sqlContext.table(table).schema.fields:
        print field_.name
        
import os
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
    while i<stop:
        i+= step
        r.extend([i])
    return r

def clean_file_name(path):
    """
    !! untested !!
    
    Remove ["_","(", ")"] and lowercase filenames.
    
    Parameters:
        paths : one path
    Return : 
        string : changed filename
    """
    
    clean_filename = path.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("_-_", "_")
    return clean_filename
        

def clean_file_names(paths):
    """
    !! untested !!
    
    Remove ["_","(", ")"] and lowercase filenames.
    
    Parameters:
        paths : array of paths
    Return : 
        Nothing : change filename on the file system (+ print on stdout)
    """
    import ntpath
    for path in paths:
        dir_           = ntpath.dirname(path)
        filename       = ntpath.basename(path)
        clean_filename = filename.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("_-_", "_")
        clean_path     = dir_+"/"+clean_filename
        print "trying to os.rename(%s,%s) "%(path,clean_path); os.stdout.flush()
        os.rename(path,clean_path)

def split_excels(path_to_excel_file, output_dir="./", n_worksheet=3):
    """
    !! Untested !!
    Create one file by worksheet of an excel file.
    
    Parameters :
        path_to_excel_file : string 
        output_dir : string, path to ouputdir (must end by a slash)
        n_worksheet : int, number of worksheet to look for

    Return : nothing (create files on hard drive + print infos on stdout)
    
    """
    import pandas as pd
    import xlrd
    import sys
    
    path           = path_to_excel_file
    short_filename = path.replace("/", "").replace(".xlsx", "").replace(".", ""); print "Going to read : %s"%path                 ; sys.stdout.flush()
    start_reading  = time.time()                             					; print "Reading"                                 ; sys.stdout.flush()
    data           = pd.read_excel(path, sheetname=range(n_worksheet))  		; print "Read in %s"%(time.time() - start_reading); sys.stdout.flush()
    for worksheet in data.keys():
        try:
            print "Wk %s"%worksheet; sys.stdout.flush()
            output_path   = "%s%s_worksheet_%s.csv"%(output_dir, short_filename, worksheet) ; print "Saving into %s"%(output_path) ; sys.stdout.flush() ;  start_saving = time.time() 
            data[worksheet].to_csv(output_path, encoding='UTF-8')                           ; print "Saved in %s"%(time.time()-start_saving)
        except Exception as e:
            print "Erreur in worksheet %s"%worksheet ; sys.stdout.flush()
            print e[:100] ; sys.stdout.flush()
            

def change_commas_to_dots_in_dir(directory_path):
    """
        Retrieve all the csv under a root dir, and apply the change_commas_to_dots function to each.

        Args:
            directory_path (str): path to the root directory

        Returns: 
            nothing
    """
    paths = get_all_csvs_underdir(directory_path)	
    map(lambda path:  change_commas_to_dots(path), paths)


def change_commas_to_dots(file_path):
	"""
		Apply the shell sed command to change commas to dot on a filepath.

		Returns: nothing. 
	"""
	from subprocess import call
	call(["sed", "-i", "s/,/\./g", file_path])





def dico_from_two_col_tsv(fsv_path, separator = "\t"):
	"""
		Open a two-col tsv file and return a dictionnary made out of it (first column is a key, second a value).

		Args:
			fsv_path  (str): path to a 'formated'-separated-value file.
			separator (str): separator used to format the separated-value file.
		
		Algo:
			open the file, and populate a dict line by line.

		Returns:
			dict: keys are value read from the 1st col, associated value are striped value from the 2nd col.
	"""
	dico_ = {}
	with open(fsv_path) as f:
		for line in f :
			k,v = line.split(separator)
			k,v = k.strip(), v.strip()
			dico_[k] = v

	return dico_

def find_type(string):
	"""
		Test the data type contained inside a string (int, float, chararray). 

		Returns (str): string's type
	"""
	from datetime import datetime
	tests = [ 	("int"			, int	), 
				("float"		, float	), 
				("chararray" 	, lambda value : datetime.strptime(value, "%d/%m/%y")),
				("chararray" 	, lambda value : datetime.strptime(value, "%Y/%m/%d")),
				("chararray" 	, lambda value : datetime.strptime(value, "%d/%m/%Y")),
				("chararray" 	, lambda value : datetime.strptime(value, "%Y-%m-%d")),
				("chararray" 	, lambda value : datetime.strptime(value, "%d-%m-%d")),
				("chararray" 	, lambda value : datetime.strptime(value, "%y/%m/%d"))]
	"""
	("date-dmy" 	, lambda value : datetime.strptime(value, "%d/%m/%y")),
	("date-Ymd" 	, lambda value : datetime.strptime(value, "%Y/%m/%d")),
	("date-dmY" 	, lambda value : datetime.strptime(value, "%d/%m/%Y")),
	("date-Y-m-d" 	, lambda value : datetime.strptime(value, "%Y-%m-%d")),
	("date-d-m-d" 	, lambda value : datetime.strptime(value, "%d-%m-%d")),
	("date-ymd" 	, lambda value : datetime.strptime(value, "%y/%m/%d"))
	"""
	for typ, test in tests:
		try 	: 
			test(string)
			return typ 
		except 	: pass
	
	try:
		s = string.replace(",", ".")
		float(s)
		return "float"
	except : pass

	return "chararray"


def detect_column_type(path_to_csv_file):
	"""
	
	"""
	# -- imports --
	import 	csv
	from 	collections import defaultdict
	# -- parameters --
	nb_line_to_test 					= 10000
	nb_of_wished_tested_value_by_col 	= 100
	# -- algo --
	with open(path_to_csv_file) as csv_file:
		csv_reader 		= csv.reader(csv_file, delimiter=find_delimiter(path_to_csv_file))
		current_line 	= 0
		type_by_header 	= {}

		for line in csv_reader:
			current_line +=1
			if current_line == 1:
				#catch headers
				headers 	= [field.strip() for field in line]
				nb_headers 	= range(len(headers))
				nb_test_by_col 	= [0] * len(headers)
				for header in headers : type_by_header[header] = defaultdict(int)
			else:
				#deal with lines
				values = [field.strip() for field in line]
				for index in nb_headers:
					value 		= values[index]
					if value != "":
						colonne 	= headers[index]
						type_cell 	= find_type(value)
						type_by_header[colonne][type_cell] += 1	
						nb_test_by_col[index] +=1
				
				
				if all(nb_test_by_col[i] > nb_of_wished_tested_value_by_col for i in nb_headers) or current_line > nb_line_to_test :
					break
				
				if current_line > nb_line_to_test :
					break
	# clean results:
	for header, types in type_by_header.items():
		if len(types) ==1:
			type_by_header[header] = types.keys()[0]
		else:
			if 	 "text" 	in types.keys()	: type_by_header[header] =  "text"
			elif "float" 	in types.keys()	: type_by_header[header] = "float"
			elif "int" 		in types.keys()	: type_by_header[header] = "int"
			else 							: type_by_header[header] =  "unknown ( %s)"% types.keys()


	return type_by_header






def get_all_csvs_underdir(directory_path):
	"""
		Call [get_all_specific_paths_under_dir] leeting wanted_ends to its default value.

		Return : 
			(Array of paths)
	"""
	return get_all_specific_paths_under_dir(directory_path)

def get_all_specific_paths_under_dir(directory_path, wanted_end = ".csv"):
	"""
		Recursevely walk a directory and create an array of path leading to a csv file.

		Parameter:
			directory:string
				Path to the root directory to walk through.
			wanted_ends:string
				Ending we are looking for into the filename. (ie: '.csv' for csv files)
				Default = ".csv" (ie returning list of csv files)int
		Return: array
			Array of paths (csv as defaults).
	"""
	files_paths = []
	for dirname, dirnames, filenames in os.walk(directory_path) :
		for filename in filenames:
			if filename.endswith(wanted_end): 
				files_paths.append(os.path.join(dirname, filename))

	return files_paths


def find_delimiter(path_to_csv_file):
	"""
		Test delimiters ([,], [;], [\t]) and send back the one more likely to be.

		Usage : 
			Useful to find the delimiter of a csv file.
	"""
	coma      = ","
	semicolon = ";"
	tab       = "\t" 
	with open(path_to_csv_file) as csv_file:
		for headers in csv_file:
			test_comma 		= len(headers.split(coma 	  ))
			test_semicolon 	= len(headers.split(semicolon ))
			test_tab 	    = len(headers.split(tab 	  ))
			max_            = max([test_comma, test_semicolon, test_tab])
			if max_ == test_comma     : return coma
			if max_ == test_semicolon : return semicolon
			if max_ == test_tab       : return tab
			
			return None

def get_headers(path_to_csv_file):
	"""
		Open a csv file and create a striped array of the first line splitted by auto-detected separator.
		
		return: array

	"""
	import csv
	with open(path_to_csv_file) as csv_file:
		csv_reader 	= csv.reader(csv_file, delimiter=find_delimiter(path_to_csv_file))
		for line in csv_reader:
			return [field.strip() for field in line]



def create_random_sample(input_dir, output_dir, nb_lines, max_line):
	"""
		Find all the csv under the input_dir and create an extract for each one in the output dir.		

		!! now the output dir is not taken into account (files are created in the local dir) !!

		Parameters:
			nb_lines : int 
				Number of line we want the extract to have (the extract may be way smaller for a file which doesn't have that much lines)

			max_line: int
				Maximum line we want to read in the files (this could be used to limit the execution time)

		Algo:
			1) create a random array of [ len = nb_lines ] line in the range [1, max_line].
			2) open the file, read it line by line, and write out the lines found in the random array of lines.
			3) break on either nb_lines are written or max_lines are read.
		
		Return : nothing

	"""
	import numpy as np
	onlycsv = get_all_csvs_underdir(input_dir)
	len_input_dir = len(input_dir)
	# 1) USER INFO :
	print "-"*50
	print " "*20, "Creating random extract"
	print "-"*50
	print "input dir = %s" 	% (input_dir)
	print "%s files : [%s]" % (len(onlycsv), ",".join(onlycsv))
	print "output dir = %s" % (output_dir)
	print "Selecting %s lines within the %s first." %(nb_lines, max_line)
	# 2) READING FILES
	for csv_path in onlycsv:
		random_lines 		= np.random.randint(1, max_line, size=nb_lines)  										# SELECTING RANDOM LINES
		current_line 		= 0
		nb_written_lines 	= 0
		to_print  			= ""
		print "Dealing with : %s "%(csv_path)
		with open( csv_path, "r") as inputs:
			output_file 			= 	csv_path[:-4]+"_random_%s_lines.csv"%(nb_lines)
			with open(output_file, "w") as output :
				for line in inputs:
					current_line   +=1
					
					if current_line == 1:  						# WE SAVE THE HEADERS
						to_print = line
						continue

					if current_line in random_lines:  			# WE WRITE OUT THE RANDOM LINES
						to_print         += line
						nb_written_lines +=1

					if current_line % 100000 ==0:
						output.write(to_print)
						to_print = ""
						print "Line %s : wrote %s lines out of %s wanted. (%.2f pct) "%(current_line, nb_written_lines, nb_lines, nb_written_lines/nb_lines )
					if nb_written_lines >= nb_lines:
						break
					if current_line >= max_line:
						break
				output.write(to_print)




def extract_n_lines(input_dir, nb_lines):
	"""
		Find all the csv under the input_dir and create an extract for each one.		
	"""
	
	for csv_path in  get_all_csvs_underdir(input_dir):
		current_line 		= 0
		print "Dealing with : %s "%(csv_path)

		with open( csv_path, "r") as inputs:
			output_file = csv_path[:-4]+"_extract_%s.csv"%(nb_lines)
			with open(output_file, "w") as output :
				for line in inputs:
					output.write(line)					
					current_line   +=1
					if current_line == nb_lines:
						break

def count_separator(file_path, delimiter=','):
	"""
		Read a file, line by line, for each line, fetch the nb of delimiter. 
		If the nb of delimiter change, print a message and the line number
	"""
	import sys
	num_line          = 0
	last_nb_delimiter = 0

	with open("%s_strange_lines.csv"%(file_path), "w") as output:
		output.write("count_separator(%s, delimiter=%s)\n"%(file_path, delimiter))
		with open( file_path, "r") as inputs:
			for line in inputs:
				num_line     += 1
				nb_delimiter  = line.count(delimiter)
				if nb_delimiter != last_nb_delimiter:
					print "%s/%s,"%(num_line, nb_delimiter),
					last_nb_delimiter = nb_delimiter
					output.write(line)
				if num_line % 500000 ==0:
					print num_line," ", ; sys.stdout.flush() 

def strip_csvs(directory_path):

	"""
		Take a directory, and strip the values contained in the csvs.

		PARAMETERS:
			directory_path : directory where to search for csvs (must end with an [/])

		RETURN : 
			create a '_small_' file for each file in the list (on the same directory list)
	"""

	from os 			import listdir
	from os.path 		import isfile, join
	"""
		PARAMETERS
	"""
	if not directory_path.endswith("/") :
		directory_path = "%s/"%(directory_path)
	path 			= directory_path 
	
	onlycsv 		=  [f 		for f in listdir(path) if isfile(join(path, f)) if f.endswith(".csv")]
	#onlycsv = [	"H_OPRT_ACTE.csv"]

	separator 		= ";"
	unwanted_values = []
	default_value 	= ''


	"""
		ALGO
	"""
	for csv in onlycsv:
		big 	= path+csv
		small 	= big[:-4]+"_small_.csv"
		with open(big,"r") as too_big:
			with open(small, "w") as smaller:
				print "Reducing :\n %s\n to:\n %s " %(too_big, smaller)
				for line in too_big:
					chunks = [x.strip() for x in line.split(separator)]
					#chunks = [ x if x not in unwanted_values else default_value for x in chunks ]
					smaller.write(separator.join(chunks))
					smaller.write("\n")
				print "--"

def find_common_key(path, onlycsv):
			import csv
			"""
				(2) populate a dictionnary with a table of fields by csv
					+
					populate 2 identical sets with the distincts fields values
			"""
			fields 					= set()
			commonfields 			= set()
			joignable_csv 			= []


			for file_name in onlycsv:
				with open(path+file_name) as input_file:
					csv_reader 		= csv.reader(input_file, delimiter=find_delimiter(path+file_name))
					if debug : print "%s delimiter = %s "% (file_name, find_delimiter(path+file_name))
					for line in csv_reader:
						headers[file_name] 	= [field.strip() for field in line]
						if debug : print "headers = %s" % (headers)
						for field in headers[file_name]:			
							fields.add(field)
							commonfields.add(field)
							nb_file_by_key[field]+=1
						break

			"""
				(3) reduce the [commonfields] set by discarding all fields wich are not in all files
			"""

			for file_name in headers:
				for field in fields:
					if field not in headers[file_name]:
						commonfields.discard(field)
			"""
				(4) populate an array of files all the having at least one field in the list of commonfields
			"""
			
			for file_name in headers:
				joignable = False
				for key in headers[file_name]: 
					if key in commonfields: joignable = True

				if joignable: joignable_csv.append(file_name)

			"""
				5) We select one commonkey
			"""
			print "="*50
			print "Looking for common key in : %s "%(onlycsv)
			commonkey = False

			try 	: commonkey = next(iter(commonfields))
			except 	: 
				print "no commonkey"
				best_key = [(k,v) for (k,v) in  nb_file_by_key.items() if v == max(nb_file_by_key.values())][0]
				print "best key : %s over %s files " % (best_key[0], best_key[1])
				commonkey = best_key[0]
				joignable_csv = []
				for file_name in headers:
					joignable = False
					for key in headers[file_name]: 
						if key == commonkey: joignable = True

					if joignable: joignable_csv.append(file_name)
			

			print "joignable_csv with this key : \n  |--> %s" % ("\n  |--> ".join(joignable_csv))
			print "commonfields = %s" % (commonfields)
			print "choosen key --> %s" % (commonkey)
			print "="*50
			return commonkey, joignable_csv

def help_change_col_name(df):
    """
    
    When we have a dataframe with strange column names, 
    it may be useful to create a directory with keys being simpler, and values pointing to these
    strange columns name.
    This print a pseudo code for creating such a dictionnary :
    the values are outputed to the screen, so that it can be copy-pasted into
    a script, and new key values can be implemented.
    
    Return:
        Nothing (output on stdout).
    
    
    """
    print "cols={"
    for c in df.columns:
        x = "''"
        print x.ljust(25),":'%s',"%c
    print '}'

def split_excels(path_to_excel_file, output_dir="./", n_worksheet=3):
    """
    Create one file by worksheet of an excel file.
    
    Parameters :
        path_to_excel_file : string 
        output_dir : string, path to ouputdir (must end by a slash)
        n_worksheet : int, number of worksheet to look for

    Return : nothing (create files on hard drive + print infos on stdout)
    
    """
    import pandas as pd
    import xlrd
    import sys
    import time
    import decouverte
    path           = path_to_excel_file
    short_filename = decouverte.get_file_name(path) + ".csv"; print "Going to read : %s"%path                 ; sys.stdout.flush()
    start_reading  = time.time()                              ; print "Reading"                                 ; sys.stdout.flush()
    data           = pd.read_excel(path, sheetname=range(n_worksheet)) ; print "Read in %s"%(time.time() - start_reading); sys.stdout.flush()
    for worksheet in data.keys():
        try:
            print "Wk %s"%worksheet
            output_path   = "%s%s_worksheet_%s.csv"%(output_dir, short_filename, worksheet) ; start_saving = time.time() ; print "Saving into %s"%(output_path) ; sys.stdout.flush()
            data[worksheet].to_csv(output_path, encoding='UTF-8') ;  print "Saved in %s"%(time.time()-start_saving)
        except Exception as e:
            print "Erreur in worksheet %s"%worksheet ; sys.stdout.flush()
            print e[:100] ; sys.stdout.flush()

def fetch_csv_headers(dirpath="."):
	"""
	Fetch all the csvs in the directory 'dirpath', 
	and create a string with the name of the file, folowwed by the list of headers.
	
	Return:
		array of lines.
	"""
	lines = []
	csv = get_all_csvs_underdir(dirpath)
	for c in csv:
		headers = get_headers(c)
		for h in headers:
			l = ntpath.basename(c)+","+h.replace("\n", " ")
			lines.append(l)
	return lines


def dico_from_directory(dir_path):
    """
    Display on screen a python code listing the csvs in a directory on a dictionnary structure : keys = csv name, v= csv path.
    
    Params:
        dir_path : string
            path to the directory from which we want to display the csvs.
    
    Return: nothing (display on stdout)
    
    Usage : 
        It can be useful to map a list of csv name to variables. 
        A dict is a good structure for that.
        this script help coding that by displaying on stdout a dict-like frame to copy-paste in your code.
    
    """
    import ntpath
    csv_paths = get_all_csvs_underdir(dir_path)
    print "files = {"
    for path in csv_paths:
        print "'':'%s',"%(ntpath.basename(path))
    print "}"

def compare_two_sets(big_liste, small_liste, to_print =""):
    """
    Print on stdout some info comparing to lists of elements (interesction / difference / subset...).
    
    Parameters : 
        big_liste : left join columns
            pandas Series
        small_list : right join columns
            pandas Series
        to_print : message to print for the user
            string
    Return :
        nothing (print on stdout)

    Usage:
        It is useful to study to columns that are used as joining key to detect some
        unexpected unfitting. This function display on screen some set difference/intersection 
        calculus as first approach to join operations.
    
    """
    
    big, small                   = set(big_liste), set(small_liste)
    len_big , len_small          = len(big), len(small)
    intersection                 = big.intersection(small)
    difference                   = big.difference(small)
    big_is_subset_of_small       = big.issubset(small)
    small_is_subset_of_big       = small.issubset(big)
    elem_in_big_not_in_small     = big.difference(small)
    elem_in_small_not_in_big     = small.difference(big)
    nb_elem_in_big_not_in_small  = len(elem_in_big_not_in_small)
    nb_elem_in_small_not_in_big  = len(elem_in_small_not_in_big)
    print to_print
    print "len_big                       : ", len_big 
    print "len_small                     : ", len_small
    print "nb of intersection            : ", len(intersection)
    print "nb_elem_in_big_not_in_small   : ", nb_elem_in_big_not_in_small
    print "nb_elem_in_small_not_in_big   : ", nb_elem_in_small_not_in_big
    print "big_is_subset_of_small        : ", big_is_subset_of_small
    print "small_is_subset_of_big        :  ", small_is_subset_of_big
    print "ex 5 elem_in_big_not_in_small : ", list(elem_in_big_not_in_small)[:5]
    print "ex 5 elem_in_small_not_in_big : ", list(elem_in_small_not_in_big)[:5]

def white_rotate():
    """
    prend la figure matplotlib en cours de création et met son fond en blanc, et affiche la figure.
    Uasage :
        à appeler après un "plot" sur une dataframe
    """
    import matplotlib.pyplot as plt
    bgcolor             = 'white'
    rotation            = 50
    loc                 = 'best'
    bbox_to_anchor      = (1.05, 1)
    loc                 = 2
    borderaxespad       = 0.
    rotation            = 45
    figsize             = (3, 22)
    date_format         = '%a'
    ax                  = plt.gca()
    short_labels        = [ item.get_text()[:10]  for item in ax.get_xticklabels()   ]
    xtl                 = [ n if i%10==0 else " " for i,n  in enumerate(short_labels)]
    

    handles, labels     = ax.get_legend_handles_labels()
    #ax.set_xticklabels(xtl)
    ax.legend(handles                          , 
              labels                           ,  
              bbox_to_anchor = bbox_to_anchor  , 
              loc            = loc             , 
              borderaxespad  = borderaxespad   )
    ax.set_axis_bgcolor(bgcolor)
    #ax.xaxis_date()
    
    #ax.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter(date_format))
    plt.xticks(rotation = rotation)        
    #plt.legend(loc      = loc     )
    plt.show()
    print 

