var checkbox = document.querySelector('.terms')
var submit_button = document.querySelector('.submit')
var fields = document.querySelectorAll('.form_field')

submit_button.addEventListener('click', function () {for (let field of fields){if (field.value === ''){field.classList.add('red')}}})