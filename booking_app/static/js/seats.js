var last_seat_id = "none";
var last_seat_color ="none";

function enable_button(id){
    var img_var = 
    console.log(last_seat_id+"-seat");
    if(last_seat_id== id){
        console.log("do nothing");
    }
    if(last_seat_id!="none"){
        var img_var = document.getElementById(last_seat_id+"-seat");
        document.getElementById(last_seat_id).disabled = true;
        img_var.src = last_seat_color;        
        document.getElementById(id).disabled = false;
        last_seat_color = document.getElementById(id+"-seat").src;
        document.getElementById(id+"-seat").src ="static/grey.png";
        last_seat_id = id;
    }
    else{
        last_seat_color = document.getElementById(id+"-seat").src;
        document.getElementById(id+"-seat").src ="static/grey.png";
        document.getElementById(id).disabled = false;
        last_seat_id = id;
    }
    
  }