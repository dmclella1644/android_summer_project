import argparse
import re
import subprocess
import sys

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filename', help='input logcat filename to be searched')
	parser.add_argument('-s', '--serial', help='device serial number for adb access')
	parser.add_argument('-r', '--regex', required=True, help='search term to be searched')
	parser.add_argument('-i', action='store_true', help='boolean for case insensitive')
	parser.add_argument('-a', action='store_true', help='boolean for all of the line')
	# parser.print_help()
	args = parser.parse_args()
	ln = 0
	if args.filename:
		with open(args.filename,'r') as file:
			for line in file:
				ln += 1
				if args.i:
					p = re.compile(".*"+args.regex+".*", re.IGNORECASE)
				else:
					p = re.compile(args.regex)
				m = p.match(line)
				if m:
					if args.a:
						print(str(ln) + " " + line)
					else:
						part = re.split("\s+[DEIVW]\s+", line)
						if len(part) >= 2:
							print(str(ln) + " " + part[1])
						else:
							print(str(ln) + " " + part[0])
				else:
					continue
	else:
		if args.serial:
			try:
				# after the decode stage of the subprocess, the return value is an array
				# with each element containing one character. So, we need to have an array
				# with words and not characters in the array. So, we join everything together
				# by "" and then split it on the newline, since the code afterwards interprets
				# lines easily. It is possibly to do this with characters, but takes more time
				# since we cannot easily use re.
				result = subprocess.run(["adb", "-s", str(args.serial), "shell", "logcat", "-v", "threadtime", "-d"], stdout = subprocess.PIPE)
				splits = result.stdout.decode("utf-8", errors='ignore')
				# print(result)
				all = "".join(splits)
				input = re.split("\n", all)
				for line in result:
					# print(line)
					# line = line.rstrip()
					ln += 1
					if args.i:
						p = re.compile(".*"+args.regex+".*", re.IGNORECASE)
					else:
						p = re.compile(args.regex)
					m = p.match(line)
					if m:
						if args.a:
							print(str(ln) + " " + line)
						else:
							part = re.split("\s+[DEIVW]\s+", line)
							if len(part) >= 2:
								print(str(ln) + " " + part[1])
							else:
								print(str(ln) + " " + part[0])
					else:
						continue
			except FileNotFoundError as err:
				print("FileNotFoundError: " + str(err))
				print('If you do not have a path to the shell command "adb",')
				print('possibly try adding a path to your adb.exe file PATH=$PATH:<adb path>')
				sys.exit(1)
			except Exception as err:
				print(err)
				sys.exit(1)
		else:
			try:
				# after the decode stage of the subprocess, the return value is an array
				# with each element containing one character. So, we need to have an array
				# with words and not characters in the array. So, we join everything together
				# by "" and then split it on the newline, since the code afterwards interprets
				# lines easily. It is possibly to do this with characters, but takes more time
				# since we cannot easily use re.
				result = subprocess.run(["adb", "shell", "logcat", "-v", "threadtime", "-d"], stdout = subprocess.PIPE)
				splits = result.stdout.decode("utf-8", errors='ignore')
				# print(result)
				all = "".join(splits)
				input = re.split("\n", all)
				for line in input:
					# line = line.rstrip()
					# print(line)
					ln += 1
					if args.i:
						p = re.compile(".*"+args.regex+".*", re.IGNORECASE)
					else:
						p = re.compile(args.regex)
					m = p.match(line)
					if m:
						if args.a:
							print(str(ln) + " " + line)
						else:
							part = re.split("\s+[DEIVW]\s+", line)
							if len(part) >= 2:
								print(str(ln) + " " + part[1])
							else:
								print(str(ln) + " " + part[0])
				else:
					continue
			except FileNotFoundError as err:
				print("FileNotFoundError: " + str(err))
				print('If you do not have a path to the shell command "adb",')
				print('possibly try adding a path to your adb.exe file: PATH=$PATH:<adb path>')
				sys.exit(1)
			except Exception as err:
				print(err)
				sys.exit(1)