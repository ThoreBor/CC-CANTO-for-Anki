import sqlite3
import re
from progressbar import *
import sys

conn = sqlite3.connect('CC-CANTO.db')
c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS dictionary(hanzi_trad TEXT, hanzi_simp TEXT, jyutping TEXT, eng TEXT)')

def data_entry(hanzi_trad, hanzi_simp, jyutping, eng):
	c.execute('INSERT INTO dictionary (hanzi_trad, hanzi_simp, jyutping , eng) VALUES(?, ?, ?, ?)', (hanzi_trad, hanzi_simp, jyutping, eng))


def txt_to_database(fname):
	counter = 0
	total = 0

	with open(fname, encoding="utf8") as f:
		for line in f:
			total += 1

	widgets = [FormatLabel(''), ' ', progressbar.Bar('=', '[', ']'),' ', Percentage(),' ', ETA()]
	bar = ProgressBar(maxval=total, widgets=widgets)
	bar.start()

	with open(fname, encoding="utf8") as f:
		for line in f:
			bar.update(counter)
			widgets[0] = FormatLabel('Entry: '+str("{:,}".format(counter))+"/"+ str("{:,}".format(total)))
			counter = counter +1 
			characters =  line.split(" ")
			hanzi_trad = characters[0]
			hanzi_simp = characters[1]
			jyutping = line.split("{")[1]
			jyutping = jyutping.split("}")[0]
			eng = line.split("}")[1]
			eng = eng.replace("# adapted from cc-cedic", "")
			eng = eng[2:-2]
			data_entry(hanzi_trad, hanzi_simp, jyutping, eng)

	bar.finish()

if len(sys.argv) != 2:
	print("No file name provided. Run database.py filename.txt")
	quit()
fname = sys.argv[1:]
create_table()
txt_to_database(fname[0])
conn.commit()