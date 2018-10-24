from __future__ import print_function
import json
import sys

print("Updating extensions.json to include custom plugin...")

with open("/usr/lib/scratch2/scratch_extensions/extensions.json") as extensionsFile:
    extensions = json.loads(extensionsFile.read())

for e in extensions:
    if e["name"] == "MCPi-Scratch":
        # already exists!
        print("Entry already exists in /usr/lib/scratch2/scratch_extensions/extensions.json. If you're upgrading from an existing install, this is fine!")
        sys.exit(0)

extensions.append({
    "name": "MCPi-Scratch",
    "type": "extensions",
    "file": "mcpi-scratch.js",
    "url" : "https://denosawr.github.io/mcpi-scratch/",
    "tags": [],
    "md5" : "mcpi-scratch.png"
    })

with open("/usr/lib/scratch2/scratch_extensions/extensions.json", "w") as extensionsFile:
    extensionsFile.write(json.dumps(extensions))

print("Updated /usr/lib/scratch2/scratch_extensions/extensions.json to include custom plugin!")


