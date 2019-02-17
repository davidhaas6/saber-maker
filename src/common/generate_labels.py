import glob
import pickle
import json
import numpy as np
from tinytag import TinyTag
import os


def trunc_tenth(num):
    return int(num*100)/float(100)


def generate_onset_map(json_path, ogg_path):
    try:
        with open(str(json_path), encoding='utf-8') as json_data:
            level = json.load(json_data)

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
                    errcnt += 1

            if errcnt > (.2 * goodcnt):
                print("Error reading song: ", json_path)
                return False

            return onset_map
    except Exception as e:
        print(e)
        return np.zeros(0)
