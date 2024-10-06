import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import url_for
from config import GRAPH_FOLDER


#plotHistorgram(,'product_quantity.png')
def plotHistogram(marksFrequencyDictonary,filename,title,xlabel,ylabel):
    data=marksFrequencyDictonary
    print(data)
    marks = list(data.keys())
    print(marks)
    frequencies = list(data.values())
    print(frequencies)
    
    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(marks, frequencies, color ='#2AAA8A',
            width = 0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    #plt.show()
    print('########Image directory',url_for('display_graph_file', filename= filename))
   # plt.savefig(url_for('display_graph_file', filename= filename))
    plt.savefig(GRAPH_FOLDER+'/'+filename) 