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