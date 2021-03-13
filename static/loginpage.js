var fields = document.querySelectorAll('.form_field')
var form = document.querySelector('.form')
var submit_button = document.querySelector('.button')
var validation_field = document.querySelector('.form_validation_field')

form.addEventListener('submit', function (evt) {
    let ok = true; evt.preventDefault();
    for (let field of fields) { if (field.value === '') { ok = false; field.classList.remove('green'); field.classList.add('red'); document.getElementById('form_validation_field').classList.remove('form_validation_field');
     document.getElementById('form_validation_field').innerHTML = 'Fill in the fields above' } }
    if (ok === true) {
        submit_button.disabled = true; fetch('http://127.0.0.1:5000/login', {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
                email: document.getElementById('email').value,
                password: document.getElementById('password').value
            })
        })
            .then(response => response.json())
            .then(response => {
                submit_button.disabled = false; for (let field of fields) { field.classList.remove('green') }
                if (response['user_id'] != null) { window.location.href = 'http://127.0.0.1:5000/area/' + response['user_id'] }
                else {
                    document.getElementById('form_validation_field').classList.remove('form_validation_field');
                    document.getElementById('form_validation_field').innerHTML = response['reason']
                }
            })
    }
}
)