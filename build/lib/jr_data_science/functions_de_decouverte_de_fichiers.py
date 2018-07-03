# -*- coding: utf-8 -*-
"""
Functions to help manipulating files.
"""
__author__ = 'romain'

def is_dir(dirpath):
    """
    Check either a path is a directory.
    :param dirpath: path to check
    :return:Boolean
    """
    return path_is_dir(dirpath)
def is_file(path):
    """
    Check either the given path is a file
    :param path: path to check
    :return: Boolean
    """
    return path_is_file(path)
def clean_dir_filenames(dirpath):
    """
    Call clean_filenames on all the file under the given dirpath
    :param dirpath: path to a directory
    :return:nothing
    """
    assert is_dir(dirpath)
    for path in get_filepaths(dirpath):
        clean_file_name(path)
def clean_file_name(path):
    """
    Replacce whites and 'minus' from filename to "_".
    :param path: file path
    :return: nothing (changing the names on the filesystem)
    """
    assert is_file(path)
    if path_is_not_a_dir(path):
        import ntpath, os
        dir = ntpath.dirname(path)
        old_path = os.path.join(dir , ntpath.basename(path))
        new_path = os.path.join(dir , ntpath.basename(path).replace(" ", "_").replace("-", "_").lower())
        if new_path != old_path :
            import os
            print("moving %s \n to: %s"%(old_path, new_path))
            os.rename(path, new_path)
        print("%s \n equals \n%s\n" %(new_path, old_path))
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
        dir_ = ntpath.dirname(path)
        filename = ntpath.basename(path)
        clean_filename = filename.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("_-_", "_")
        clean_path = dir_ + "/" + clean_filename
        print("trying to os.rename(%s,%s) " % (path, clean_path));
        os.stdout.flush()
        os.rename(path, clean_path)
def path_is_file(path):
    """
    Return True is path is a file, Raise an exception otherwise.
    """
    import os
    #assert(os.path.exists(path)), "'Path' parameter is not a file (%s)"%(path)
    return os.path.exists(path)
def path_is_not_a_file(path):
    """
    Return True is path is not a file, Raise an exception otherwise.
    """
    import os
    assert(not os.path.exists(path)), "'Path' parameter is an existing file (%s)"%(path)
    return True
def path_is_dir(directory):
    """
    Return True is path is a directory, Raise an exception otherwise.
    """

    import os
    assert(os.path.isdir(directory)), "The 'directory' parameter is not a directory (%s)"%(directory)
    return True
def path_is_not_a_dir(directory):
    """
    Return True is path is not a directory, Raise an exception otherwise.
    """
    import os
    assert(not os.path.isdir(directory)), "The 'directory' parameter is a directory (%s)"%(directory)
    return True
def do_extract(path, n_ligne, output_dir="./", debug=True):
    """
    Create a new file and write on it the n first ligne of the given path.
    :param path: file from which to extract lines
    :param n_ligne: number of ligne to extract (is used on the new-file naming)
    :param output_dir: if we want to write on a specific dir
    :return: nothing (new file created)
    #TODO: change to a panda trunk reading ?
    """
    import os
    assert path_is_file(path)
    assert is_dir(output_dir)
    n_written = 0
    output_path = os.path.join(output_dir , get_file_name(path)+"_%s.csv"%n_ligne)
    assert path_is_not_a_file(output_path), "%s already exist."%(output_path)
    with open(path, "r") as input_file:
        with open(output_path, "w") as output_file:
            while n_ligne > 0:
                ligne = input_file.readline()
                output_file.write(ligne)
                n_written += 1
                n_ligne = n_ligne -1
            if debug :
                print("Wrote %s lines into %s."%(n_written, output_path))
                print("Target dir = %s"%(output_dir))
def concatenate_csv(list_csv_path, path_output_file):
    """
    Write several files into the path_output_file (no header logic done !)
    :param list_csv_path: list of full path
    :param path_output_file: where to write the concatenation
    :return: void
    """
    #sanity check
    assert path_is_not_a_file(path_output_file)
    for path in list_csv_path: assert path_is_file(path)
    if not len(list_csv_path): return -1

    #var declaration

    #algo
    try:
        with open(path_output_file, "w") as outputfile:
            first_input_file= list_csv_path.pop()
            for line in open(first_input_file):
                outputfile.write(line)

            for path in list_csv_path:
                with open(path) as input_file:
                    next(input_file)
                    for line in input_file:
                        outputfile.write(line)
    except Exception as e:
        print("pbm in concatenate_csv: %s"%(e))
