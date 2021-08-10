function genkey() {
  $.ajax("/genkey", {
    type: 'GET',  // http method
    success: function(d){
        if (document.getElementById('tohide').style.display == 'block') {
            document.getElementById('tohide').style.display = 'none';
        }

        document.getElementById("key").value = d; 
    }, 
  });
}  


function encrypt_text(name,value) {
  key = document.getElementById('key').value;
  text = document.getElementById('txtarea').value;

  var dict = {};
  dict[name]=value;
  dict["key"]=key;
  dict["value"]=text;


  $.ajax("/encrypttext", {
    contentType: "application/json",
    type: 'POST',  // http method
    data: JSON.stringify(dict),  // data to submit
    success: function(d){
        
        if (d["status"] == "1"){
            document.getElementById("txtarea").value = d["value"];
        }  
        else if (d["status"] == "0"){            
            window.scrollTo(0,0)
            document.getElementById('tohide').style.display = 'block';
            document.getElementById("message").innerHTML = d["value"];
        }      
    }, 
  });
}  



function decrypt_text(name,value) {
  key = document.getElementById('key').value;
  text = document.getElementById('txtarea').value;

  var dict = {};
  dict[name]=value;
  dict["key"]=key;
  dict["value"]=text;


  $.ajax("/decrypttext", {
    contentType: "application/json",
    type: 'POST',  // http method
    data: JSON.stringify(dict),  // data to submit
    success: function(d){
        if (d["status"] == "1"){
            document.getElementById("txtarea").value = d["value"];
        }  
        else if (d["status"] == "0"){
            window.scrollTo(0,0)
            document.getElementById('tohide').style.display = 'block';
            document.getElementById("message").innerHTML = d["value"];
        } 
    }, 
  });
}

function close_msg(){
    document.getElementById('tohide').style.display = 'none';

}  
