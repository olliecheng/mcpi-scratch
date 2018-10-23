from __future__ import print_function

import json
import sys
from mcpi import minecraft
from flask import Flask, request
app = Flask(__name__)


#suppress some really annoying logs
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)



MCPI_FUNCTIONS = [
    "getBlock", "setBlock", "standingOnBlock", "postToChat", "setPos", "postToChat"
	"playerForward", "playerBackward", "playerLeft", "playerRight",
	"getPosX", "getPosY", "getPosZ"
]  # name of functions which will be sent thru POST


class ConversionFunctions:
	"A holder for all our wrapper functions. All staticmethods so we don't have to initalize ConversionFunctions."
	# note that the Coord is just an object of Any which can be safely converted to a float
	#   (such as "1", int(1), float(1), 1.0)

	@staticmethod
	def postToChat(message):
		# type: str -> None
		"Posts a message to chat."

		mc.postToChat(message)

	@staticmethod
	def getBlock(x, y, z):
		# type: Coord, Coord, Coord -> string
		"Gets the block at coords (x, y, z)."

		blockID = mc.getBlock(float(x), float(y), float(z))
		for k in BLOCK_IDS:
			if BLOCK_IDS[k] == blockID:
				return k
		return "error" # default... dunno what to do. shouldn't ever get here tho

	@staticmethod
	def setBlock(x, y, z, blockType):
		# type: Coord, Coord, Coord, string -> None
		"Sets the block at coords (x, y, z) to type (belonging to BLOCK_IDS.keys())."

		mc.setBlock(float(x), float(y), float(z), BLOCK_IDS[blockType])

	@staticmethod
	def standingOnBlock():
		# type: None -> string
		"Returns the block type (belonging to BLOCK_IDS.keys()) of the block the player is standing on."

		position = mc.player.getTilePos()  # getTilePos returns the position of the block your legs are in
		position.y -= 1  				   # to see the tile we're standing on, move y down by one
		blockID = mc.getBlock(* position)
		for k in BLOCK_IDS:
			if BLOCK_IDS[k] == blockID:
				return k
		return "error" # default... dunno what to do. shouldn't ever get here tho

	@staticmethod
	def setPos(x, y, z):
		# type: Coord, Coord, Coord -> None
		"Sets the position of the player to (x, y, z)."

		mc.player.setPos(float(x), float(y), float(z))

	@staticmethod
	def movePlayer(direction, amount):
		# type: string \in ["forward", "backward", "right", "left"], int -> None
		"Moves the player in a certain direction (along the 2D xz plane) a scalar amount."

		position = mc.player.getPos()
		if direction == "forward": position.x += amount
		elif direction == "backward": position.x -= amount
		elif direction == "right": position.z += amount
		elif direction == "left": position.z -= amount

		mc.player.setPos(*position)

	@staticmethod
	def getPosition(axis):
		# type: string \in ["x", "y", "z"] -> int
		"Gets the amount the player has moved along that axis. Equivalent to <player position>.<axis>."

		position = mc.player.getPos()
		return int(eval("position." + axis))  # only one character, so fairly safe; vec3 doesn't implement __getitem__




@app.route("/command", methods=["POST"])
def processCommand():
	"""This is the entry for the API.

	Sample usage with Ajax:
	$.ajax({
        type: "POST",
        url: "http://127.0.0.1:9095/command",
        data: <JSON string>,
    });

	Return type varies depending on type of data. Empty string if non-reporter function, else value.
	Note that for Bools, the return type is "True" and "False" instead of "true" and "false" (as used by JS and like).
	"""

	data = json.loads(request.form.to_dict().keys()[0])
	function = data["function"]

	try:
		args = [str(x) for x in data["args"]]
	except UnicodeEncodeError:
		print("Currently, MCPi has a bug in where Unicode strings " + \
			  "(such as an accented letter) are not supported.")
		return
		# MCPi bug - passing through a unicode string will cause a recursion error.

	if function not in MCPI_FUNCTIONS:
		print("Function %s nonexistent." % function)
		return "Function doesn't exist.", 404

	if function.startswith("player"):
		ret = ConversionFunctions.movePlayer(function[6:].lower(), args[0])
	elif function.startswith("getPos"):
		ret = ConversionFunctions.getPosition(function[-1].lower())
	else:
		ret = getattr(ConversionFunctions, function)(*args)

	# ret should be empty/null if the calling function is not a reporter! else String
	ret = str(ret)
	return ret, 200

@app.route('/')
def hello():
    return "<h1>Hello World! This is confirmation that your MCPi Scratch server is running.</h1>"

def startupBanner():
	msg = """
***********************************
        MCPi-Scratch Server
***********************************

Hello! This is a Flask web app which exposes control to Minecraft: Pi Edition (or RaspberryJuice).
It's meant for use with the MCPi-Scratch extension (which will send requests to this web app through Ajax).
You can get that extension here: https://github.denosawr/MCPi-Scratch.

Extension hanging or not working? There may be some pearls of wisdom in the stdout here.

Connecting to Minecraft: Pi Edition (make sure it's up and running)... """
	print(msg, end="")

BLOCK_IDS = {  # from https://www.stuffaboutcode.com/p/minecraft-api-reference.html
	"air": 0, "stone": 1, "grass": 2, "dirt": 3, "cobblestone": 4, "wood_planks": 5, "sapling": 6, "bedrock": 7, "water": 8, "lava": 10, "sand": 12, "gravel": 13, "gold_ore": 14, "iron_ore": 15, "coal_ore": 16, "wood": 17, "leaves": 18, "glass": 20, "lapis_lazuli_ore": 21, "lapis_lazuli_block": 22, "sandstone": 24, "bed": 26, "cobweb": 30, "grass_tall": 31, "wool": 35, "flower_yellow": 37, "flower_cyan": 38, "mushroom_brown": 39, "mushroom_red": 40, "gold_block": 41, "iron_block": 42, "stone_slab_double": 43, "stone_slab": 44, "brick_block": 45, "tnt": 46, "bookshelf": 47, "moss_stone": 48, "obsidian": 49, "torch": 50, "fire": 51, "stairs_wood": 53, "chest": 54, "diamond_ore": 56, "diamond_block": 57, "crafting_table": 58, "farmland": 60, "furnace_inactive": 61, "furnace_active": 62, "door_wood": 64, "ladder": 65, "stairs_cobblestone": 67, "door_iron": 71, "redstone_ore": 73, "snow": 78, "ice": 79, "snow_block": 80, "cactus": 81, "clay": 82, "sugar_cane": 83, "fence": 85, "glowstone_block": 89, "bedrock_invisible": 95, "stone_brick": 98, "glass_pane": 102, "melon": 103, "fence_gate": 107, "glowing_obsidian": 246, "nether_reactor_core": 247,
}


if __name__ == '__main__':
	startupBanner()
	mc = minecraft.Minecraft.create()
	print("Done!\nStarting webserver on Port 9095. Ctrl+C to cancel, or you can just close this Terminal window.\n\n")
	app.run(port=9095)