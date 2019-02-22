#!/usr/bin/env python3

import glob
import os
import sys
import pickle
import numpy as np

from common import audio_preprocessing as audioproc
from common import generate_labels as labelgen


class SoundFileMapPair:
    def __init__(self, audio_fpath, map_fpath, numbered_dir):
        self.audio_fpath = audio_fpath
        self.map_fpath = map_fpath
        self.numbered_dir = numbered_dir


def generate_data(search_path, output_path):

    hard_search = glob.glob(search_path + '/**/Hard.json', recursive=True)

    map_sound_pairs = []
    for hard_json_file in hard_search:
        hard_dir = os.path.dirname(hard_json_file)
        numbered_dir = os.path.dirname(hard_dir)
        numbered_dir = numbered_dir[numbered_dir.rfind("/") + 1:]
        ogg_search = glob.glob(hard_dir + '/*.ogg')
        if len(ogg_search) == 1:
            map_sound_pairs.append(SoundFileMapPair(
                ogg_search[0], hard_json_file, numbered_dir))
        elif len(ogg_search) == 0:
            print('Directory', hard_dir,
                  'didn\'t contain any OGG files. Ignoring.', file=sys.stderr)
        else:
            print('Directory', hard_dir,
                  'contained more than one OGG file. Skipping.', file=sys.stderr)
    # print('File pairs:', map_sound_pairs)

    num_songs = 120
    cnt = 0
    data_list = []
    label_list = []
    for pair in map_sound_pairs:
        data = audioproc.preprocess_file(pair.audio_fpath, 46)
        label = labelgen.generate_onset_map(pair.map_fpath, pair.audio_fpath)

        if len(label) > 0:
            data_list.append(data)
            label_list.append(label)

            cnt += 1
            progress = '(' + str(cnt) + "/" + str(num_songs) + ")"
            print('Processed data for', pair.audio_fpath, progress)
            if cnt == num_songs:
                break
        else:
            print("error labeling data")

    # pickling!
    davids_special_pickle_jar = open(output_path, "wb")
    pickle.dump((data_list, label_list),
                davids_special_pickle_jar)
    davids_special_pickle_jar.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("use: main.py data_path output_file_path")
        sys.exit()

    search_path = sys.argv[1]
    output_path = sys.argv[2]
    generate_data(search_path, output_path)
