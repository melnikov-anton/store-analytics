#!/usr/local/bin/python3
import random
import string
import csv
import os
from datetime import datetime, timedelta


AMOUNT_OF_SECTORS = 16
AMOUNT_OF_LEVELS = 6
CELLS_FILLABILITY = 0.8
PROBABILITY_OF_DOUBLE_BARCODES = 0.1
EMPTY_CELL_VALUE = None

VB_FILENAME = os.path.join(os.path.dirname(os.path.abspath( __file__ )), 'input_data', 'video_barcodes.csv')
DC_FILENAME = os.path.join(os.path.dirname(os.path.abspath( __file__ )), 'input_data', 'drone_cells.csv')

AMOUNT_OF_CELLS = AMOUNT_OF_SECTORS * (AMOUNT_OF_LEVELS - 1)
AMOUNT_EMPTY_CELLS = int(AMOUNT_OF_CELLS * (1 - CELLS_FILLABILITY))
AMOUNT_OF_CELLS_WITH_TWO_BARCODES = int(AMOUNT_OF_CELLS * CELLS_FILLABILITY * PROBABILITY_OF_DOUBLE_BARCODES)
START_TIME = datetime.now() - timedelta(hours=2)
TIME_DELTA = timedelta(seconds=5)
START_TIMESTAMP = datetime.timestamp(START_TIME)

all_barcodes = []

def generateBarcode(length=10):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

def isFirst(sector_number):
    return sector_number == 0

def isLast(sector_number):
    return sector_number == (AMOUNT_OF_SECTORS - 1)

def fillCells():
    sectors = []
    current_time = START_TIME
    for sector_number in range(AMOUNT_OF_SECTORS):
        levels = []
        current_time += TIME_DELTA
        if (sector_number % 2) == 0:
            for level_number in range(AMOUNT_OF_LEVELS):
                if level_number == 0:
                    levels.append(None)
                else:
                    levels.append({'timestamp': datetime.timestamp(current_time), 'barcodes': [generateBarcode()]})
                current_time += TIME_DELTA
            sectors.append(levels[:])

        else:
            for level_number in range(AMOUNT_OF_LEVELS-1, -1, -1):
                if level_number == 0:
                    levels.append(None)
                else:
                    levels.append({'timestamp': datetime.timestamp(current_time), 'barcodes': [generateBarcode()]})
                current_time += TIME_DELTA
            levels.reverse()
            sectors.append(levels[:])

    # Создание пустых ячеек
    for i in range(AMOUNT_EMPTY_CELLS):
        lev_numb = random.randint(1, AMOUNT_OF_LEVELS-1)
        sec_numb = random.randint(0, AMOUNT_OF_SECTORS-1)
        while not sectors[sec_numb][lev_numb]:
            lev_numb = random.randint(1, AMOUNT_OF_LEVELS-1)
            sec_numb = random.randint(0, AMOUNT_OF_SECTORS-1)
        sectors[sec_numb][lev_numb] = EMPTY_CELL_VALUE

    # Создание ячеек с двумя баркодами
    two_barcodes_dells = 0
    while two_barcodes_dells < AMOUNT_OF_CELLS_WITH_TWO_BARCODES:
        lev_numb = random.randint(1, AMOUNT_OF_LEVELS-1)
        sec_numb = random.randint(0, AMOUNT_OF_SECTORS-1)
        delta = random.choice([1, -1])
        if (not isFirst(sec_numb)) and (not isLast(sec_numb)) and sectors[sec_numb][lev_numb] and sectors[sec_numb+delta][lev_numb]:
            sectors[sec_numb][lev_numb]['barcodes'].append(sectors[sec_numb+delta][lev_numb]['barcodes'][0])
            two_barcodes_dells += 1
        elif isFirst(sec_numb) and sectors[sec_numb][lev_numb] and sectors[sec_numb+1][lev_numb]:
            sectors[sec_numb][lev_numb]['barcodes'].append(sectors[sec_numb+1][lev_numb]['barcodes'][0])
            two_barcodes_dells += 1
        elif isLast(sec_numb) and sectors[sec_numb][lev_numb] and sectors[sec_numb-1][lev_numb]:
            sectors[sec_numb][lev_numb]['barcodes'].append(sectors[sec_numb-1][lev_numb]['barcodes'][0])
            two_barcodes_dells += 1

    return sectors


def generateVideoBarcode(store):
    result = []
    for sector in store:
        for level in sector:
            if level:
                result.append({'timestamp': level['timestamp'], 'barcodes': level['barcodes'][0:2]})
    return sorted(result, key=lambda item: item['timestamp'])


def generateDroneCells(store):
    result = []
    for sec_numb, sector in enumerate(store):
        for lev_numb, level in enumerate(sector):
            if level:
                result.append({'timestamp': level['timestamp'], 'level': lev_numb, 'sector': sec_numb})
    return sorted(result, key=lambda item: item['timestamp'])


def writeCsvFile(list_of_dicts, filename):
    with open(filename, 'w', encoding='utf8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list_of_dicts[0].keys())
        writer.writeheader()
        writer.writerows(list_of_dicts)


def generateInputData():
    store = fillCells()
    video_barcodes = generateVideoBarcode(store)
    drone_cells = generateDroneCells(store)
    writeCsvFile(video_barcodes, VB_FILENAME)
    writeCsvFile(drone_cells, DC_FILENAME)


if __name__ == '__main__':

    generateInputData()
