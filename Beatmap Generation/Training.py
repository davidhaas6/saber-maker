import os
from JSONsanitizer import *
import sys
import json

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

expertP_json = get_files("ExpertPlus")
expert_json = get_files("Expert")
normal_json = get_files("Normal")
easy_json = get_files("Easy")

# for file in expert_json:
#   print(file)

def training_data(files):
  r = []
  for file in files:
    f=open(file, "r")
    r.append(f.read())
  return r

# print(json_to_notes(training_data(easy_json)[0]))

def format_output(note_list):
  t = []
  for i in range(len(note_list)):
    t.append(note_list[i][0])
  print(t)
  for i in range(note_list[len(note_list)-1][0]):
    if(i in t):
      sys.stdout.write(str(i) +': x')
      for j in range(t.count(i)-1):
        sys.stdout.write('x')
      sys.stdout.write('\n')
    else:
      sys.stdout.write(str(i) +': -\n')

# print(training_data(expertP_json)[0])
# notes = json_to_notes(training_data(expertP_json)[0])
# format_output(notes)

def pattern_conversion(file):
  text = json.loads(open(file, "r").read())
  output = []
  attr = ''
  keys = ['_lineIndex','_lineLayer','_cutDirection','_type']
  for note in text.get('_notes'):
      for key in keys:
          attr += str(note[key])
      output.append(attr)
      attr = ''
  return output

def find_unique_note_types(files):
  r = []
  for file in files:
    text = json.loads(open(file, "r").read())
    output = []
    attr = ''
    keys = ['_lineIndex','_lineLayer','_cutDirection','_type']
    for note in text.get('_notes'):
        for key in keys:
            attr += str(note[key])
        output.append(attr)
        attr = ''
    r.append(output)
  return r

def get_unique_notes(song_list):
  patterned_song_list = find_unique_note_types(song_list)
  notes_set = set()
  for song in patterned_song_list:
    for note in song:
      if note not in notes_set:
        notes_set.add(note)
  return notes_set

def unique_minus_bombs(note_list):
  r = []
  for note_type in sorted(unique_notes):
    if(not note_type.endswith('3')):
      r.append(note_type)
  return r

def all_note_types():
  r = []
  for i in range(4):
    for j in range(3):
      for k in range(9):
        for l in range(2):
          r.append(str(i) + str(j) + str(k) + str(l))
  return r

# print(unique_minus_bombs(unique_notes))
# print(len(unique_minus_bombs(unique_notes)))
# print(all_note_types())

# Get all unused note types
  # unique_notes = get_unique_notes(expertP_json)
  # all_notes = all_note_types()
  # used_notes_minus_bombs = unique_minus_bombs(unique_notes)
  # diff = list(set(all_notes) - set(used_notes_minus_bombs))
  # print(diff)

def pretty_printout(file):
  text = open(file, "r").read()
  bpm = get_bpm(text)
  bpb = get_bpb(text)
  njs = get_note_jump_speed(text)
  data = json.loads(text)
  line_index = get_attr_from_list(text,1)
  line_col = get_attr_from_list(text,2)
  print("Bpm " + str(bpm) + " Bpb " + str(bpb) + " Njs " + str(njs))
  beat_list = get_times_from_list(text)
  total_beats = beat_list[len(beat_list) - 1]
  line = ['-','-','-','-']
  count = 0
  adjusted_beats = [int(round(i * 4)) for i in beat_list]
  print(adjusted_beats)
  for beat in range(int(adjusted_beats[len(beat_list)-1])):
    if(beat in adjusted_beats):
      sys.stdout.write(str(beat) + ": ")
      line[line_index[count]] = str(line_col[count])
      list_print(line)
      count +=1
    else:
      sys.stdout.write(str(beat) + ": ")
      list_print(line)
    line = ['-','-','-','-']

def first_non_zero_time(list):
  time_list = list
  print(time_list)
  for time in time_list:
    if(time != 0):
      return time
  return 0

def list_print(list):
  for item in list:
    sys.stdout.write(item)
  sys.stdout.write('\n')

# Styled vertical prinout
file = expertP_json[75]
# pretty_printout(file)
# print(file)