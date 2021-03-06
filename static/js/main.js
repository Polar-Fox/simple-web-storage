function makeFileOperationRequest(req) {
    $.ajax({
        url: '/ajax',
        data: req,
        dataType: 'json',
        method: 'POST',
        success: function(data, textStatus, jqXHR) {
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

function createNewDirectory(dirname) {
    var req = {
        'dir': $('input[name="dir"]').eq(0).val(),
        'action': 'new_directory',
        'dirname': dirname
    };
    makeFileOperationRequest(req);
};

function makePublicLink(dirname, filename) {
    var req = {
        'action': 'make_public_link',
        'dir': dirname,
        'filename': filename
    };
    makeFileOperationRequest(req);
};

function removePublicLink(dirname, filename) {
    var req = {
        'action': 'remove_public_link',
        'dir': dirname,
        'filename': filename
    };
    makeFileOperationRequest(req);
};

function renameEntry(dirname, entryname) {
    vex.dialog.prompt({
        message: 'Rename',
        placeholder: 'enter name',
        value: entryname,   
        callback: function(value) {
            if (value != undefined) {
                var req = {
                    'action': 'rename_entry',
                    'dir': dirname,
                    'old_name': entryname,
                    'new_name': value
                };
                makeFileOperationRequest(req);
            }
        }
    });
};

function deleteEntry(dirname, entryname) {
    vex.dialog.confirm({
        message: 'Are you sure you want to delete "'+entryname+'"?',
        callback: function(value) {
            if (value) {
                var req = {
                    'action': 'delete_entry',
                    'dir': dirname,
                    'entryname': entryname
                };
                makeFileOperationRequest(req);
            }
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

    $('#btn_upload').click(function() {
        vex.dialog.open({
            message: 'Upload a file:',
            buttons: [
                $.extend({}, vex.dialog.buttons.YES, { text: 'Upload' }),
                $.extend({}, vex.dialog.buttons.NO, { text: 'Cancel' })
            ],
            shouldClose: false,
            input:
                '<form id="upload_form" action="" method="POST" enctype="multipart/form-data"> '+
                '    <input type="file" name="file"> '+
                '</form>',
            callback: function(data) {
                if (data) {
                    $('#upload_form').submit();
                }
            },
            onSubmit: function(e) {
                var filename = $('#upload_form input[name="file"]').eq(0).val();
                if (!filename) {
                    vex.dialog.alert('Choose a file');
                }
                else {
                    $('#upload_form').submit();
                }
                e.preventDefault();
            }
        });

        return false;
    });
});