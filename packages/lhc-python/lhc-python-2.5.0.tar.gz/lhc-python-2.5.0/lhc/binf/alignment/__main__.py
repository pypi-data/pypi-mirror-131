import argparse

from .tools import call_variants, get_consensus, strand, mismatch_filter, trim_gaps


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    parser.set_defaults(func=lambda args: parser.print_usage())
    subparsers = parser.add_subparsers()

    call_variants_parser = subparsers.add_parser('call_variants')
    call_variants.define_parser(call_variants_parser)

    get_consensus_parser = subparsers.add_parser('get_consensus')
    get_consensus.define_parser(get_consensus_parser)

    strand_parser = subparsers.add_parser('strand')
    strand.define_parser(strand_parser)

    mismatch_filter_parser = subparsers.add_parser('mismatch_filter')
    mismatch_filter.define_parser(mismatch_filter_parser)

    trim_parser = subparsers.add_parser('trim_gaps')
    trim_gaps.define_parser(trim_parser)

    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
