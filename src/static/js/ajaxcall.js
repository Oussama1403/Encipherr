function genkey() {
    $.ajax("/genkey", {
      type: 'GET',  // http method
      success: function(d){
          HideErrorMsg()
          document.getElementById("key").value = d; 
      }, 
    });
}  
  
function text_mode(name,value) {
    key = document.getElementById('key').value;
    key_type = document.querySelector("input[type='radio'][name=key_type]:checked").value;
    text = document.getElementById('txtarea').value;
    var dict = {};
    dict[name]=value;
    dict["key"]=key;
    dict["key_type"] = key_type;
    dict["value"]=text;

    $.ajax("/text", {
      contentType: "application/json",
      type: 'POST',  // http method
      data: JSON.stringify(dict),  // data to submit
      success: function(d){
          HideErrorMsg()
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