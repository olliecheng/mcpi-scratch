// Here are the different functions which can be passed through to the Python script.
//


const MCPI_FUNCTIONS_ASYNC = [
    "getBlock", "setBlock", "postToChat", "setPos", "standingOnBlock",
    "playerForward", "playerBackward", "playerLeft", "playerRight",
    "getPosX", "getPosY", "getPosZ"
]

var global_callback;


(function(ext) {
    ext.running = true;
    function connect() {
        if (window.socket.readyState != window.socket.OPEN) {
            window.socket.close();
            window.socket = new WebSocket("ws://127.0.0.1:9095");
            window.socket.onMessage = socketOnMessage;
        }
    }

    function connectTimeoutLoop() {
        if (!ext.running) {
            return;
        }
        connect();
        setTimeout(connectTimeoutLoop, 3000); // every second, connect if not connected already
    }
    
    function socketOnMessage (message) {
        var msg = JSON.parse(message.data);
        console.log(msg)
    };

    window.socket = new WebSocket("ws://127.0.0.1:9095");
    window.socket.onMessage = socketOnMessage;
    connectTimeoutLoop();

    function sendToServer(functionName, args) {
        var msg = JSON.stringify({
            "function": functionName,
            "args": args
        });
        if (window.socket.readyState != window.socket.OPEN) {
            // not connected to server :(
            
            if (global_callback) {
                global_callback();
                global_callback = undefined;
            }
            
            return;
        }
        window.socket.send(msg);
        /*$.ajax({
            type: "POST",
            url: "http://127.0.0.1:9095/command",
            data: msg,
            failure: function(data) {
                if (global_callback) {
                    global_callback();
                    global_callback = undefined;
                }
            },
            success: function(data) {
                console.log("success");
                if (global_callback) {
                    global_callback(data);
                    global_callback = undefined;
                }
            }
        });*/
    }

    function createSendToServerFunctionWithCallback(functionName) {
        return function(a,b,c,d,e) {
            var targs = [a, b, c, d, e].filter(function(n) {return n}),
                args = targs.splice(0, targs.length - 1),
                callback = targs.splice(-1)[0];
            global_callback = callback;
            sendToServer(functionName, args);
        }
    }


    // Cleanup function when the extension is unloaded
    ext._shutdown = function() {
        ext.running = false;
    };

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function() {
        if (window.socket.readyState == window.socket.OPEN) {
            return {status: 2, msg: "Ready!"}
        } else {
            return {status: 1, msg: "Server not running."}
        }
        // return {status: 2, msg: 'Ready'};
    };

    // Now, we create a property of ext for each of MCPI_FUNCTIONS
    for (var i=0; i<MCPI_FUNCTIONS_ASYNC.length; i++) {
        ext[MCPI_FUNCTIONS_ASYNC[i]] = createSendToServerFunctionWithCallback(MCPI_FUNCTIONS_ASYNC[i]);
    }

    // Block and block menu descriptions
    var descriptor = {
        blocks: [
            ["R", "get block at ( %n, %n, %n )", "getBlock", "0", "0", "0"],
            ["w", "set block at ( %n, %n, %n ) to %m.blockTypes", "setBlock", "0", "0", "0", "dirt"],
            ["R", "stood on block", "standingOnBlock"],
            ["w", "post %s to chat", "postToChat", "hello world!"],
            ["w", "set player position to ( %n, %n, %n )", "setPos", "0", "0", "0"],
            ["w", "forward %n blocks", "playerForward", "1"],
            ["w", "left %n blocks", "playerLeft", "1"],
            ["w", "backwards %n blocks", "playerBackward", "1"],
            ["w", "right %n blocks", "playerRight", "1"],
            ["R", "player x", "getPosX"],
            ["R", "player y", "getPosY"],
            ["R", "player z", "getPosZ"]
        ],
        menus: {
            blockTypes: [
                "air", "stone", "grass", "dirt", "cobblestone", "wood_planks", "sapling", "bedrock",
                "water", "lava", "sand", "gravel", "gold_ore", "iron_ore", "coal_ore", "wood", "leaves", "glass",
                "lapis_lazuli_ore", "lapis_lazuli_block", "sandstone", "bed", "cobweb", "grass_tall", "wool",
                "flower_yellow", "flower_cyan", "mushroom_brown", "mushroom_red", "gold_block", "iron_block",
                "stone_slab_double", "stone_slab", "brick_block", "tnt", "bookshelf", "moss_stone", "obsidian",
                "torch", "fire", "stairs_wood", "chest", "diamond_ore", "diamond_block", "crafting_table",
                "farmland", "furnace_inactive", "furnace_active", "door_wood", "ladder", "stairs_cobblestone",
                "door_iron", "redstone_ore", "snow", "ice", "snow_block", "cactus", "clay", "sugar_cane",
                "fence", "glowstone_block", "bedrock_invisible", "stone_brick", "glass_pane", "melon",
                "fence_gate", "glowing_obsidian", "nether_reactor_core"
            ]
        }
    };


    // Register the extension
    ScratchExtensions.register('MCPi Scratch', descriptor, ext);
})({});

