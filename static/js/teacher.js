username=window.location.href.split("=")[1]
console.log(username)
// c=document.getElementById('username')
// console.log(c.value


function check_avl3(f) {

	c=document.getElementById('username')
	console.log(c.value)
	c.value=username

    e=document.getElementById('cls_code')
    data= new FormData()
    
    data.append('username',username)
    data.append('cls_code',e.value)
    // data.append('password',f.value)
    console.log(e.value)
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {

          console.log(this.responseText);
          g=document.getElementById('print')
          g.innerHTML=this.responseText
      }
    };

    xhttp.open("POST","/check_avl3",true)
		console.log(""+e.value)
    // xhttp.send("username="+e.value+"&password="+f.value)
    xhttp.send(data)
}

class_id=""
function popUp(a){
  console.log(a)
  class_id=a
  console.log(username)
  // document.getElementById("blur").style.filter="blur(8px)"
  pop_up=document.getElementById("ass_container").style
  pop_up.display='block';
  pop_up.background=" linear-gradient(to left, #006699 0%, #669999 100%)"
  pop_up.zIndex=2
  pop_up.filter="drop-shadow(8px 8px 10px gray)"
  pop_up1=document.getElementById("container").style
  pop_up1.backgroundColor="rgba(0,0,0,0.4)"
}

function createAss(){
  data = new FormData();
  data.append('cls_id',class_id);
  data.append('name',document.getElementById('ass_name').value);
  data.append('desc',document.getElementById('ass_desc').value);
  data.append('date',document.getElementById('ass_date').value);
  // data.append('password',f.value)
  console.log(class_id)
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

        console.log(this.responseText);
        document.getElementById("ass_container").style.display='none'
        // some miracle here
        window.open(window.location.href,'_top')
    }
  };

  xhttp.open("POST","/createAss",true)
  // console.log(""+e.value)
  // xhttp.send("username="+e.value+"&password="+f.value)
  xhttp.send(data);
}
function cancel() {
  // body...
  document.getElementById("ass_container").style.display='none'
  class_id=''
}