import argparse
import io
import json
import os.path
import sys
import time
from datetime import datetime

from .downloader import YoutubeCommentDownloader, SORT_BY_RECENT


def main(argv = None):
    parser = argparse.ArgumentParser(add_help=False, description=('Download Youtube comments without using the Youtube API'))
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    parser.add_argument('--path_to_id', '-p', help='Path to csv with ID`s of Youtube videos for which to download the comments')
    parser.add_argument('--output', '-o', default='data/comments.json', help='Output filename (output format is line delimited JSON)')
    parser.add_argument('--limit', '-l', type=int, help='Limit the number of comments')
    parser.add_argument('--language', '-a', type=str, default=None, help='Language for Youtube generated text (e.g. en)')
    parser.add_argument('--sort', '-s', type=int, default=SORT_BY_RECENT,
                        help='Whether to download popular (0) or recent comments (1). Defaults to 1')
    
    args = parser.parse_args() if argv is None else parser.parse_args(argv)

    path_to_id = args.path_to_id
    output = args.output
    limit = args.limit

    ids = open(f"{path_to_id}", "r", encoding="utf-8")
    
    if os.path.isfile(output):
        output = 'data/comments_{}.json'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
        print('Such an output file already exists, entry in {}'.format(output))

    start_time_total = time.time()
    comments_total = 0
    for iter, youtube_id in enumerate(ids):

        try:
            
            if not youtube_id or not output:
                parser.print_usage()
                raise ValueError('you need to specify a Youtube ID/URL and an output filename')

            sys.stdout.write(f'Downloading Youtube comments for {youtube_id}')
            downloader = YoutubeCommentDownloader()
            generator = downloader.get_comments(youtube_id, args.sort, args.language)
            count = 0
            with io.open(output, 'a', encoding='utf8') as fp:
                sys.stdout.write('Downloaded %d comment(s)\r' % count)
                sys.stdout.flush()
                start_time = time.time()
                for comment in generator:
                    comment_json = json.dumps(comment, ensure_ascii=False)
                    print(comment_json.decode('utf-8') if isinstance(comment_json, bytes) else comment_json, file=fp)
                    count += 1
                    sys.stdout.write('Downloaded %d comment(s)\r' % count)
                    sys.stdout.flush()
                    if limit and count >= limit:
                        break
            comments_total += count
            print('\n[{:.2f} seconds] Video №{} Done!\n'.format(time.time() - start_time, iter+1))

        except Exception as e:
            print('Error:', str(e))
            sys.exit(1)
    print('\nTotal time [{:.2f} seconds]'.format(time.time() - start_time_total))
    print('Total downloaded comments: {}'.format(comments_total))
    print(f'File saved to {output}')