var form = document.querySelector('.form')
var field = document.getElementById('email')
var submit_button = document.querySelector('.button')
var validation_field = document.querySelector('.form_validation_field')

field.addEventListener('input', function () {
   field.classList.remove('red'); field.classList.remove('green'); validation_field.classList.add('form_validation_field');
   if (field.value.trim().length >= 1) { field.classList.add('green') }
})

form.addEventListener('submit', function (evt) {
   let ok = true; evt.preventDefault(); field.classList.remove('green'); field.classList.remove('red'); validation_field.classList.add('form_validation_field');
   if (field.value === '') {
      ok = false; field.classList.remove('green'); field.classList.add('red'); validation_field.classList.remove('form_validation_field');
      validation_field.innerHTML = 'Fill in the fields above'
   }
   if (ok === true) {
      submit_button.disabled = true; fetch('/recover', {
         method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
            email: document.getElementById('email').value
         })
      })
         .then(response => response.json())
         .then(response => {
            submit_button.disabled = false; field.value = ''; field.classList.remove('green');
            if (response['reason']) { alert(response['reason']) } else { window.location.href = response['link'] }
         })
   }
})

