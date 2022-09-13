function HideErrorMsg() {
    if (document.getElementById('tohide').style.display == 'block') {
      document.getElementById('tohide').style.display = 'none';
      }
}

function CloseMsg(){
    document.getElementById('tohide').style.display = 'none';

}

// disable genkey button when key in custom mode.

$("#pwd").click( function() {
    $(':button.genkey').attr('disabled','disabled');
})

$("#aes").click( function(){
    $(':button.genkey').removeAttr("disabled");
})
