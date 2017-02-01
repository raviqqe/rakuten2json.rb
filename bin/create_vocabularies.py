import argparse
import collections
import glob
import json
import multiprocessing
import os.path


def map_to_chunks(func, sequence):
    chunks = []

    num_cpus = multiprocessing.cpu_count()
    chunk_size = (len(sequence) + num_cpus - 1) // num_cpus

    for i in range(0, len(sequence), chunk_size):
        chunks.append(sequence[i:i + chunk_size])

    assert sum(len(chunk) for chunk in chunks) == len(sequence)

    return multiprocessing.Pool().map(func, chunks)


def gather_words(filenames):
    words = []

    for filename in filenames:
        with open(filename) as phile:
            for sentence in json.load(phile)['document']:
                words += sentence

    return collections.Counter(words), collections.Counter(''.join(words))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--min_freq', type=int, default=0)
    parser.add_argument('--word_file', default='words.txt')
    parser.add_argument('--char_file', default='chars.txt')
    parser.add_argument('dirnames', nargs='+')
    args = parser.parse_args()

    word_counter = collections.Counter()
    char_counter = collections.Counter()

    for dirname in args.dirnames:
        word_counters, char_counters = zip(*map_to_chunks(
            gather_words,
            glob.glob(os.path.join(dirname, '*'))))

        for counter in word_counters:
            word_counter += counter

        for counter in char_counters:
            char_counter += counter

    with open(args.word_file, 'w') as phile:
        for word, count in word_counter.most_common():
            if count < args.min_freq:
                break
            phile.write(word + '\n')

    with open(args.char_file, 'w') as phile:
        for char, count in char_counter.most_common():
            assert len(char) == 1
            if count < args.min_freq:
                break
            phile.write(char + '\n')


if __name__ == '__main__':
    main()
