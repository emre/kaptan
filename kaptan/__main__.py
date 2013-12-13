import argparse
import os

from kaptan import HANDLER_EXT, Kaptan

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog=__package__,
        description='Configuration manager in your pocket')
    parser.add_argument('config_file', action='store',
                        help="file to load config from")
    parser.add_argument('--handler', action='store',
                        help="handler to use (default: guessed from filename)")
    parser.add_argument('-e', '--export', action='store', default='json',
                        help="format to export to")
    parser.add_argument('-k', '--key', action='store',
                        help="config key to get value of")
    args = parser.parse_args()
    handler = (
        args.handler or
        HANDLER_EXT.get(os.path.splitext(args.config_file)[1][1:], None)
    )
    if not handler:
        raise RuntimeError("Unable to determine handler")
    with open(args.config_file) as f:
        config = Kaptan(handler=handler)
        config.import_config(f.read())
    if args.key:
        print(config.get(args.key))
    else:
        print(config.export(args.export))
    parser.exit(0)

