function createNewDirectory(dirname) {
    var req = {
        'dir': $('input[name="dir"]').eq(0).val(),
        'action': 'new_directory',
        'dirname': dirname
    };

    $.ajax({
        url: '/ajax',
        data: req,
        dataType: 'json',
        method: 'POST',
        success: function(data, textStatus, jqXHR) {
            console.log(data);
            console.log(textStatus);
            if (data['result'] == 'OK') {
                location.reload();
            }
            else if (data['result'] == 'error') {
                vex.dialog.alert({ unsafeMessage: '<b>Error:</b> '+data['message'] });
            }
        },
        error: function(data, textStatus, jqXHR) {
            console.log('Error: '+textStatus);
        }
    });
};

$(document).ready(function() {
    $('#btn_new_directory').click(function() {
        vex.dialog.prompt({
            message: 'Create new folder',
            placeholder: 'enter name',
            callback: function(value) {
                if (value != undefined) {
                    createNewDirectory(value);
                }
            }
        });
        return false;
    });
});