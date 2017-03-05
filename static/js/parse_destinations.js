$(document).ready(function() {
    
    startup();
    
    $("#match").click(function() {
        var loc = $("#location").text()
        var post_data = {"location": loc}
        $.ajax({
            url : "/matches",
            type: "POST",
            data : JSON.stringify(post_data),
            contentType: "application/json; charset=utf-8",
            success: function(data, textStatus, jqXHR) {
                // Do nothing
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Failed. " + textStatus + ": " + errorThrown)
            }
        });
        var patch_data = {
            "matched": "true",
            "seen": "true"
        }
        $.ajax({
            url : "/destinations/" + getCookie("position"),
            type: "POST",
            data : JSON.stringify(patch_data),
            contentType: "application/json; charset=utf-8",
            success: function(data, textStatus, jqXHR) {
                console.log("SUCCESS")
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Failed. " + textStatus + ": " + errorThrown)
            }
        });

        increment_position();
        get_destination();
    });
    
    $("#skip").click(function() {
        var send_data = {"seen": "true"}
        $.ajax({
            url : "/destinations/" + getCookie("position"),
            type: "POST",
            data : JSON.stringify(send_data),
            contentType: "application/json; charset=utf-8",
            success: function(data, textStatus, jqXHR) {
                console.log("SUCCESS")
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Failed. " + textStatus + ": " + errorThrown)
            }
        });
        increment_position();
        get_destination();
    });
    
});

function get_destination() {
    $.ajax({
        url : "/destinations",
        type: "GET",
        dataType: "json",
        success: function(data, textStatus, jqXHR) {
            var position = getCookie("position")
            if(typeof position != 'undefined') {
                var dest = data[position]
            } else {
                document.cookie = "position=0";
                var dest = data[0]
            }
            $("#location").text(dest["location"]);
            $("#dest-image").attr("src", dest["image"]);
            $("#description").attr("src", dest["description"]);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Failed. " + textStatus + ": " + errorThrown)
        }
    });
    
    if (typeof getCookie("data_length") == 'undefined') {
        document.cookie = "data_length=" + lines.length;
    }
}


function startup() {
    if (!(getCookie("startup_complete") == "true")) {
        document.cookie = "position=0";
        document.cookie = "startup_complete=true";
    }
    get_destination();
}

    
function increment_position() {
    var position = getCookie("position")
    if (typeof position != 'undefined') {
        var new_position = parseInt(position)+1
        if (new_position >= getCookie("data_length")) {
            new_position = 0;
        }
        document.cookie = "position=" + new_position
    }
}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}