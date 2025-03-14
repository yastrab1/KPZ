import segno
import argparse

args_parse = argparse.ArgumentParser()
args_parse.add_argument("-d","--data", type=str)
args_parse.add_argument("-o", "--output", type=str)

args = args_parse.parse_args()
segno.make_qr(args.data).save(args.output)