def get_filepaths(directory, extension=None):
    """
    Generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    import os, ntpath
    assert(os.path.isdir(directory)), "The 'directory' parameter is not a directory (%s)"%(directory)

    file_paths = []  # List which will store all of the full filepaths.
    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)

            if not ntpath.basename(filepath).startswith("."):
                file_paths.append(filepath)  # Add it to the list.

    if extension:return [x for  x in file_paths if x.endswith(extension) ]

    return file_paths  # Self-explanatory.
def get_header(path, delimiter):
    """

    :param path: full path to csv
    :param delimiter: csv delimiter
    :return: array of string
    """
    import os
    import csv
    assert(os.path.exists(path)), "'Path' parameter is not a file (%s)"%(path)
    try:
        result = []
        with open(path, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=delimiter)
            for row in csvreader:
                result = [r for r in row]
                break
        return result
    except:
        print("pbm")
        return False
def get_headers(csv_path, sep=";"):
    """
    Call a sub function with distinct encoding parameter to try reading csv.
    :param csv_path: complete path to csv file
    :param sep: csv separator
    :return: array
    """
    assert is_file(csv_path)
    r = False
    try:
        r = get_headers_sub(csv_path, ";", 'utf-8')
    except:
        pass
        #print "not utf-8"
    if not r:
        try:
            r = get_headers_sub(csv_path, ";", 'latin-1')
        except:
            pass
            #print "not latin-1"
    return r
def get_headers_sub(csv_path, sep=";", encoding_='utf-8'):
    """
    Try opening a csv file with a given encoding to read the first line.
    :param csv_path: complete path
    :param sep: csv separator
    :param encoding_: encoding
    :return: array
    """
    assert is_file(csv_path)
    from pandas import read_csv
    csv_reader = read_csv(csv_path, sep, iterator=True, chunksize=10, encoding=encoding_ )
    try:
        for chunk in csv_reader:
            r = []
            for row in chunk:
                r.append(row)
            return r
            break

    except Exception as e:
        #print "pbm reading the csv : %s"%(e)
        return False
def get_all_csvs_underdir(directory_path):
    """
        Call [get_all_specific_paths_under_dir] leeting wanted_ends to its default value.

        Return :
            (Array of paths)
    """
    return get_all_specific_paths_under_dir(directory_path)
def get_all_specific_paths_under_dir(directory_path, wanted_end=".csv"):
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
    import os
    files_paths = []
    for dirname, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename.endswith(wanted_end):
                files_paths.append(os.path.join(dirname, filename))

    return files_paths
def get_file_name(path):
    """
    Return jsut the filename (no path, no extension).
    :param path: complete file path
    :return: filename without extension
    """
    assert is_file(path)
    import ntpath
    import os
    base = os.path.basename(path)
    return "".join(os.path.splitext(base)[0:2])
def get_containing_dir(path):
    """
    Return the path of the containing dir
    :param path: complete file path
    :return: str
    """
    return  get_file_name_infos(path)[0]
def get_file_name_infos(path):
    """
    :param path: complete file path
    :return: infos
    """
    assert is_file(path)
    import ntpath
    import os
    base                 = os.path.basename(path)
    (filename, filetype) = os.path.splitext(base)
    dirname              = os.path.dirname (path)
    return  (dirname, filename, filetype)
def get_txt_and_csv(dir_path, txt_sep=";", csv_sep=";"):
    txt= get_filepaths(dir_path, ".txt" )
    csv= get_filepaths(dir_path, ".csv" )
    return txt+csv
def remove_string_from_file(path, to_search, replace_by=""):
    return replace_string_from_file(path, to_search, replace_by="")
def replace_string_from_file(path, to_search, replace_by=""):
    """
    Replace a string (or a list of strings) by another one.
    :param path: file to be changed
    :param to_search: string or sring array to be changed
    :param replace_by: string to write instead of the string to be replaced
    :return: path to the new file
    """
    assert isinstance(to_search, list) or isinstance(to_search, str), "%ss should be a list or a string"%(to_search)

    print("Going to replace %s by [%s] from %s "%(to_search, replace_by, path))

    if isinstance(to_search, str):
        to_search = [to_search]
    output_path = path+"_small"
    with open(output_path , "w") as f2:
        with open(path, "r") as f:
            for l in f:
                to_write = l
                for to_be_replaced in to_search:
                    to_write = to_write.replace(to_be_replaced, replace_by)
                f2.write(to_write)

    return output_path
def explore(file, sep=";", top = 10):
    """

    """
    import pandas as pd
    print("Exploring %s"%(get_file_name(file)))
    to_explore = pd.read_csv(file, sep=";", error_bad_lines=False)
    nb_lignes  = to_explore.shape[0]
    cols       = to_explore.columns
    i          = -1
    for col in cols:
        i       += 1
        serie    = to_explore[col]
        null     = serie.isnull()
        not_null = len([x for x in null if not x])

        print("%s) %s"%(i,col))
        print(not_null, " values not null out of ", nb_lignes, "(", not_null/nb_lignes, "), top %s :"%(top))
        s        = serie.value_counts()
        d        = s/not_null
        d        = ["%.2f"%(x) for x in d]
        top_     = list(zip(s.index[:top], s.values[:top] , d))
        print(top_,  "\n")
    print("="*50)
def extract_column_from_csv(path, columns, output_dir, sep=';', chunksize=100000, debug=False):
    import pandas as pd
    import os
    assert is_file(path), "%s is not a file !"%(path)
    output_path = os.path.join(output_dir, "_extract_col_%s_from_%s.csv"%("__".join(columns), get_file_name(path)))
    assert path_is_not_a_file(output_path), "%s already exist : work already done ?"%(output_path)
    assert isinstance(columns, list), "%s should be a list"%(columns)
    print("Extract %s from %s by chunk of %s and store into %s (input path =%s)"%(columns, get_file_name(path),chunksize, output_dir,  path))
    csv_reader = pd.read_csv(path, chunksize=100000, sep=sep, error_bad_lines = False)
    n_ligne =0
    with open(output_path, "w") as output_file:
        header_written = False
        for df in csv_reader:
            if not header_written:
                assert all([ x in df.columns for x in columns]), "%s not in DF cols (%s)"%(columns, df.columns)
                output_file.write(df.ix[:,columns].to_csv(index=False, sep=sep))
                header_written = True
            else:
                output_file.write(df.ix[:,columns].to_csv(index=False, header=False, sep=sep))
                n_ligne += chunksize
                print(n_ligne)
    print("%s lines written in %s"%(n_ligne, output_path))
def transform_csv_into_excel(path_csv):
    """

    """
    import pandas as pd
    output_path = path_csv[:-4] + ".xls"
    writer = pd.ExcelWriter(output_path)
    df = pd.read_csv(path_csv)
    df.to_excel(writer)
    writer.save()
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

    path = path_to_excel_file
    short_filename = path.replace("/", "").replace(".xlsx", "").replace(".", "");
    print("Going to read : %s" % path);
    sys.stdout.flush()
    start_reading = time.time()                             			; print("Reading")                                 ; sys. stdout.flush()
    data           = pd.read_excel( path, sheetname= list(range( n_worksheet)))
    print("Read in %s"%(time.time() - start_reading)); sys.stdout.flush()
    for worksheet in list(data.
                                  keys()):
        try:
            print("Wk %s"% worksheet); sys.stdout. flush()
            output_path   = "%s%s_worksheet_%s.csv"%(output_dir, short_filename,worksheet)
            print("Saving into %s"%(output_path))
            sys.stdout.flush()
            start_saving = time.time()
            data[worksheet].to_csv ( output_path, encoding='UTF-8')
            print( "Saved in %s"%(time . time()-start_saving))
        except Exception as e:
            print( "Erreur in worksheet %s"% worksheet)
            sys.stdout.flush()
        print(e[:100])
        sys.stdout.flush()
def change_commas_to_dots_in_dir(directory_path):
    """
        Retrieve all the csv under a root dir, and apply the change_commas_to_dots function to each.

        Args:
            directory_path (str): path to the root directory

        Returns:
            nothing
    """
    paths = get_all_csvs_underdir(directory_path)
    list(map(lambda path: change_commas_to_dots(path), paths))
def change_commas_to_dots(file_path):
    """
        Apply the shell sed command to change commas to dot on a filepath.

        Returns: nothing.
    """
    from subprocess import call
    call(["sed", "-i", "s/,/\./g", file_path])
def dico_from_two_col_tsv(fsv_path, separator ="\t"):
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
def find_delimiter(path_to_csv_file, encoding="utf-8", debug=False):
    """
        Test delimiters ([,], [;], [\t]) and send back the one more likely to be.

        Usage :
            Useful to find the delimiter of a csv file.
    """
    sep_to_test = [",", ";", "\t", "|"]
    with open(path_to_csv_file, encoding="utf-8") as csv_file:
        for headers in csv_file:
            occurences = [len(headers.split(x)) for x in sep_to_test]
            if debug: print(occurences)
            max_       = occurences.index(max(occurences))
            return sep_to_test[max_]


def get_headers(path_to_csv_file):
    """
        Open a csv file and create a striped array of the first line splitted by auto-detected separator.

        return: array

    """
    import csv
    with open(path_to_csv_file) as csv_file: csv_reader 	= csv.reader(
                                                                     csv_file, delimiter=find_delimiter(path_to_csv_file))
    for line in csv_reader:
        return [field.strip() for field in


line]
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
    # 1) USER INFO : print( "-"*50)print( " "* 20, "Creating random extract")
    print("-" * 50)
    print("input dir = %s" % (input_dir))
    print("%s files : [%s]" % (len(onlycsv), ",".join(onlycsv)))
    print("output dir = %s" % (output_dir))
    print("Selecting %s lines within the %s first." % (nb_lines, max_line))
    # 2) READING FILES
    for csv_path in onlycsv:
        random_lines = np.random.randint(1, max_line, size=nb_lines)  # SELECTING RANDOM LINES
        current_line = 0
        nb_written_lines = 0
        to_print = ""
        print("Dealing with : %s " % (csv_path))
        with open(csv_path, "r") as inputs:
            output_file = csv_path[:-4] + "_random_%s_lines.csv" % (nb_lines)
            with open(output_file, "w") as output:
                for line in inputs:
                    current_line += 1

                    if current_line == 1:  # WE SAVE THE HEADERS
                        to_print = line
                        continue

                    if current_line in random_lines:  # WE WRITE OUT THE RANDOM LINES
                        to_print += line
                        nb_written_lines += 1

                    if current_line % 100000 == 0:
                        output.write(to_print)
                        to_print = ""
                        print("Line %s : wrote %s lines out of %s wanted. (%.2f pct) " % (
                            current_line, nb_written_lines, nb_lines, nb_written_lines / nb_lines))
                    if nb_written_lines >= nb_lines:
                        break
                    if current_line >= max_line:
                        break
                output.write(to_print)
def extract_n_lines(input_dir, nb_lines):
    """
        Find all the csv under the input_dir and create an extract for each one.
    """

    for csv_path in get_all_csvs_underdir(input_dir):
        current_line = 0
        print("Dealing with : %s " % (csv_path))

        with open(csv_path, "r") as inputs:
            output_file = csv_path[:-4] + "_extract_%s.csv" % (nb_lines)
            with open(output_file, "w") as output:
                for line in inputs:
                    output.write(line)
                    current_line += 1
                    if current_line == nb_lines:
                        break
def count_separator(file_path, delimiter=','):
    """
        Read a file, line by line, for each line, fetch the nb of delimiter.
        If the nb of delimiter change, print a message and the line number
    """
    import sys
    num_line = 0
    last_nb_delimiter = 0

    with open("%s_strange_lines.csv" % (file_path), "w") as output:
        output.write("count_separator(%s, delimiter=%s)\n" % (file_path, delimiter))
        with open(file_path, "r") as inputs:
            for line in inputs:
                num_line += 1
                nb_delimiter = line.count(delimiter)
                if nb_delimiter != last_nb_delimiter:
                    print("%s/%s," % (num_line, nb_delimiter))
                    last_nb_delimiter = nb_delimiter
                    output.write(line)
                if num_line % 500000 == 0:
                    print(num_line, " ")
                    sys.stdout.flush()
def strip_csvs(directory_path):
    """
        Take a directory, and strip the values contained in the csvs.

        PARAMETERS:
            directory_path : directory where to search for csvs (must end with an [/])

        RETURN :
            create a '_small_' file for each file in the list (on the same directory list)
    """

    from os import listdir
    from os.path import isfile, join
    """
        PARAMETERS
    """
    if not directory_path.endswith("/"):
        directory_path = "%s/" % (directory_path)
    path = directory_path

    onlycsv = [f for f in listdir(path) if isfile(join(path, f)) if f.endswith(".csv")]
    # onlycsv = [	"H_OPRT_ACTE.csv"]

    separator = ";"
    unwanted_values = []
    default_value = ''

    """
        ALGO
    """
    for csv in onlycsv:
        big = path + csv
        small = big[:-4] + "_small_.csv"
        with open(big, "r") as too_big:
            with open(small, "w") as smaller:
                print("Reducing :\n %s\n to:\n %s " % (too_big, smaller))
                for line in too_big:
                    chunks = [x.strip() for x in line.split(separator)]
                    # chunks = [ x if x not in unwanted_values else default_value for x in chunks ]
                    smaller.write(separator.join(chunks))
                    smaller.write("\n")
                print("--")
def find_common_key(path, onlycsv):
    import csv
    """
        (2) populate a dictionnary with a table of fields by csv
            +
            populate 2 identical sets with the distincts fields values
    """
    fields = set()
    commonfields = set()
    joignable_csv = []

    for file_name in onlycsv:
        with open(path + file_name) as input_file:
            csv_reader = csv.reader(input_file, delimiter=find_delimiter(path + file_name))
            if debug: print("%s delimiter = %s " % (file_name, find_delimiter(path + file_name)))
            for line in csv_reader:
                headers[file_name] = [field.strip() for field in line]
                if debug: print("headers = %s" % (headers))
                for field in headers[file_name]:
                    fields.add(field)
                    commonfields.add(field)
                    nb_file_by_key[field] += 1
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
    print("=" * 50)
    print("Looking for common key in : %s " % (onlycsv))
    commonkey = False

    try:
        commonkey = next(iter(commonfields))
    except :
        print("no commonkey")
        best_key = [(k ,v) for (k, v) in list(nb_file_by_key.items()) if v == max(nb_file_by_key.values())][0]
        print("best key : %s over %s files " % (best_key[0], best_key[1]))
        commonkey = best_key[0]
        joignable_csv = []
        for file_name in headers:
            joignable = False
            for key in headers[file_name]:
                if key == commonkey: joignable = True

            if joignable: joignable_csv.append(file_name)

    print("joignable_csv with this key : \n  |--> %s" % ("\n  |--> ".join(joignable_csv)))
    print("commonfields = %s" % (commonfields))
    print("choosen key --> %s" % (commonkey))
    print("=" * 50)
    return commonkey, joignable_csv
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
    from . import functions_de_decouverte_de_fichiers
    path = path_to_excel_file
    short_filename = functions_de_decouverte_de_fichiers.get_file_name(path) + ".csv";
    print("Going to read : %s" % path);
    sys.stdout.flush()
    start_reading = time.time();
    print("Reading");
    sys.stdout.flush()
    data = pd.read_excel(path, sheetname=list(range(n_worksheet)));
    print("Read in %s" % (time.time() - start_reading));
    sys.stdout.flush()
    for worksheet in list(data.keys()):
        try:
            print("Wk %s" % worksheet)
            output_path = "%s%s_worksheet_%s.csv" % (output_dir, short_filename, worksheet);
            start_saving = time.time();
            print("Saving into %s" % (output_path));
            sys.stdout.flush()
            data[worksheet].to_csv(output_path, encoding='UTF-8');
            print("Saved in %s" % (time.time() - start_saving))
        except Exception as e:
            print("Erreur in worksheet %s" % worksheet);
            sys.stdout.flush()
            print(e[:100]);
            sys.stdout.flush()
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
            l = ntpath.basename(c) + "," + h.replace("\n", " ")
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
    print("files = {")
    for path in csv_paths:
        print("'':'%s'," % (ntpath.basename(path)))
    print("}")
def get_directory_paths(directory, extension=None):
    """
    Generate the directory names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    import os, ntpath
    assert(os.path.isdir(directory)), "The 'directory' parameter is not a directory (%s)"%(directory)

    directory_paths = []  # List which will store all of the full filepaths.
    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for directory in directories:
            # Join the two strings in order to form the full filepath.
            directory = os.path.join(root, directory)

            if not ntpath.basename(directory).startswith("."):
                directory_paths.append(directory)  # Add it to the list.

    if extension:return [x for  x in directory_paths if x.endswith(extension) ]

    return directory_paths  # Self-explanatory.
