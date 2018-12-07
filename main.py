"""Main file to data analysis."""
from app.analysis import main_analysis
from time import time
ts = time()
main_analysis(8)
print(time() - ts)
# plot_bar()
# from app.db.models import create_tables
# create_tables()
# from app.dataimports import import_data
# import_data('click_data')
