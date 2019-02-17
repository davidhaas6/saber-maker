#!/usr/bin/env python3

import glob
import os
import sys

import audio_preprocessing as audioproc

class SoundFileMapPair:
    def __init__(self, audio_fpath, map_fpath):
        self.audio_fpath = audio_fpath
        self.map_fpath = map_fpath

if __name__ == "__main__":
    search_path = sys.argv[1]

    hard_search = glob.glob(search_path + '/**/Hard.json', recursive=True)
    print('Hard search:', hard_search)

    map_sound_pairs = []
    for hard_json_file in hard_search:
        hard_dir = os.path.dirname(hard_json_file)
        ogg_search = glob.glob(hard_dir + '/*.ogg')
        if len(ogg_search) == 1:
            map_sound_pairs.append(SoundFileMapPair(ogg_search[0], hard_json_file))
        elif len(ogg_search) == 0:
            print('Directory', hard_dir, 'didn\'t contain any OGG files. Ignoring.', file=sys.stderr)
        else:
            print('Directory', hard_dir, 'contained more than one OGG file. Skipping.', file=sys.stderr)
    print('File pairs:', map_sound_pairs)

    for pair in map_sound_pairs:
        print('Processed data for', pair.audio_fpath, ':')
        print(audioproc.preprocess_file(pair.audio_fpath, 46))
