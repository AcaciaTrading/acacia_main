var entityType = "strategy";

function init() {
    loadTradingPairs("BacktestExchange", "BacktestTradingPair", function() {
        setupOptionDisplays();
    });
    updateOptionDisplay("#UsingAverageTable");
}

function saveClicked() {
    $(".save").html("Saving...");
	
	var restoreButtons = function() {
		$(".save").html("Save Settings");
	};
	
	setTimeout(function() {
		saveUserSettings(function(result) {
			if(result["success"] == 1) {
				$(".save").html("Saved");
				setTimeout(function() {
					backtest(restoreButtons);
				}, 400);
			}
			else {
				$(".save").html("Save Failed");
				setTimeout(function() {
					restoreButtons();
				}, 2000);
			}
		});
	}, 500);
}

function backtest(callback) {
    
    var backtestCallback = function(callbackIn) {
		$(".save").html("Backtest done");
		setTimeout(function() {
			callbackIn();
		}, 1000);
	};
	
	$(".save").html("Backtesting...");
	
	document.getElementById("backtestResults").innerHTML = " ";
	document.getElementById("backtestProfit").innerHTML = " ";
	
	var params = {
        "strategy":pageItem,
        "exchange":$("#BacktestExchange").val(),
        "trading_pair":$("#BacktestTradingPair").val()
    };
	apiCall("POST", urls["backtest"], params, function(result) {
        if(result == null) {
            backtestCallback(callback);
            return;
        }
        console.log(result);
        result = result["result"];
        
        var text = "";
        var header = "<tr><th>#</th><th>Time</th><th>Type</th><th>Amount</th><th>Price</th></tr>";
        
        for(var i in result["trades"]) {
            var row = "<tr>";
            var trade = result["trades"][i];
            row += "<td>" + (parseInt(i) + 1) + "</td>";
            // FORMAT THIS TIMESTAMP
            row += "<td>" + trade["date"] + "</td>";
            row += "<td>" + trade["type"] + "</td>";
            row += "<td>" + trade["amount"] + "</td>";
            row += "<td>" + trade["price"] + "</td>";
            row += "</tr>";
            text = text + row;
        }
        
        if(text == "") {
            text = "No trades would have executed in the given timeframe.";
        }
        
        document.getElementById("backtestProfit").innerHTML =
            "Primary Profit After Fee: " + (result["profit_primary"] * 1) + "%<br>" + "Secondary Profit After Fee: " + (result["profit_secondary"] * 1) + "%";

        document.getElementById("backtestResults").innerHTML = header + text;
        document.getElementById("backtestResults").style.display = "";

        updatePairDisplays("BacktestTradingPair");
        backtestCallback(callback);
	});
}

function updateSaveButton() {
	document.getElementById("Save").style.display = "";
}


document.addEventListener('DOMContentLoaded', function() {
	setTimeout(function() {
		init();
	}, 50);
});

$(".save").click(saveClicked);

document.querySelector('#BacktestExchange').addEventListener('change', function() {
	loadTradingPairs("BacktestExchange", "BacktestTradingPair", null);
});

document.querySelector('#BacktestTradingPair').addEventListener('change', function() {
	updatePairDisplays("BacktestTradingPair");
});

document.addEventListener('change', function(e){
	updateOptionDisplay(e.target.id);
});