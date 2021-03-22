var form = document.querySelector('.form')
var field = document.querySelector('.form_field')
var button = document.querySelector('.button')
var path = window.location.pathname.split('/').pop()
var balance_field = document.getElementById('balance_field')
var liked_photos = document.getElementById('liked_photos')
var total_payments = document.getElementById('total_payments')
var loaders = document.querySelectorAll('.loader')
var hidden_field = document.getElementById('hidden')
var photo = document.getElementById('photo')
var description = document.getElementById('description')


window.onload = function () {balance_field.value = ''; liked_photos.value = ''; total_payments.value = ''; photo.value = ''; description.value = '';hidden_field.value = path; for (let loader of loaders) {loader.hidden = false}; 
    fetch('/userinfo', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: path
        })
    })
    .then(response => response.json())
    .then(response => {for (let loader of loaders) {loader.hidden = true}; if (response['code'] === 200) { balance_field.value = response['likes_balance']; liked_photos.value = response['total_likes']; total_payments.value = response['total_payments'] } else alert(response['reason']) }
    )
}


form.addEventListener('submit', function (evt) {
    evt.preventDefault(); button.disabled = true;
    fetch('/buylikes', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            number: field.value,
            user_id: path
        })
    })
        .then(response => response.json())
        .then(response => {
            button.disabled = false; field.value = '0';
            if (response['code'] === 400) { alert(response['reason']) } else balance_field.value = response['likes_balance']
        })
})

