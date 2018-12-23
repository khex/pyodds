# https://docs.python.org/3/library/argparse.html
%matplotlib inline
import numpy as np
from docopt import docopt
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.collections as collections

args = docopt(__doc__)
print(args['<team_name>'])

MONGODB_URI = "mongodb://stavros:balalajka7@ds057934.mongolab.com:57934/deltabase"
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

team = "Texas Rangers"
seas = "2017-2018"

query = {'league': 'nba', 'seas_year': seas, 'seas_type': 'season',
         '$or': [{'home.team': team}, {'away.team': team}]}
match_list = db.matches.find(query).sort([('date.iso', 1)])  # [30:]

arry = [[[0.0] for n in range(3)] for m in range(4)]
lbls = ['Line', 'Asian Handycap', 'Total', 'Individ. Total']

# for match in match_list:
#    print(match['date']['datetime'])

for match in match_list:
    place = 'home' if match['home']['team'] == name else 'away'
    m = match[place]["ftot"]

    for n in range(4):
        arry[n][0].append(m["resalt"][n])
        arry[n][1].append(m["oddval"][n])
        arry[n][2].append(m["delta"][n])

for i in range(4):
    r = arry[i]
    fig, ax = plt.subplots(figsize=(17, 5))
    ax.set_title(lbls[i])
    X, d_Y = range(len(r[0])), np.array(r[2])

    ax.plot(X, r[0], color='green', label='Resalt')
    ax.plot(X, r[1], color='red', label='Value')
    ax.plot(X, r[2], color='m')  # , ls = ' - ')

    m_arr = r[0] + r[1] + r[2]
    max_haight, min_haight = max(m_arr), min(m_arr)

    # from official collection documentation
    ax.add_collection(collections.BrokenBarHCollection.span_where(
        X, ymin=0, ymax=max_haight, where=d_Y >= 0, facecolor='green', alpha=0.25))
    ax.add_collection(collections.BrokenBarHCollection.span_where(
        X, ymin=min_haight, ymax=0, where=d_Y < 0, facecolor='red', alpha=0.25))

    ax.legend(loc='best', fancybox=True)

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Generate the data
data = np.random.randn(15, 1024)

# The PDF document
pdf_pages = PdfPages('barcharts.pdf')

# Generate the pages
plots_count = data.shape[0]
plots_per_page = 5
pages_count = int(np.ceil(plots_count / float(plots_per_page)))
grid_size = (plots_per_page, 1)
for i, samples in enumerate(data):
    
    # Create a figure instance (ie. a new page) if needed
    if i % plots_per_page == 0:
    fig = plt.figure(figsize=(8.27, 11.69), dpi=100)
    
    # Plot one bar chart
    plt.subplot2grid(grid_size, (i % plots_per_page, 0))
    plt.hist(samples, 32, normed=1, facecolor='.5', alpha=0.75)
    
    # Close the page if needed
    if (i + 1) % plots_per_page == 0 or (i + 1) == plots_count:
    plt.tight_layout()
    pdf_pages.savefig(fig)
    
    # Write the PDF document to the disk
    pdf_pages.close()


    fig = plt.figure(figsize=(11.69, 8.27), dpi=100)
    plt.xticks(dlina, short_names, ha='left', rotation='vertical', fontsize=12)
    ax = plt.axes()
    ax.set_title('{}: {}'.format(game_place[r], odds_type[i]))
    bars = ax.bar(dlina, data, color=clrs)  
    pdf_pages.savefig(fig)
