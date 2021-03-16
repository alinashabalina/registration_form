var form = document.querySelector('.form')
var field = document.querySelector('.form_field')
var button = document.querySelector('.button')
var path = window.location.pathname.split('/').pop()
var balance_field = document.getElementById('balance_field')


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

