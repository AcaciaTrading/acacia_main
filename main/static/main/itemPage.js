function loadTradingPairs(idExchange, idTradingPair, callback) {
	var exchange = document.getElementById(idExchange);
	var exchangeValue = exchange.children[exchange.selectedIndex].value;
    
    var options = "";
    for(var i in tradingPairs[exchangeValue]) {
        var pair = tradingPairs[exchangeValue][i];
        options += "<option value=\"" + pair  + "\">" + pair + "</option>";
    }
    var tradingPair = document.getElementById(idTradingPair);
    tradingPair.innerHTML = options;

    if(callback == null) {
        updatePairDisplays(idTradingPair);
    }
    if(callback) {
        callback();
    }
}

function updatePairDisplays(idTradingPair) {
	var tradingPair = document.getElementById(idTradingPair);
	if(tradingPair.value == "") return;
	
	var pair = tradingPair.children[tradingPair.selectedIndex].value;
	
	var index = pair.indexOf("_");
	var primary = pair.substring(index + 1, pair.length).toUpperCase();
	var secondary = pair.substring(0, index).toUpperCase();
	
	var primaries = document.getElementsByClassName("primary");
	var secondaries = document.getElementsByClassName("secondary");
	for(var i = 0; i < primaries.length; i++) {
		primaries[i].innerHTML = primary;
		secondaries[i].innerHTML = secondary;
	}
}

function saveUserSettings(callback) {
    console.log("save!");
    var fieldsArray = $(":input").serializeArray();
    var fields = {};
    for(var i in fieldsArray) {
        var obj = fieldsArray[i];
        fields[obj.name] = obj.value;
    }
    if(entityType == "strategy") {
        if(fields["UsingAverage"] == "1") {
            var crossover = {"id":5};
            for(var name in fields) {
                if(name.substring(0, 3) == "ac-") {
                    crossover[name.substring(3)] = fields[name];
                }
            }
            fields["average_crossover"] = JSON.stringify(crossover);
        }
        else {
            fields["average_crossover"] = null;
        }

        fields["indicators"] = [];
        for(var i in indicators) {
            var indName = indicators[i];
            if(fields["Using" + indName] == "1") {
                var indicator = {"indicator_type":indName};
                for(var name in fields) {
                    if(name.substring(0, indName.length) == indName) {
                        indicator[name.substring(indName.length + 1)] = fields[name];
                    }
                }
                console.log(indicator);
                fields["indicators"].push(indicator);
            }
        }
        fields["indicators"] = JSON.stringify(fields["indicators"]);
    }
    
    fields["id"] = pageItem;
    
    console.log(fields);
    apiCall("POST", urls[entityType + "_detail"], fields, callback);
}

function apiCall(type, url, params, callback) {
    
    $.ajax({
        type: type,
        url: url,
        data: params,
        headers: {
            "Authorization":"Token " + token
        }
    }).always(function(data) {
        if(data["success"] != false && data["success"] != true) {
            data = data.responseJSON;
        }
        console.log(data);
        if(data["success"] == false) {
            alert(data["error"]);
        }
        callback(data);
    });
}


function time() {
	return Math.round(new Date().getTime() / 1000);
}

function loadToggleButton() {
	var toggle = document.getElementById("Toggle");
	//toggle.innerHTML = "Toggling...";
	
	var message = "";
	var prompt = "";
    if(itemRunning == true) {
        message += "Disable bot";
        prompt = 'Your bot is currently <span style="color: #5cb85c;">enabled</span>.';
    }
    else {
        message += "Enable bot";
        prompt = 'Your bot is currently <span style="color: #d9534f;">disabled</span>.';
    }

    toggle.style.display = "";
    toggle.innerHTML = message;

    document.getElementById("TogglePrompt").innerHTML = prompt;
}

function setToggleButton(status) {
	var toggle = document.getElementById("Toggle");
	
	var message = "";
	var prompt = "";
    if(status == "Enable bot") {
        message += "Disable bot";
        prompt = 'Your bot is currently <span style="color: #5cb85c;">enabled</span>.';
    }
    else {
        message += "Enable bot";
        prompt = 'Your bot is currently <span style="color: #d9534f;">disabled</span>.';
    }

    toggle.style.display = "";
    toggle.innerHTML = message;
    
    document.getElementById("TogglePrompt").innerHTML = prompt;
}

function eventFire(el, etype){
  if (el.fireEvent) {
    el.fireEvent('on' + etype);
  } else {
    var evObj = document.createEvent('Events');
    evObj.initEvent(etype, true, false);
    el.dispatchEvent(evObj);
  }
}

function setupOptionDisplays() {
	for(i in selectElements) {
		updateOptionDisplay(selectElements[i]);
	}
}

function updateOptionDisplay(id) {
	if(id.substring(0, 5) == "Using") {
		var input = document.getElementById(id);
		var table = document.getElementById(id + "Table");
		var display = "";
		
		if(input.value == "1") display = "";
		else display = "none";
		
		table.style.display = display;
	}
}

function message(message) {
	console.log(message);
}

$('[data-toggle="popover"]').popover({
    trigger: 'hover',
        'placement': 'top'
});

$('[data-toggle="popover"]').popover({
    trigger: 'click',
        'placement': 'top'
});