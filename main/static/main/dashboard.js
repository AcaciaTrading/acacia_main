$(".delete-bot").click(function(e) {
    deleteItem("bot", e.currentTarget.getAttribute("data-id"));
});

$(".delete-strategy").click(function(e) {
    deleteItem("strategy", e.currentTarget.getAttribute("data-id"));
});

$("#newBot").click(function(e) {
    newItem("bot");
});

$("#newStrategy").click(function(e) {
    newItem("strategy");
});

function deleteItem(itemType, itemID) {
    if (confirm("Are you sure you want to delete this " + itemType + "?")) {
        apiCall(urls[itemType + "_delete"], {"id":itemID}, function(data) {
            if(data["success"]) {
                $("#panel-" + itemType + "-" + itemID).hide();
            }
        });
    }
}

function newItem(itemType) {
    var name = prompt("What should your new " + itemType + " be named?");
    console.log(name);
    if(name != null) {
        apiCall(urls[itemType + "_new"], {"name":name, "type":2}, function(data) {
            if(data["success"]) {
                window.location.href = urls[itemType + "_page"].replace("0", data["result"]);
            }
        });
    }
}

function apiCall(url, params, callback) {
    $.ajax({
        type: 'POST',
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