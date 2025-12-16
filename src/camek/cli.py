#!/usr/bin/env python
import sys
import argparse
from camek.camek import main
from camek.exceptions import CamekError as CamekError

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--proc-config',
        help='Audio application engine processing configuration file.',
        dest='proc_conf',
        required=True,
        default=None,
        action='store',
	)

    parser.add_argument(
        '-i', '--in-config',
        help='Audio application engine input source configuration file.',
        dest='isrc_conf',
        required=True,
        default=None,
        action='store',
	)
    parser.add_argument(
        '-o', '--out-config',
        help='Audio application engine output sink configuration file.',
        dest='osnk_conf',
        required=True,
        default=None,
        action='store',
	)
    parser.add_argument(
			'-l', '--verbosity-file',
			help='File logging verbosity level.',
			dest='verbosity_level_file',
            required=False,
			action='store',
            default='info',
            choices=['debug','info','warning','error','critical'],
	)
    parser.add_argument(
			'-v', '--verbosity-console',
			help='Console logging verbosity level.',
			dest='verbosity_level_console',
            required=False,
			action='store',
            default='warning',
            choices=['debug','info','warning','error','critical'],
	)
    return parser.parse_args()

def run() -> int:
    """Main entry point for camek CLI application."""
    args = parse_args()

    try:
        main(
            proc_conf=args.proc_conf,
            isrc_conf=args.isrc_conf,
            osnk_conf=args.osnk_conf,
            verbosity_level_console=args.verbosity_level_console,
            verbosity_level_file=args.verbosity_level_file,
            )
    except CamekError as e:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(run())
