import subprocess
import platform
import os
import time as t
import socket
import json

def tail(fn):
	fp = open(fn, 'r')
	while True:
		new = fp.readline()
		if new:
			yield (new)
		else:
			t.sleep(0.5)

def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(("127.0.0.1", 65432))
		files = os.listdir()
		if platform.system() == 'Windows':
			subprocess.Popen(["qrt_data_extraction-Windows_x64.exe"])
		elif platform.system() == 'Darwin':
			subprocess.Popen(["./qrt_data_extraction.MacOS"])
		elif platform.system() == 'Linux':
			subprocess.Popen(["./qrt_data_extraction.Linux_x86_x64"])
		t.sleep(1)
		newfiles = os.listdir()
		for file in newfiles:
			if file not in files:
				filename = file
				break
		for line in tail(filename):
			try:
				date = line.split(" ")[0]
				time = line.split(" ")[1]
				type = line.split(" ")[2][:-1]
				message = ' '.join(line.split(" ")[3:])
			except IndexError:
				continue
			jsona = {
				"date": date,
				"time": time,
				"type": type,
				"message": message
			}
			s.sendall(json.dumps(jsona).encode('utf-8'))
			print(date, time, type, message)

if __name__ == "__main__":
	main()