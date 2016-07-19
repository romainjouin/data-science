import pandas           as pd
import extra_pandas
import decouverte
import class_extra      as extra
import pandas           as pd
import seaborn          as sns
import useful_functions as useful
import matplotlib
import datetime

reload(extra_pandas)
import matplotlib.pyplot as plt
import randstad
import extend_import
import stats_functions

finder = extend_import.NotebookFinder()
loader = extend_import.NotebookLoader()

try:
	matplotlib.style.use('ggplot')
except Exception as e:
	print e

data_dir = "/Users/romain/Informatique/randstad/randstad_local/zz_data"

#path ="/Users/romain/Informatique/randstad/randstad_local/notebooks/functions_envoie_d_emails" 	; envoie_d_emails = finder.find_module(path).load_module(path)
#path = "/Users/romain/Informatique/randstad/randstad_local/notebooks/functions_divers" 			; divers          = finder.find_module(path).load_module(path)

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

print "(The following list is post treatment)"
print "import pandas           as pd"
print "import extra_pandas"
print "import decouverte"
print "import class_extra      as extra"
print "import pandas           as pd"
print "import seaborn          as sns"
print "import useful_functions as useful"
print "import matplotlib"
print "import datetime"
print "matplotlib.style.use('ggplot')"
print "reload(extra_pandas)"
print "import matplotlib.pyplot as plt"
print "import randstad"
print "import extend_import"
print ""
print "finder = extend_import.NotebookFinder()"
print "loader = extend_import.NotebookLoader()"
print ""
print ""
print "data_dir = \"/Users/romain/Informatique/randstad/randstad_local/zz_data\""
print ""
print "path =\"functions_envoie_d_emails\" 	; envoie_d_emails = finder.find_module(path).load_module(path)"
print "path = \"functions_divers\" 			; divers          = finder.find_module(path).load_module(path)"
print ""
print "from matplotlib import rcParams"
print "rcParams.update({'figure.autolayout': True})"
