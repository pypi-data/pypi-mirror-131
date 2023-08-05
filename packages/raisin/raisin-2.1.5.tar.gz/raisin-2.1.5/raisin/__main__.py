#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import raisin

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_module = subparsers.add_parser("install", help="install a module")
parser_module.add_argument("module", type=str, nargs="?", help="name of module")
parser_module.add_argument("-U", "--upgrade", action="store_true", default=False, help="force to upgrade")

parser_compress = subparsers.add_parser("compress", help="make an archive")
parser_compress.add_argument("source", nargs="?", help="file or directory")
parser_compress.add_argument("outfile", nargs="?", default=None, help="name of archive")
parser_compress.add_argument("-c", "--compresslevel", type=int, choices=[0,1,2,3], default=3, help="compression rate")
parser_compress.add_argument("-p", "-psw", "--psw", "--password", type=str, default=None, help="cifer the archive")
parser_compress.add_argument("-r", "--recursive", action="store_true", default=False, help="kip the tree and replace all file by an archive")

parser_decompress = subparsers.add_parser("decompress", help="exctract an archive")
parser_decompress.add_argument("infile", nargs="?", help="a .rais archive or a repertory")
parser_decompress.add_argument("-p", "-psw", "--psw", "--password", type=str, default=None, help="cifer the archive")

parser_work = subparsers.add_parser("run", help="try help another computer")
parser_work.add_argument("--cpu", default=None, help="maximum percentage of cpu taken by raisin")
parser_work.add_argument("--compresslevel", type=int, choices=[0,1,2,3], default=2, help="compression rate of result sending")
parser_work.add_argument("--dt", type=float, default=6, help="typical response time of the hash function")
parser_work.add_argument("--boss", type=bool, default=False, help="True for the control only")
parser_work.add_argument("--laborer", type=bool, default=False, help="True for execute work only")

args = parser.parse_args()
dico = args.__dict__

if ("module" in dico) and ("upgrade" in dico):
	raisin.install.install(args.module, upgrade=args.upgrade)

elif ("recursive" in dico) and ("psw" in dico) and ("outfile" in dico) and ("source" in dico) and ("compresslevel" in dico):
	if args.outfile == None:
		args.outfile = args.source.split("/")[0]+".rais"
	elif args.outfile[-5:] != ".rais":
		args.outfile = args.outfile+".rais"
	
	if not args.recursive:
		with open(args.outfile, "wb") as d:
			raisin.dump(args.source, d, compresslevel=args.compresslevel, psw=args.psw)
	else:
		principal_path = os.path.abspath(args.source)
		for father, dirs, files in os.walk(principal_path):
			os.chdir(father)
			for file in files:
				if file[-5:] != ".rais":
					with raisin.raisin.Printer("encapsulation of "+file+"..."):
						with open(file+".rais", "wb") as d:
							raisin.dump(file, d, compresslevel=args.compresslevel, psw=args.psw)
						os.remove(file)
			os.chdir(principal_path)

elif ("infile" in dico) and ("psw" in dico):
	if os.path.isfile(args.infile):
		with open(args.infile, "rb") as file:
			print(raisin.load(file, psw=args.psw, rep=os.getcwd()))
	else:
		principal_path = os.path.abspath(args.infile)
		for father, dirs, files in os.walk(principal_path):
			os.chdir(father)
			for file in files:
				if file[-5:] == ".rais":
					try:
						with raisin.raisin.Printer("desencapsulation of "+file+"..."):
							with open(file, "rb") as s:
									raisin.load(s, psw=args.psw, rep=os.getcwd())
					except:
						pass
					if os.path.exists(file[:-5]):
						os.remove(file)
			os.chdir(principal_path)

elif ("cpu" in dico) and ("compresslevel" in dico):
	if __name__ == '__main__':
		raisin.raisin.Worker(cpu=args.cpu, compresslevel=args.compresslevel, dt=args.dt, boss=args.boss, laborer=args.laborer)


