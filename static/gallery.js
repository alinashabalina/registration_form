var pics = document.querySelectorAll('.pic')
var dict = {}
var img_template = document.querySelector('#img-template').content
var img_src = img_template.querySelector('.gallery_photo')
var i = 0

window.onload = function () {fetch ('/int_gallery', {method:'POST', headers: { 'Content-Type': 'application/json' }
})
.then(response=>response.json())
.then(response => {dict = response})
}

for (let pic of pics) {pic.addEventListener('click', 
function () {let cloned = img_src.cloneNode(false); cloned.src = '/photos/'+String(dict[i]['name']);
 i+=1; pic.removeChild(pic.querySelector('.svg')); pic.appendChild(cloned)})}