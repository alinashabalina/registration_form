var checkbox = document.querySelector('.terms')
var form = document.querySelector('.form')
var fields = document.querySelectorAll('.form_field')
var copy_button = document.querySelector('.copy_button')
var button = document.querySelector('.button')
var validation_field = document.getElementById('form_validation_field')
var error_when_fields_are_empty = 'Fill in the fields above'
var password_field = document.querySelector('.password_field')


form.addEventListener('submit', function (evt) {let ok = true; evt.preventDefault();
    for (let field of fields) { if (field.value === '') {ok = false; field.classList.remove('green'); field.classList.add('red');  validation_field.classList.remove('form_validation_field'); validation_field.innerHTML = error_when_fields_are_empty }; 
    if (field.value.trim() === ''){ok = false; field.classList.remove('green'); field.classList.add('red'); validation_field.innerHTML = error_when_fields_are_empty } }
     if (checkbox.checked === false) {ok = false; alert("Read the terms and agree with them") } 
if (ok === true) {validation_field.classList.add('form_validation_field'); button.disabled = true; for (let field of fields) {field.classList.remove('green')}; fetch('http://127.0.0.1:5000/register', {method: 'POST', headers: { 'Content-Type': 'application/json'}, body: JSON.stringify({
    name: document.getElementById('name').value,
    surname: document.getElementById('surname').value,
    email: document.getElementById('email').value
})})
.then(response => response.json())
.then(response =>{button.disabled = false; for (let field of fields) {field.classList.remove('green'); field.value = ''};
 if (response['code']===200) {alert("You are registered! Copy your temporary password in the field below") ; document.getElementById('default_password').value = response['default_password']; copy_button.disabled = false} 
 else if (response['code']===400){validation_field.classList.remove('form_validation_field'); validation_field.innerHTML = response['reason']} else {console.log(response['code'])}})
}
}
)

for (let field of fields) { field.oninput = function () { field.classList.remove('red'); field.classList.remove('green'); validation_field.classList.add('form_validation_field'); if (field.value.trim().length >= 1) { field.classList.add('green') } } }

copy_button.addEventListener('click', function () {password_field.select();
document.execCommand("copy");})