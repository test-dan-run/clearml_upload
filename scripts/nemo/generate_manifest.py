import os
import json
import librosa

### PARAMS ###

DATA_DIR = '/mnt/d/datasets/jtube/id/wav_16k/train'
OUTPUT_MANIFEST_PATH = '/mnt/d/datasets/jtube/id/wav_16k/train/train_manifest.json'

##############


def generate_manifest(data_dir: str, output_manifest_path: str = 'manifest.json') -> str:

    with open(output_manifest_path, mode='w', encoding='utf-8') as fw:
        for root, _, filenames in os.walk(data_dir):
            for filename in filenames:
                # only check wav files
                if not filename.endswith('.wav'):
                    continue
                filepath = os.path.join(root, filename)

                # assuming text file is just .txt of original audio path, 
                # and contains only 1 transcript
                textpath = filepath.replace('.wav', '.txt')
                with open(textpath, mode='r', encoding='utf-8') as f:
                    text = f.readlines()[0].strip('\r\n')

                relative_filepath = os.path.relpath(filepath, data_dir)

                # duration = 0.0
                duration = round(librosa.get_duration(filename=filepath), 2)

                item = {
                    'audio_filepath': relative_filepath,
                    'text': text,
                    'duration': duration,
                    # add other params of interest here
                }

                fw.write(
                    json.dumps(item) + '\n'
                )

    return output_manifest_path

if __name__ == '__main__':
    generate_manifest(DATA_DIR, OUTPUT_MANIFEST_PATH)
