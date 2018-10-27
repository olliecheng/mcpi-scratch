// Here are the different functions which can be passed through to the Python script.
//


// These are all the functions available from Scratch. Note that all of them run 'async' - that is, have a callback.
var MCPI_FUNCTIONS_ASYNC = [
    "getBlock", "setBlock", "postToChat", "setPos", "standingOnBlock",
    "playerForward", "playerBackward", "playerLeft", "playerRight",
    "playerUp", "playerDown", "getPosX", "getPosY", "getPosZ"
] // note that this _can_ be const, but that means that removing and re-adding the plugin may cause issues

// declare a global callback which will be updated and called
var global_callback;


(function(ext) {
    //  init some variables
    ext.running = true;
    ext.reader = new FileReader();



    // cleanup function when the extension is unloaded
    ext._shutdown = function() {
        ext.running = false;  // so connectTimeoutLoop can harmessly stop
    };

    // change the status
    ext._getStatus = function() {
        if (window.socket.readyState == window.socket.OPEN) {  // ws connected
            return {status: 2, msg: "Ready!"}
        } else {  // ws not connected/connecting; connecting should be practically instantaneous
            return {status: 1, msg: "Server not running."}
        }
    };



    // connect to WebSocket
    function connect() {
        if (window.socket.readyState != window.socket.OPEN) {
            window.socket.close();
            window.socket = new WebSocket("ws://127.0.0.1:9095");
            window.socket.onmessage = socketOnMessage;
        }
    }

    // calls connect() periodically to allow auto-connect
    function connectTimeoutLoop() {
        if (!ext.running) {
            // if the plugin has been removed, stop connecting to ws
            return;
        }

        connect();
        setTimeout(connectTimeoutLoop, 3000); // every 3 seconds, connect if not connected already
    }



    // Message recieve actions
    ext.reader.addEventListener('loadend', (e) => {
        // reader.readAsText(data) will call this function
        const msg = e.srcElement.result;

        global_callback(msg);
        global_callback = undefined;
        return;
      });

    function socketOnMessage (message) {
        // function to be called when ws recieves data
        ext.reader.readAsText(message.data);
    };



    // create WebSocket. note we can't call connect() because right now window.socket == undefined.
    window.socket = new WebSocket("ws://127.0.0.1:9095");
    window.socket.onmessage = socketOnMessage;
    connectTimeoutLoop();



    // function to call to send data to server
    function sendToServer(functionName, args) {
        var msg = JSON.stringify({
            "function": functionName,
            "args": args
        });
        if (window.socket.readyState != window.socket.OPEN) {
            // not connected to server :(
            // immediately call global_callback and quit
            if (global_callback) {
                global_callback();
                global_callback = undefined;
            }
            return;
        }
        window.socket.send(msg);  // send payload
    }



    // create a wrapper function around sendToServer which updates global_callback
    // this is being done in case non-async functions are ever used, which don't have a callback
    // the callback function should be passed _last_
    function createSendToServerFunctionWithCallback(functionName) {
        return function(a,b,c,d,e) {
            var targs = [a, b, c, d, e].filter(function(n) {return n}),  // [1,2,3,undefined,undefined] -> [1,2,3]
                args = targs.splice(0, targs.length - 1),                // [1,2,3] -> [1,2]
                callback = targs.splice(-1)[0];                          // [1,2,3] -> [3]
            global_callback = callback;
            sendToServer(functionName, args);
        }
    }

    // Now, we create a property of ext for each of MCPI_FUNCTIONS
    for (var i=0; i<MCPI_FUNCTIONS_ASYNC.length; i++) {
        // for each MCPI_FUNCTION wrap it around sendToServer
        ext[MCPI_FUNCTIONS_ASYNC[i]] = createSendToServerFunctionWithCallback(MCPI_FUNCTIONS_ASYNC[i]);
    }



    // Scratch stuff - specify blocks and menus to be used by the extension
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
            ["w", "fly up %n blocks", "playerUp", "1"],
            ["w", "fly down %n blocks", "playerDown", "1"],
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

