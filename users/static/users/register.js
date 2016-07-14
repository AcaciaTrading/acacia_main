var id_user = "#id_username";
var id_pass = "#id_password2";

var check = null;

function setMessage(id, type, message) {
    $(id + '_help').remove()
    $(id).siblings(".help-block").remove();
    $(id).parent().parent().attr('class', 'form-group has-' + type);
    $(id).parent().append('<span id="' + id + '_help" class="help-block ">' + message + '</span>');
}

function removeMessage(id) {
    $(id + '_help').remove()
    $(id).siblings(".help-block").remove();
    $(id_user).parent().parent().attr('class', 'form-group');
}

$(id_user).attr('autocomplete', 'off')

$(id_user).keydown(function(e) {
    clearTimeout(check)
    check = setTimeout(function() {
        $.get("/accounts/username/", {'username':$(id_user).val()}, function(data) {
            if(data == "true") {
                setMessage(id_user, "error", "Username taken!");
            }
            else if(data == "false") {
                 setMessage(id_user, "success", "Username available!");
            }
            else {
                removeMessage(id_user);
            }
        });
    }, 400);
});


$(id_pass).keydown(function(e) {
    setTimeout(function() {
        console.log($(id_pass).val() + $("#id_password1").val());
        if($(id_pass).val() == $("#id_password1").val()) {
            setMessage(id_pass, "success", "Passwords match!");
        }
        else {
            setMessage(id_pass, "error", "Passwords do not match.");
        }
    }, 10);
});