def map_bokeh(inputs ):
    print inputs
    import sys
    import pandas     as pd
    import numpy      as np
    import shapefile
    import bokeh
    from bokeh.io         import output_notebook
    from bokeh.models     import HoverTool
    from bokeh.plotting   import figure, ColumnDataSource
    from bokeh.plotting   import *
    from sortedcontainers import SortedSet
    import matplotlib.pylab
    sys.path.append("/Users/romain/Informatique/notebooks/python/")
    import extend_import
    from imports import *
    function_randstad     = "function_randstad"
    f_rand = finder.find_module(function_randstad).load_module(function_randstad)
    output_notebook()
    %matplotlib inline
    inputs
    
    #france_hors_zdc = inputs[0] 
    #nb_unite_by_cp  = inputs[1] 
    #unite_hors_zdc = inputs[2] 
    #unite_dans_zdc= inputs[3] 
    """
    import time
    p  = figure()
    n_row = 100000
    n_row = 100000
    d = time.time()

    output_file("france_zdc_et_unites_%s.html"%d)
    print "france hors zdc", sys.stdout.flush()
    glyph  = p.patches(source =ColumnDataSource(france_hors_zdc[:n_row]), xs = "lat", ys = "lng", fill_color="white",line_color="white")
    p.add_tools(HoverTool(renderers=[glyph], tooltips=[("cp", "@cp")], name="hors_zdc"))
    d1 = time.time()
    print d1-d

    print "zdc", sys.stdout.flush()
    source = ColumnDataSource(nb_unite_by_cp[['lat', 'lng','cp_y', 'unite', 'unites', 'color']][:n_row])
    glyph  = p.patches(source =source, xs = "lat", ys = "lng", fill_color="color",)
    p.add_tools(HoverTool(renderers=[glyph], tooltips=[("cp", "@cp_y"), ("nb unite", "@unite"), ("liste unites", "@unites")], name="zdc"))
    d2 = time.time()
    print d2-d1


    print " unités hors zdc", sys.stdout.flush()
    source =ColumnDataSource(unite_hors_zdc[[u'unit', u'pool', u'X_lambert93', u'Y_Lambert93']][:n_row])
    glyph  = p.circle(source =source , x = u'X_lambert93', y = u'Y_Lambert93', color="red")
    p.add_tools(HoverTool(renderers=[glyph], tooltips=[("pool", "@pool"), ("unite", "@unit")], name="pool_units"))
    d3 = time.time()
    print d3-d2

    print " unités dans zdc", sys.stdout.flush()
    source =ColumnDataSource(unite_dans_zdc[[u'unit', u'pool', u'X_lambert93', u'Y_Lambert93']][:n_row])
    glyph  = p.circle(source=source, x = u'X_lambert93', y = u'Y_Lambert93', color="orange")
    p.add_tools(HoverTool(renderers=[glyph], tooltips=[("pool", "@pool"), ("unite", "@unit")], name="pool_units"))
    d4 = time.time()
    print d4-d3

    show(p)
    d5 = time.time()
    print "show = ", d5-d4
    print "total time = ", d5-d
    total_times.append(d5-d)

    print total_times
    """