#-*- coding: utf-8 -*-
"""
	Fichiers
"""
"""
	Stats
"""
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
				nb_headers 	= list(range(len(headers)))
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
	for header, types in list(type_by_header.items()):
		if len(types) ==1:
			type_by_header[header] = list(types.keys())[0]
		else:
			if 	 "text" 	in list(types.keys())	: type_by_header[header] =  "text"
			elif "float" 	in list(types.keys())	: type_by_header[header] = "float"
			elif "int" 		in list(types.keys())	: type_by_header[header] = "int"
			else 							: type_by_header[header] =  "unknown ( %s)"% list(types.keys())


	return type_by_header
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
    print("cols={")
    for c in df.columns:
        x = "''"
        print(x.ljust(25),":'%s',"%c)
    print('}')
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
    print(to_print)
    print("len_big                       : ", len_big) 
    print("len_small                     : ", len_small)
    print("nb of intersection            : ", len(intersection))
    print("nb_elem_in_big_not_in_small   : ", nb_elem_in_big_not_in_small)
    print("nb_elem_in_small_not_in_big   : ", nb_elem_in_small_not_in_big)
    print("big_is_subset_of_small        : ", big_is_subset_of_small)
    print("small_is_subset_of_big        :  ", small_is_subset_of_big)
    print("ex 5 elem_in_big_not_in_small : ", list(elem_in_big_not_in_small)[:5])
    print("ex 5 elem_in_small_not_in_big : ", list(elem_in_small_not_in_big)[:5])
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
    print() 

