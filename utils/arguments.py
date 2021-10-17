import argparse


parser = argparse.ArgumentParser(description='Panopto Sync UniVR')


sub_parser = parser.add_subparsers(metavar='ACTION', dest='action', required=True)
sub_parser.add_parser('init', help='Create credential file')
sub_parser.add_parser('update', help='Update user\'s courses')
sync = sub_parser.add_parser('sync', help='Sync lessons')
# sub_parser.add_parser('clean', help='Clean lessons of deleted courses')

sync.add_argument(
    '--sync-dir',
    '-d',
    dest='sync_dir',
    metavar='path',
    default='./downloads',
    help='Downloaded video lessons folder'
)
sync.add_argument(
    '--format',
    '-f',
    dest='video_format',
    default='mp4',
    help='Video lessons\' format'
)
sync.add_argument(
    '--skip-download',
    '-s',
    dest='skip_download',
    action='store_true',
    help='Do not download video lessons'
)
sync.add_argument(
    '--no-repeat',
    '-o',
    dest='no_repeat',
    action='store_true',
    help='Sync repetitive'
)
sync.add_argument(
    '--every',
    '-e',
    dest='every',
    type=int,
    default=60,
    help='Sync every N minutes'
)
