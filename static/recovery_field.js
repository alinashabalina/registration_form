var form = document.querySelector('.form')
var field = document.querySelector('.password_field')
var copy_button = document.querySelector('.copy_button')
var button = document.querySelector('.button')
var validation_field = document.getElementById('form_validation_field')
var error_when_fields_are_empty = 'Fill in the fields above'
var password_field = document.querySelector('.password_field')
var path = window.location.pathname.split('/').pop()


button.addEventListener('click', function (evt) {
    button.disabled = true; fetch('/setapassword', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
            link_id: path
        })
    })
        .then(response => response.json())
        .then(response => {
            button.diabled = false; if (response['code'] === 200) { field.value = response['new_password']; copy_button.disabled = false }
            else { alert(response['reason']) }
        })
})


copy_button.addEventListener('click', function () {
    password_field.select();
    document.execCommand("copy")
})
