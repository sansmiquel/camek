#!/usr/bin/env python
import sys
import argparse
from camek.camek import main
from camek.exceptions import CamekError as CamekError

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-t', '--top-config',
        help='Top-level processing module configuration file.',
        dest='topl_conf',
        required=True,
        default=None,
        action='store',
	)

    parser.add_argument(
        '-i', '--in-config',
        help='Input source module configuration file.',
        dest='isrc_conf',
        required=True,
        default=None,
        action='store',
	)
    parser.add_argument(
        '-o', '--out-config',
        help='Output sink module configuration file.',
        dest='osnk_conf',
        required=True,
        default=None,
        action='store',
	)

    parser.add_argument(
        '-I', '--in-type',
        help='Input source type.',
        dest='in_type',
        required=False,
        default='file',
        choices=['file','chunkedfile','device'],
        action='store',
	)

    parser.add_argument(
        '-O', '--out-type',
        help='Output source type.',
        dest='out_type',
        required=False,
        default='file',
        choices=['file','chunkedfile','device'],
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

    parser.add_argument(
        "top_module",
        help=f"Top level processing module.",
        action="store",
        nargs=1,
        type=str,
        metavar="TOPMODULE")
    
    return parser.parse_args()

def run() -> int:
    """Main entry point for camek CLI application."""
    args = parse_args()

    try:
        main(
            top_module=args.top_module[0],
            topl_conf=args.topl_conf,
            isrc_conf=args.isrc_conf,
            osnk_conf=args.osnk_conf,
            out_type=args.out_type,
            in_type=args.in_type,
            verbosity_level_console=args.verbosity_level_console,
            verbosity_level_file=args.verbosity_level_file,
            )
    except CamekError as e:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(run())
