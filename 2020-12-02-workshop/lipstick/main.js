
// Initializing wappsto
const Wappsto = require('wapp-api');
let wappsto = new Wappsto();

// Enable printing log to the browser's console
let wappstoConsole = require("wapp-api/console");
wappstoConsole.start();
console.log("Hello, Wapp!!");

// Temperature threshold for closing relay
const TEMP_THRESHOLD = 25;

// Fetch and define control state
let relayControlState;
wappsto.get("device", { "name": "Relay" }, {
    "quantity": "1",
    "expand": 5,
    "success": (collection) => {
        relay = collection.last();
        relayControlState = relay.get("value").findWhere({ name: "On-off" }).get("state").findWhere({ type: "Control" });
        console.log(collection);
    }
});

// Define function for updating relay control state
function saveControlValue(theValue) {
    if (relayControlState) {
        relayControlState.save({ data: theValue }, { patch: true });
    }
}

// Fetch and define temperature report state and
// assign callback function on temperature change stream events
wappsto.get("device", { "name": "Barometer" }, {
    "quantity": "1",
    "expand": 5,
    "subscribe": true,
    "success": (collection, response) => {
        temperature = collection.last();
        const temperatureReportState = temperature.get("value").findWhere({ name: "Temperature" }).get("state").findWhere({ type: "Report" });
        temperatureReportState.on('change:data', () => {
            console.log('New stream event arrived');
            const temperatureState = temperatureReportState.get('data')
            console.log(temperatureState);
            console.log("Checking temp");
            if (parseFloat(temperatureState) > TEMP_THRESHOLD) {
                console.log("High temp closing relay.");
                saveControlValue("1");
            } else {
                console.log("Low temp opening relay.");
                saveControlValue("0");
            }
        });
    }
});
