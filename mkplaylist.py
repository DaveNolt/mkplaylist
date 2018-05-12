import os
import sys
import json
import errno
import argparse


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


parser = argparse.ArgumentParser(description='Make m3u playlist of mp3 files.')
parser.add_argument('path', type=str, default='.', nargs='?',
                    help='directory of playlist')
parser.add_argument('--recursive', action='store_true',
                    help='walk the path recursively')
parser.add_argument('--clean', action='store_true',
                    help='clean the directory from playlist files')

args = parser.parse_args()

walk_dir = args.path

# print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
# print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))
playlists = []

for root, subdirs, files in os.walk(walk_dir):
    # print('playlist_path = ' + playlist_path)
    if args.clean:
        # print('kek')
        for file in files:
            if file == 'mkplaylists.json':
                with open(os.path.join(root, file), 'r') as f:
                    for fdelp in json.load(f):
                        silentremove(os.path.normpath(fdelp))
                silentremove(file)

    elif any((os.path.splitext(f)[1] == '.mp3') for f in files) and not any((os.path.splitext(f)[1] == '.m3u') for f in files):
        print('--\nroot = ' + os.path.split(os.path.abspath(root))[1])
        playlist_path = os.path.join(
            root, '00. %s.m3u' % os.path.split(os.path.abspath(root))[1])
        playlists.append(os.path.abspath(playlist_path))
        with open(playlist_path, 'w') as playlist_file:
            for filename in files:
                if (os.path.splitext(filename)[1] == '.mp3'):
                    file_path = os.path.join(root, filename)
                    print('\t- file %s' % (filename))
                    playlist_file.write(filename + '\n')

    if not args.recursive:
        break

if len(playlists) > 0:
    with open(os.path.join(walk_dir, 'mkplaylists.json'), 'w') as f:
        json.dump(playlists, f, sort_keys=True, indent=4)
