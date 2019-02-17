import json
from pprint import pprint
import os, sys
import JSONsanitizer as JANitizer
import numpy as np
import model_test as model

with open('Believer/Expert.json') as f:
    beatmap_json = json.load(f)

with open('Believer/info.json') as g:
	info_json = json.load(g)

# pprint(beatmap_json)
# pprint(info_json)

# Song Information
author = info_json["authorName"]
difficultyLevels = info_json["difficultyLevels"]
audioPath = difficultyLevels[0]["audioPath"]
# print(audioPath)
	# There's also some information about the preview music when in the main menu

# Beatmap Information
bpb = beatmap_json["_beatsPerBar"]
bpm = beatmap_json["_beatsPerMinute"]
lighting_events = beatmap_json["_events"] #Ignore
	# _time, _type, _value
njs = beatmap_json["_noteJumpSpeed"]
notes = beatmap_json["_notes"]
	# _cutDirection 0-8, _lineIndex 0-3, _lineLayer 0-2, _time seconds, _type 0-2

# 1-hot encoding for note types
	# 2 note types (red and blue)
	# 12 note locations
	# 9 note directions
	# 216 total note types

def get_times(notes):
	times = []
	for i in range(len(notes)):
		times.append(notes[i]["_time"])
	return times

def get_notes_by_time(notes):
	times = {}
	for i,note in enumerate(notes):
		if note["_time"] not in times:
			times[note["_time"]] = str(note["_cutDirection"]) + str(note["_lineIndex"]) + str(note["_lineLayer"]) + str(note["_type"])
		else:
			times[note["_time"]] = [times[note["_time"]], str(note["_cutDirection"]) + str(note["_lineIndex"]) + str(note["_lineLayer"]) + str(note["_type"])]
	return times

def get_unique_notes(notes):
	notes_by_time = get_notes_by_time(notes)
	times = get_times(notes)
	unique_notes = []
	for time in times:
		if notes_by_time[time] not in unique_notes:
			unique_notes.append(notes_by_time[time])
	return unique_notes

# ijkl
# efgh
# abcd

one_hot = {'00':'a','01':'b','02':'c','03':'d','10':'e','11':'f',
'12':'g','13':'h','20':'i','21':'j','22':'k','23':'l',}

def one_hot_encode(note):
	return one_hot[str(note['_lineLayer'])+str(note['_lineIndex'])]

def better_one_hot(notes):
	times = get_times(notes)
	offset = times[0]
	ret = [' ']*(round(max(times)+1000)*12)
	for note in notes:
		if [round((note['_time']-offset)*12)] != ' ':
			ret[round((note['_time']-offset)*12)]+= one_hot_encode(note)
		else:
			ret[round((note['_time']-offset)*12)] = one_hot_encode(note)
	return ret

# print(one_hot_encode(notes))

def print_format(encoded):
	ret = ''
	for block in encoded:
		ret += block
	return ret.rstrip()


def list_files(dir):
  r = []
  for root, dirs, files in os.walk(dir):
    for name in files:
      r.append(os.path.join(root, name))
  return r

def get_files(ext):
  r = []
  file_list = list_files('C:/Program Files (x86)/Steam/steamapps/common/Beat Saber/CustomSongs')
  for file in file_list:
    if(file.endswith(ext + '.json')):
      r.append(file)
  return r

expert_json = get_files("Expert")

def training_data(files):
  r = []
  for file in files:
    f=open(file, "r")
    r.append(f.read())
  return r

# print(json.loads(training_data(expert_json)[0])['_notes'])
def beeg_yoshi():
	ret = ''
	for i in range(1):
		ret += print_format(better_one_hot(json.loads(training_data(expert_json)[i])['_notes']))
	return ret

def dont_touch_this(test_data):
	encoded = list(test_data.replace(" ", ''))
	reverse_dict = {'a':'00','b':'01','c':'02','d':'03','e':'10','f':'11',
	'g':'12','h':'13','i':'20','j':'21','k':'22','l':'23',}

	decoded = []
	for note in encoded:
		decoded.append(reverse_dict[note])
	return decoded