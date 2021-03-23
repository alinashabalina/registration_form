var pic1 = document.getElementById('pic0')
var pic2 = document.getElementById('pic1')
var pic3 = document.getElementById('pic2')
var pic4 = document.getElementById('pic3')
var pic5 = document.getElementById('pic4')
var pic6 = document.getElementById('pic5')
var dict = {}

window.onload = function () {fetch ('/int_gallery', {method: POST, headers: { 'Content-Type': 'application/json' }
})
.then(response=>response.json())
.then(response => {dict = response})
}

