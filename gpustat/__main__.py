from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

from gpustat import __version__
from .core import GPUStatCollection


def print_gpustat(json=False, debug=False, **args):
    '''
    Display the GPU query results into standard output.
    '''
    try:
        gpu_stats = GPUStatCollection.new_query()
    except Exception as e:
        sys.stderr.write('Error on querying NVIDIA devices.'
                         ' Use --debug flag for details\n')
        if debug:
            try:
                import traceback
                traceback.print_exc(file=sys.stderr)
            except Exception as e:
                # NVMLError can't be processed by traceback:
                #   https://bugs.python.org/issue28603
                # as a workaround, simply re-throw the exception
                raise e
        sys.exit(1)

    if json:
        gpu_stats.print_json(sys.stdout)
    else:
        gpu_stats.print_formatted(sys.stdout, **args)


def main(*argv):
    if not argv:
        argv = list(sys.argv)

    # attach SIGPIPE handler to properly handle broken pipe
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    # arguments to gpustat
    import argparse
    parser = argparse.ArgumentParser()

    parser_color = parser.add_mutually_exclusive_group()
    parser_color.add_argument('--force-color', '--color', action='store_true',
                              help='Force to output with colors')
    parser_color.add_argument('--no-color', action='store_true',
                              help='Suppress colored output')

    parser.add_argument('-c', '--show-cmd', action='store_true',
                        help='Display cmd name of running process')
    parser.add_argument('-u', '--show-user', action='store_true',
                        help='Display username of running process')
    parser.add_argument('-p', '--show-pid', action='store_true',
                        help='Display PID of running process')
    parser.add_argument('--json', action='store_true', default=False,
                        help='Print all the information in JSON format')
    parser.add_argument('-v', '--version', action='version',
                        version=('gpustat %s' % __version__))
    parser.add_argument(
        '-P', '--show-power', nargs='?', const='draw,limit',
        choices=['', 'draw', 'limit', 'draw,limit', 'limit,draw'],
        help='Show GPU power usage or draw (and/or limit)'
    )
    parser.add_argument(
        '--no-header', dest='show_header', action='store_false', default=True,
        help='Suppress header message'
    )
    parser.add_argument(
        '--gpuname-width', type=int, default=16,
        help='The minimum column width of GPU names, defaults to 16'
    )
    parser.add_argument(
        '--debug', action='store_true', default=False,
        help='Allow to print additional informations for debugging.'
    )
    args = parser.parse_args(argv[1:])

    print_gpustat(**vars(args))


if __name__ == '__main__':
    main(*sys.argv)
