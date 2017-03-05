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
    var ajax_url = "/destinations?"
    var settings = ["cloud_coverage", "sea_temp", "snow_thickness", "surface_temp"]
    for (index in settings) {
        cookie = getCookie(settings[index])
        if (cookie != "") {
            ajax_url += (settings[index] + "=" + cookie + "&")
        }
    }
    $.ajax({
        url : ajax_url,
        type: "GET",
        dataType: "json",
        success: function(data, textStatus, jqXHR) {
            var position = getCookie("position")
            if(typeof position != 'undefined' && position < data.length) {
                var dest = data[position]
            } else {
                document.cookie = "position=0";
                var dest = data[0]
            }
            if (typeof getCookie("data_length") == 'undefined') {
                document.cookie = "data_length=" + data.length;
            }
            $("#location").text(dest["location"]);
            $("#dest-image").attr("src", dest["image"]);
            $("#description").attr("src", dest["description"]);
            // table values
            $("#temp_val").text(dest["metrics"]["surface_temp"]);
            $("#sea_temp_val").text(dest["metrics"]["sea_temp"]);
            $("#cloud_coverage_val").text(dest["metrics"]["cloud_coverage"]);
            $("#snow_thickness_val").text(dest["metrics"]["snow_thickness"]);
            
            
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Failed. " + textStatus + ": " + errorThrown)
        }
    });
}


function startup() {
    if (!(getCookie("startup_complete") == "true")) {
        document.cookie = "position=0";
        document.cookie = "startup_complete=true";
    }
    store_settings_as_cookies();
    get_destination();
    
}

function store_settings_as_cookies() {
    $.ajax({
        url : "/settings?format=json",
        type: "GET",
        dataType: "json",
        success: function(data, textStatus, jqXHR) {
            document.cookie = "cloud_coverage=" + data["cloudCoverageField"]
            document.cookie = "sea_temp=" + data["seaWaterTempField"]
            document.cookie = "snow_thickness=" + data["snowThicknessField"]
            document.cookie = "surface_temp=" + data["surfaceTempField"]
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Failed. " + textStatus + ": " + errorThrown)
        }
    });
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