from __future__ import print_function

import json
import sys
from mcpi import minecraft
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

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


class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        print(self.data, type(self.data))
        data = json.loads(self.data)
        function = data["function"]
        print(data, function)

        # python 2 unicode bug - Python3 should fix it
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
        self.sendMessage(ret)
        print("Return message sent.")


    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


if __name__ == "__main__":
    # mc = minecraft.Minecraft.create()
    mc = minecraft()
    server = SimpleWebSocketServer('', 9095, SimpleEcho)
    server.serveforever()