function getValue() {
    $.ajax({
        url: 'validate',
        data: JSON.stringify($('#editor').serialize()),
        type: 'POST',
        success: function (response) {
            $('#terminal' ).val(response)
        },
        error: function (error) {
            $('#terminal').val(error)
        }
    });
}