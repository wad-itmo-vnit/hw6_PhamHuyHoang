let container = document.getElementsByClassName('container')[0];
let modal = document.getElementsByClassName('modal')[0];
let close = document.getElementsByTagName('span')[0];
let picModal = document.getElementById('picModal');
let pic = document.getElementsByClassName('item');
    
for (let i=0; i<pic.length; i++){
    pic[i].onclick=function(){
        picModal.src= pic[i].firstElementChild.src;
        modal.style.display='block';
    }
}

close.onclick= function (){
    modal.style.display='none';
}
document.addEventListener('keydown',(e) =>{
    if (e.key === 'Escape'){
        modal.style.display='none';
    }
})

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

document.getElementById('username').innerHTML= getCookie('username');

