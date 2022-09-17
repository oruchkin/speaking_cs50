window.addEventListener('load', (event) => {
});
// share button witch copy link
function share_question_button(question_pk){
    let shareButton = document.getElementById('share-button-' + question_pk);
    let shareDialog = document.getElementById('share-dialog-' + question_pk);
    let closeButton = document.getElementById('close-button-' + question_pk);
    
    if (shareDialog.classList[1] == 'is-open'){
        shareDialog.classList.remove('is-open');
    }
    else {
        shareDialog.classList.add('is-open');
    }

    closeButton.addEventListener('click', event => {
        shareDialog.classList.remove('is-open');
    });
}


function share_theme_button(theme_pk){
    let shareButton = document.getElementById('share-button-t' + theme_pk);
    let shareDialog = document.getElementById('share-dialog-t' + theme_pk);
    let closeButton = document.getElementById('close-button-t' + theme_pk);
    
    if (shareDialog.classList[1] == 'is-open'){
        shareDialog.classList.remove('is-open');
    }
    else {
        shareDialog.classList.add('is-open');
    }

    closeButton.addEventListener('click', event => {
        shareDialog.classList.remove('is-open');
    });
}


// when copy link pressed
function copy_theme_question_share_link(button_copy_id) {
    console.log(button_copy_id)
    var copy_link = document.getElementById(button_copy_id);
    navigator.clipboard.writeText(copy_link.getAttribute('value'));
    copy_link.innerHTML = " &nbsp; Copied &nbsp;&nbsp; "
    setTimeout(function(){
        copy_link.innerHTML = "Copy Link"
    }, 500); 
}


//robot vocalize theme title
function say(m) {
    var msg = new SpeechSynthesisUtterance();
    var voices = window.speechSynthesis.getVoices();
    msg.voice = voices[10];
    msg.voiceURI = "native";
    msg.volume = 1;
    msg.rate = 1;
    msg.pitch = 0.8;
    msg.text = m;
    msg.lang = 'en';
    speechSynthesis.speak(msg);
}


