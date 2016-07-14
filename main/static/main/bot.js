var graphHeight = 350;
var graphWidth = 600;

var entityType = "bot";

function init() {
	//loadRecentTrades();
    updatePairDisplays("trading_pair");
    checkBitstampClientID();
    loadToggleButton();
}

function saveClicked() {
	$(".save").html("Saving...");
	setTimeout(function() {
		saveUserSettings(function(result) {
			if(result["success"] == 1) {
				$(".save").html("Saved");
                makeGraph();
			}
			else {
				$(".save").html("Save Failed");
			}
			setTimeout(function() {
				$(".save").html("Save Settings");
			}, 2000);
		});
	}, 500);
}

function checkBitstampClientID() {
	var row = document.getElementById("ClientIDRow");
	var exchange = document.getElementById("exchange");
	
	
	if(exchange.children[exchange.selectedIndex].value == "bitstamp") {
		row.style.display = "";
	}
	else {
		row.style.display = "none";
	}
}

function loadStrategies(callback) {
	apiCall("listStrategies", null, function(result) {
		var options = "";
		for(var i in result["Strategies"]) {
			var stratName = result["Strategies"][i]["Name"];
			options += "<option value=\"" + i  + "\">" + stratName + "</option>";
		}
		var strategies = document.getElementById("StrategyID");
		strategies.innerHTML = options;
		
		callback();
	});
}

function loadRecentTrades() {
	var params = {"days":30, "BotID":pageItem};
	apiCall("getRecentTrades", params, function(result) {
			if(result && result["Success"] == 1 && result["Trades"].length > 0) {
				var text = "";
				var header = "<tr><th>#</th><th>Time</th><th>Type</th><th>Amount</th><th>Price</th></tr>";
				/*if(exchange == "bitmex") {
					header = "<tr><th>#</th><th>Time</th><th>Type</th><th>Price</th></tr>";
				}*/
				
				for(var i in result["Trades"]) {
					var row = "<tr>";
					var trade = result["Trades"][i];
					row += "<td>" + (parseInt(i) + 1) + "</td>";
					row += "<td>" + trade["DateString"] + "</td>";
					row += "<td>" + trade["Type"] + "</td>";
					//if(exchange != "bitmex") {
						row += "<td>" + trade["Amount"] + "</td>";
					//}
					row += "<td>" + trade["Price"] + "</td>";
					row += "</tr>";
					text = text + row;
				}
	
				document.getElementById("recentTrades").innerHTML = header + text;
				if(result["Profit"]) {
					document.getElementById("recentTradesProfit").innerHTML = 
						"(Estimated) <span class=\"primary\"></span> Profit: <strong>" + (result["Profit"]["Primary"]).toFixed(2) + "</strong>%<br>" +
						"(Estimated) <span class=\"secondary\"></span> Profit: <strong>" + (result["Profit"]["Secondary"]).toFixed(2) + "</strong>%";
				}
				document.getElementById("recentTradesWrapper").style.display = "";
			}
	});
}

function updateSaveButton() {
	document.getElementById("Save").style.display = "";
}

function toggleBot() {
	var toggle = document.getElementById("Toggle");
	var status = toggle.innerHTML;
	toggle.innerHTML = "Toggling...";
    
    var currentValue = $("#enabled").val();
    if(currentValue == "true") {
        $("#enabled").val("false");
    }
    else {
        $("#enabled").val("true");
    }
	
    saveUserSettings(function(result) {
        if(result["success"] && result["success"] == true) {
			setToggleButton(status);
		}
	});
}


document.addEventListener('DOMContentLoaded', function() {
	setTimeout(function() {
		init();
	}, 50);
});

document.querySelector('#Save').addEventListener('click', saveClicked);

document.querySelector('#exchange').addEventListener('change', function() {
	checkBitstampClientID();
	loadTradingPairs("exchange", "TradingPair", null);
});

document.querySelector('#trading_pair').addEventListener('change', function() {
	updatePairDisplays("trading_pair");
});

document.querySelector('#Toggle').addEventListener('click', function() {
	toggleBot();
});