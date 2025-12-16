#!/usr/bin/env python
import sys
#import argparse
from camek.camek import main
#from camek.exceptions import CamekError as CamekError

# def parse_args() -> argparse.Namespace:

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         '-a', '--audio-processor',
#         help='Audio processor configuration file.',
#         dest='aproc_conf',
#         required=True,
#         default=None,
#         action='store',
# 	)

#     parser.add_argument(
#         '-i', '--input-source',
#         help='Input source configuration file.',
#         dest='isrc_conf',
#         required=True,
#         default=None,
#         action='store',
# 	)
#     parser.add_argument(
#         '-o', '--output-sink',
#         help='Output sink configuration file.',
#         dest='osnk_conf',
#         required=True,
#         default=None,
#         action='store',
# 	)
#     parser.add_argument(
# 			'-v', '--verbosity-level',
# 			help='Verbosity level.',
# 			dest='verbosity_level',
#             required=False,
# 			action='store',
#             default='info',
#             choices=['debug','info','warning','error','critical'],
# 	)
#
#    return parser.parse_args()

def run() -> int:
    # args = parse_args()
    

    main()
    # try:
    #     main(
    #         aproc_conf=args.aproc_conf,
    #         isrc_conf=args.isrc_conf,
    #         osnk_conf=args.osnk_conf,
    #         verbosity_level=args.verbosity_level,
    #         )
    # except CamekError as e:
    #     return 1
    # return 0

    return 0

if __name__ == "__main__":
    sys.exit(app())
