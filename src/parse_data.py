import glob
import pickle
import json
import numpy as np
from tinytag import TinyTag
import os

data_path = "data/nn_labels/"
out_dir = "data/ground_truth/"


def trunc_tenth(num):
    return int(num*100)/float(100)


def generate_onset_map(json_data, do_i_pickle):
    with open(str(filename), encoding='utf-8') as json_data:
        level = json.load(json_data)
        firstslash = filename.find('/', filename.find('/')+1)
        lastslash = filename.find('/', firstslash+1)
        outfile = filename[firstslash+1:lastslash]
        ogg_path = glob.glob(filename[0:filename.rfind('/')+1] + "*.ogg")[0]

        frame_period = .01
        num_notes = len(level['_notes'])
        beats_per_second = level['_beatsPerMinute'] / 60
        song_length = TinyTag.get(ogg_path).duration
        num_frames = int(song_length / frame_period)

        onset_map = np.zeros(num_frames, dtype=np.bool)
        errcnt = 0
        goodcnt = 0
        for note in level['_notes']:
            time_occurence = note['_time'] / beats_per_second
            try:
                onset_map[int(
                    round(trunc_tenth(time_occurence)/frame_period))-1] = 1
                goodcnt += 1
            except:
                # print("\n" + filename)
                # print("songlength:", song_length, " bps:", beats_per_second)
                # print("note:", round(note['_time'], 1),
                #       " time: ", time_occurence)
                errcnt += 1

        if errcnt > (.2 * goodcnt):
            print("Error reading song: ", filename)
            return

        if do_i_pickle:
            pickling_on = open(out_dir + outfile + "_label.pickle", "wb")
            pickle.dump(onset_map, pickling_on)
            pickling_on.close()

        unique, counts = np.unique(onset_map, return_counts=True)
        #print(outfile, song_length, level['_beatsPerMinute'])


# for root, dirs, files in os.walk(data_path):
#     for name in files:
#         if name == "Hard.json":
#             print(root+dirs+files)

for filename in glob.iglob(data_path + '**/Hard.json', recursive=True):
    try:
        generate_onset_map(filename, True)
    except Exception as e:
        print(e)
