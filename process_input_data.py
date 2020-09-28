#!/usr/local/bin/python3
import csv
import os
from generate_input_data import VB_FILENAME, DC_FILENAME, AMOUNT_OF_SECTORS, AMOUNT_OF_LEVELS, writeCsvFile

CB_FILENAME = os.path.join(os.path.dirname(os.path.abspath( __file__ )), 'output_data', 'cell_barcodes.csv')

def readCsvFileIntoDict(filename):
    result = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            result.append(row)
    return result


def parseStringToList(string_data):
    res = string_data.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
    res = res.split(',')
    return res

def resolveCells(sure_res, suspected_res):
    resolved_res = []
    suspected_res_still = []
    for suspected_cell in suspected_res:
        susp_barcodes = suspected_cell['barcodes']
        marker = None
        found = False
        for k in range(len(susp_barcodes)):
            marker = next((sure_item for sure_item in sure_res if sure_item['barcodes'][0] == susp_barcodes[k]), None)
            if marker:
                suspected_cell['barcodes'].pop(k)
                resolved_res.append(suspected_cell)
                found = True
            else:
                marker = next((resolved_item for resolved_item in resolved_res if resolved_item['barcodes'][0] == susp_barcodes[k]), None)
                if marker:
                    suspected_cell['barcodes'].pop(k)
                    resolved_res.append(suspected_cell)
                    found = True
        if not found:
            suspected_res_still.append(suspected_cell)

    sure_res.extend(resolved_res[:])
    suspected_res = suspected_res_still[:]
    return sure_res, suspected_res


def processInputData(video_barcodes, drone_cells):
    result = []
    sure_res = []
    suspected_res = []

    # объединение двух таблиц(списков) по полю timestamp
    for dc_item in drone_cells:
        row = list(filter(lambda vb_item: vb_item['timestamp'] == dc_item['timestamp'], video_barcodes))
        row = row[0]
        result.append({'level': int(dc_item['level']), 'sector': int(dc_item['sector']), 'barcodes': parseStringToList(row['barcodes'])})

    # 1-й проход - разделение на распознанные правильно (1 баркод в ячейке) и не правмльно (2 баркода в ячейке)
    for res_item in result:
        if len(res_item['barcodes']) == 1:
            sure_res.append(res_item)
        elif len(res_item['barcodes']) == 2:
            suspected_res.append(res_item)

    if len(suspected_res) != 0:
        # 2-й проход - поиск дубликатов (в ячейках с двумя баркодами) в правильно распознанных ячейках
        sure_res, suspected_res = resolveCells(sure_res, suspected_res)

    if len(suspected_res) == 0:
        fullyResolved = True
    else:
        # 3-й проход - дополнительный поиск дубликатов (в ячейках с двумя баркодами) в правильно распознанных ячейках
        sure_res, suspected_res = resolveCells(sure_res, suspected_res)
        if len(suspected_res) == 0:
            fullyResolved = True
        else:
            sure_res.extend(suspected_res)
            fullyResolved = False
            print('Unresolved {0} cells'.format(len(suspected_res)))

    # Добавление пустых ячеек
    for sec_numb in range(AMOUNT_OF_SECTORS):
        for lev_numb in range(AMOUNT_OF_LEVELS):
            if lev_numb != 0:
                cell = list(filter(lambda sure_item: sure_item['level'] == lev_numb and sure_item['sector'] == sec_numb, sure_res))
                if not cell:
                    sure_res.append({'level': lev_numb, 'sector': sec_numb, 'barcodes': None})

    return sorted(sure_res, key=lambda item: (item['sector'], item['level'])), fullyResolved


def getCellBarcodes(video_barcodes, drone_cells):
    res, ok = processInputData(video_barcodes, drone_cells)
    writeCsvFile(res, CB_FILENAME)
    return res


if __name__ == '__main__':
    vb = readCsvFileIntoDict(VB_FILENAME)
    dc = readCsvFileIntoDict(DC_FILENAME)
    res = getCellBarcodes(vb, dc)
    # for row in res:
    #     print(row)
