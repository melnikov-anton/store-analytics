from flask import Flask
from flask import render_template, redirect, url_for
from generate_input_data import generateInputData, VB_FILENAME, DC_FILENAME
from process_input_data import readCsvFileIntoDict, getCellBarcodes, parseStringToList, CB_FILENAME
import os



app = Flask(__name__)

@app.route('/')
def index():
    cells_barcodes = readCsvFileIntoDict(CB_FILENAME)

    return render_template('index.html', cells = cells_barcodes)

@app.route('/newdata')
def newdata():
    generateInputData()
    vb = readCsvFileIntoDict(VB_FILENAME)
    dc = readCsvFileIntoDict(DC_FILENAME)
    getCellBarcodes(vb, dc)
    return redirect(url_for('index'))

@app.route('/unresolveddata')
def unresolved():
    vb = readCsvFileIntoDict(os.path.join(os.path.dirname(os.path.abspath( __file__ )), 'input_with_unresolved', 'video_barcodes.csv'))
    dc = readCsvFileIntoDict(os.path.join(os.path.dirname(os.path.abspath( __file__ )), 'input_with_unresolved', 'drone_cells.csv'))
    getCellBarcodes(vb, dc)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
