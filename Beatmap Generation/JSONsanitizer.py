import json
from pprint import pprint

# 0 - Time
# 1 - Index
# 2 - Layer
# 3 - Type
# 4 - Direction

# Print JSON beatmap
def print_json():
  pprint(data)

# Converts JSON to vector output
def json_to_notes(file):
  data = json.loads(file)
  output = []
  attr = []
  for note in data.get('_notes'):
      for key in note.keys():
          attr.append(note[key])
      output.append(attr)
      attr = []
  return output

# Get the obstacle list
def json_to_obstacles():
  output = []
  for obstacle in data.get('_obstacles'):
      output.append(obstacle)
  return output

# Get BPB
def get_bpb(file):
  data = json.loads(file)
  return data.get('_beatsPerBar')

# Get BPM
def get_bpm(file):
  data = json.loads(file)
  return data.get('_beatsPerMinute')

# Get note jump speed
def get_note_jump_speed(file):
  data = json.loads(file)
  return data.get('_noteJumpSpeed')

def get_times_from_list(file):
  notes = json_to_notes(file)
  output = []
  for note in notes:
    output.append(note[0])
  return output

def get_attr_from_list(file, idx):
  notes = json_to_notes(file)
  output = []
  for note in notes:
    output.append(note[idx])
  return output

# Test Func
# print_json()
# pprint(json_to_notes())
# print(json_to_obstacles())
# print(get_bpm())
# print(get_bpb())
# print(get_note_jump_speed())
# print(get_times_from_list())
# print(get_attr_from_list(3))




