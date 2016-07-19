# -*- coding: utf-8 -*-
__author__ = 'romain'


def is_file(path):
    """
    Check either the given path is a file
    :param path: path to check
    :return: Boolean
    """
    return path_is_file(path)

def is_dir(dirpath):
    """
    Check either a path is a directory.
    :param dirpath: path to check
    :return:Boolean
    """
    return path_is_dir(dirpath)

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
            print "moving %s \n to: %s"%(old_path, new_path)
            os.rename(path, new_path)
        print "%s \n equals \n%s\n" %(new_path, old_path)


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
        print "pbm"
        return False


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
                print "Wrote %s lines into %s."%(n_written, output_path)
                print "Target dir = %s"%(output_dir)

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
                    input_file.next()
                    for line in input_file:
                        outputfile.write(line)
    except Exception as e:
        print "pbm in concatenate_csv: %s"%(e)


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



def list_csvs():
    """
    list randstad csvs
    :return:
    """
    import ntpath, os
    print "-- BEGIN --"
    assert path_is_dir("/home/romain/informatique/memorandum/randstad")

    try:
        separator   = ";"
        extension   = ("txt", "csv")
        root_dir    = "/home/romain/informatique/memorandum/randstad"
        paths       = get_filepaths(root_dir, extension)
        nb_ligne    =0

        with open(os.path.join(root_dir, "header.csv"), "w") as outputfile:
            for path in paths:
                index = 0
                for header in get_header(path, separator):
                    header  = header.replace('\n', ' ')
                    to_write = "%s%s%s%s%s\n"%(ntpath.basename(path), separator, header, separator,  index)
                    to_write = to_write.replace('\n', ' ')
                    outputfile.write (to_write )
                    index += 1
                    nb_ligne +=1
        print nb_ligne
    except AssertionError as e:
        print e
        print "__ END with Error__"

    print "END ok  :-) !"
def get_pig_load_statement(csv_path, sep):
    """

    :param csv_path: path where to find header on first line
    :param sep: csv separator
    :return: pig loading sentence (string)
    """
    assert is_file(csv_path)
    headers = get_headers(csv_path, sep)

    headers = ',\n\t'.join(map(lambda x: x.strip()+":chararray", headers)).replace(" ", "_").replace("'", "_").lower().replace("(", "").replace(")", "").replace("-", "_").replace(".", "_")
    return "%s = LOAD '%s' \n\t USING org.apache.pig.piggybank.storage.CSVExcelStorage('%s', 'NO_MULTILINE', 'NOCHANGE', 'SKIP_INPUT_HEADER')\n\t\
AS (%s);\n"%(get_file_name(csv_path), csv_path, sep,headers)

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
    return os.path.splitext(base)[0]


def explore(file, sep=";", top = 10):
    """

    """
    import pandas as pd
    print "*"*20
    #print "Exploring %s"%(get_file_name(file))
    to_explore = pd.read_csv(file, sep=";", error_bad_lines=False)
    cols = to_explore.columns
    i = -1
    for col in cols:
        i +=1
        serie = to_explore[col]
        null  = serie.isnull()
        not_null = len([x for x in null if not x])
        print "%s) %s"%(i,col)
        print not_null, " values not null out of ", nb_lignes, "(", not_null/nb_lignes, "), top %s :"%(top)
        s = serie.value_counts()
        d = s/not_null
        d = ["%.2f"%(x) for x in d]
        top_ = zip(s.index[:top], s.values[:top] , d)
        print top_,  "\n"
    print "="*50

def get_txt_and_csv(dir_path, txt_sep=";", csv_sep=";"):
    txt= get_filepaths(dir_path, ".txt" )
    csv= get_filepaths(dir_path, ".csv" )
    return txt+csv

def extract_column_from_csv(path, columns, output_dir, sep=';', chunksize=100000, debug=False):
    import pandas as pd
    import os
    assert is_file(path), "%s is not a file !"%(path)
    output_path = os.path.join(output_dir, "_extract_col_%s_from_%s.csv"%("__".join(columns), get_file_name(path)))
    assert path_is_not_a_file(output_path), "%s already exist : work already done ?"%(output_path)
    assert isinstance(columns, list), "%s should be a list"%(columns)
    print "Extract %s from %s by chunk of %s and store into %s (input path =%s)"%(columns, get_file_name(path),chunksize, output_dir,  path)
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
                print n_ligne
    print "%s lines written in %s"%(n_ligne, output_path)

def remove_string_from_file(path, to_search, replace_by=""):
    return replace_string_from_file(path, to_search, replace_by="")

def replace_string_from_file(path, to_search, replace_by=""):
    assert isinstance(to_search, list) or isinstance(to_search, str), "%ss should be a list or a string"%(to_search)

    print "Going to replace %s by [%s] from %s "%(to_search, replace_by, path)

    with open(path+"_small", "w") as f2:
        with open(path, "r") as f:
            if isinstance(to_search, list):
                print "Replacing an array"
                for l in f:
                    to_write = l
                    for to_be_replaced in to_search:
                        to_write = to_write.replace(to_be_replaced, replace_by)
                    f2.write(to_write)
            else:
                if isinstance(to_search, str):
                    print "Replacing a string"
                    for l in f:
                        to_write = l.replace(to_search, replace_by)
                        f2.write(to_write)
    print "end replacement for %s"%(path)


if __name__ == "__main__":
    import pandas as pd

    c ="/Users/nouveau/Documents/memorandum/randstad/HEC_2/REF_QUALIFS.txt"

    for x in get_header(c, ";"):
        print x

    exit(0)


    c = pd.DataFrame()

    print "debut"
    separator   = ";"
    dir_path    = "/Users/nouveau/Documents/memorandum/randstad/HEC/simple_copie"
    output_dir  = "/Users/nouveau/Documents/memorandum/randstad/HEC/simple_copie/"
    x = dir_path    + "/indicateurs.csv"
    csvs = get_filepaths(dir_path, ".txt")
    for csv in csvs :
        print get_pig_load_statement(csv, ";")
        print type([])
        c =  ["NUM_CONTRAT", "MATRICULECLI", "MAT_INT", "NUM_COMMANDE", "CA_REMISE", "UNITE"]
        d = [y.lower() for y in c ]

        extract_column_from_csv(x,d, output_dir)
        exit(0)

    csvs = get_filepaths(dir_path, ".csv")
    for csv in csvs :
        try:
            print get_pig_load_statement(csv, ";")
        except:
            print "pbm with %s"%(csv)
    print "fin"