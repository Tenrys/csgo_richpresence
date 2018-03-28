import sys
import rpc
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import os
import win32gui, win32con, win32process, psutil
import argparse
import sys



phases = {
	"freezetime": "freeze time",
	"live": "playing",
	"over": "round over"
}
modes = {
	"casual": "Casual",
	"competitive": "Competitive",
	"deathmatch": "Deathmatch"
}
client_id = "427969147985723403"

class CSGOGameStateServer(HTTPServer):
	def init_rpc(self):
		self.rpc = rpc.DiscordRPC(client_id)
		self.rpc.start()

	def __init__(self, *args, **kwargs):
		self.rpc = None
		while not self.rpc:
			try:
				self.init_rpc()
				print("RPC connection initialized.")
				break
			except:
				time.sleep(5)
				pass
		self.state = -1
		HTTPServer.__init__(self, *args, **kwargs)

	def service_actions(self):
		running = False
		for pid in psutil.pids():
			try:
				p = psutil.Process(pid)
				if p.name() == "csgo.exe":
					running = True
			except:
				pass
		if not running:
			print("csgo.exe not running, no need to keep going.")
			self.shutdown()

	def handle_json(self, data):
		game_state = json.loads(data)

		# print all available game state info available to use
		# print(json.dumps(game_state, sort_keys=True, indent=4, separators=(',', ': ')))

		activity = {}
		if "round" in game_state:
			if self.state != 1:
				self.state = 1 # playing
				self.time = time.time()

			# init vars
			round = game_state["round"]
			player = game_state["player"]
			match_stats = player["match_stats"]
			state = player["state"]
			map = game_state["map"]

			# round state info
			round_state = "State: " + str(map["team_ct"]["score"]) + " - " + str(map["team_t"]["score"]) + ", "
			round_state += phases[round["phase"]]
			if round["phase"] == "live" and "bomb" in round and round["bomb"] == "planted":
				round_state += ", bomb planted"

			# map / mode info
			map_text = map["name"] + " - " + modes[map["mode"]]

			# team / player state info
			team_text = ""
			if "team" in player:
				if player["team"] == "CT":
					team_text = "Counter-Terrorist"
				elif player["team"] == "T":
					team_text = "Terrorist"
			else:
				team_text = "Spectator" # never seen unless I add an icon
			team_text += " - " + str(state["health"]) + " HP, " + str(state["armor"]) + " Armor"

			# player stats info
			stats_text = str(match_stats["kills"]) + "|"
			stats_text += str(match_stats["assists"]) + "|"
			stats_text += str(match_stats["deaths"]) + " - "
			stats_text += str(match_stats["mvps"]) + " MVPs"
			stats_text += " - $" + str(state["money"])

			# compile activity dict
			activity = {
				"state": round_state,
				"details": stats_text,
				"timestamps": {
					"start": self.time
				},
				"assets": {
					"small_text": team_text,
					"large_text": map_text,
					"large_image": map["name"].lower()
				}
			}
			if "team" in player: # spectator, no icon
				activity["assets"]["small_image"] = player["team"].lower()

			# send activity
			self.rpc.send_rich_presence(activity)
		else:
			if self.state != 0:
				self.state = 0 # menu state
				self.time = time.time()

				activity = {
					"state": "In main menu",
					"timestamps": {
						"start": self.time
					},
					"assets": {
						"large_image": "main_menu"
					}
				}

				# nothing really happens in the menu, no need to update it all the time
				self.rpc.send_rich_presence(activity)

	def server_close(self, *args, **kwargs):
		if self.rpc:
			self.rpc.close()
		HTTPServer.server_close(self, *args, **kwargs)

class CSGOGameStateRequestHandler(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_POST(self):
		content_length = int(self.headers["Content-Length"])
		post_data = self.rfile.read(content_length).decode("utf-8")
		# print("POST request,\nPath: {}\nHeaders:\n{}\n\nBody:\n{}\n".format(str(self.path), str(self.headers), post_data))

		# we received game state data, process it
		self.server.handle_json(post_data)

		self._set_response()



os.system("title Discord Rich Presence: Counter-Strike: Global Offensive")

parser = argparse.ArgumentParser(prog="csgo_richpresence")
parser.add_argument("-S", "--silent", action="store_true", default=False, help="hide the console window entirely, leaving the program to run in the background")
parser.add_argument("-P", "--port", default=3000, help="pick what port to use for the http server")
args = parser.parse_args()

port = args.port
silent = args.silent

if silent:
	# this layer of fuckery should do
	our_pid = os.getpid()
	hide = {
		"cmd.exe": True,
		"conhost.exe": True,
		"python.exe": True,
	}
	hide[psutil.Process(our_pid).name().lower()] = True

	def enum_window_callback(hwnd, pid):
		try: # psutil is prone to error if you give it a pid for a process that doesn't exist
			p = psutil.Process(pid)
			if p and p.name().lower() in hide:
				_, window_pid = win32process.GetWindowThreadProcessId(hwnd)
				if pid == window_pid:
					print("Hid window of", p.name())
					win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
		except Exception as e:
			print("Failed to hide window:", str(e), pid)
			# print("Something could have gone wrong here while hiding the console, ignore this")
			# pass

	def hide_window(pid):
		win32gui.EnumWindows(enum_window_callback, pid)

	print("Trying to hide console window...")
	# process through all windows, compare their process' ID with ours and hide their windows if they match
	print("Try 1")
	hide_window(our_pid)

	# just in the case that it didn't actually hide it, try that with the parents
	# there might be a need to fuck with process children too but it works for now
	our_process = psutil.Process(our_pid)
	if our_process.parent():
		print("Try 2")
		hide_window(our_process.parent().pid)
		if our_process.parent().parent():
			print("Try 3")
			hide_window(our_process.parent().parent().pid) # fuck it, why not

server_address = ("127.0.0.1", port)
httpd = None
try:
	while True:
		print("Looking for csgo.exe...")
		found_csgo = False
		for pid in psutil.pids():
			try: # same as for enum_window_callback
				p = psutil.Process(pid)
				if p.name() == "csgo.exe":
					found_csgo = True
					break
			except:
				# print("Something could have gone wrong here while finding csgo.exe, ignore this")
				pass
		if found_csgo:
			print("Found csgo.exe, running server.")
			httpd = CSGOGameStateServer(server_address, CSGOGameStateRequestHandler)
			print("Starting httpd at {}:{}".format(server_address[0], port))
			httpd.serve_forever()
		time.sleep(30)
except KeyboardInterrupt:
	if httpd:
		print('Stopping httpd...')
		httpd.server_close()
	print("Exiting...")
	sys.exit()

# so many try statements in this script jesus fuck i don't know how to code

