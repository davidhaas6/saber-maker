import json
import sys
import numpy as np
import Training
import model_test as model
import Preprocessing
import os.path

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("use: main.py data_path output_file_path")
        sys.exit()

    search_path = sys.argv[1]
    output_path = sys.argv[2]
    export_beatmap()


pattern = Preprocessing.dont_touch_this(model.create_pattern())
with open('Believer/Expert.json') as f:
    beatmap_json = json.load(f)

def dir_frequencies():
	#ret=[[[0]*4]*3]*9
	expert_json = Training.expert_json
	prob = dict()
	for i in range(3):
		for j in range(4):
			prob[(i,j)] = [0]*9 # row, column
	for song in Training.training_data(expert_json)[:100]:
		notes = json.loads(song)['_notes']
		for note in notes:
			j = note['_lineIndex']
			i = note['_lineLayer']
			direction = note['_cutDirection']
			prob[(i,j)][direction] += 1

	for key in prob.keys():
		prob[key] = [float(i)/sum(prob[key]) for i in prob[key]]

	return prob

def color_frequencies():
	#ret=[[[0]*4]*3]*9
	expert_json = Training.expert_json
	colors = dict()
	for i in range(3):
		for j in range(4):
			colors[(i,j)] = [0]*4 # row, column
	for song in Training.training_data(expert_json)[:100]:
		notes = json.loads(song)['_notes']
		for note in notes:
			j = note['_lineIndex']
			i = note['_lineLayer']
			block = note['_type']
			colors[(i,j)][block] += 1

	for key in colors.keys():
		colors[key] = [float(i)/sum(colors[key]) for i in colors[key]]

	return colors

def compile_notes():
	prob = dir_frequencies()
	colors = color_frequencies()
	fake = beatmap_json.copy()
	for i,note in enumerate(fake['_notes']):
		layer = pattern[i][0]
		index = pattern[i][1]
		note['_lineLayer'] = int(layer)
		note['_lineIndex'] = int(index)
		note['_cutDirection'] = np.random.choice(list(range(9)), p=prob[(int(layer),int(index))])
		note['_type'] = np.random.choice(list(range(4)), p=colors[(int(layer),int(index))])
	return fake

def trim_beatmap():
	beatmap = compile_notes()
	beatmap.pop('_obstacles')
	unique_notes = []
	times = [""]*len(beatmap['_notes'])
	unique_notes = [""]*len(beatmap['_notes'])
	for i,note in enumerate(beatmap['_notes']):
		if (note['_time']) not in times:
			times[i] = note['_time']
			unique_notes[i] = note
		else:
			current_note = unique_notes[times.index(note['_time'])]
			if (current_note['_lineIndex'] == note['_lineIndex']) and (current_note['_lineLayer'] == note['_lineLayer']) or (current_note['_type'] == note['_type']):
				beatmap['_notes'].remove(note)
	return beatmap

def export_beatmap():
	save_path = 'C:/Program Files (x86)/Steam/steamapps/common/Beat Saber/CustomSongs/Believer - Copy/'
	completeName = os.path.join(save_path, "Expert.json")         
	file1 = open(completeName, "w")
	file1.write(str(trim_beatmap()))
	file1.close()