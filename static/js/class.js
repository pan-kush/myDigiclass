

// IMPLEMENTING PROFILE MODAL


// console.log(profileMenu.style);


// let toggleProfileMenu = () => {
// 	this.classList.toggle("active");
// 	console.log('profile button clicked');
// 	// if(profileMenu.style.display === 'none') {
// 	// 	profileMenu.style.display = 'block';
// 	// } else {
// 	// 	profileMenu.style.display = 'none';
// 	// }
// }
// console.log(document.getElementById('icon-profile'));
let profileDiv = document.getElementById('icon-profile');
let profileMenu = document.getElementsByClassName('dropdown-profile')[0];
profileMenu.style.display = 'none';
profileDiv.onclick = function () {
	let showDiv = () => { return (profileMenu.style.display == "none")};
	if(showDiv()) {
		profileMenu.style.display = 'block'
	} else {
		profileMenu.style.display = 'none'
	}
}

// function toggleProfileMenu() {
// 	console.log('inside method');
	
// 	if(profileMenu.style.display === 'none') {
// 		profileMenu.style.display = 'block';
// 	} else {
// 		profileMenu.style.display = 'none';
// 	}
// }



// document.querySelector(".panel ul .dropdown-profile").addEventListener("click", 
// function(){
// 	this.classList.toggle("active");
// });



// Previous JS code
username=window.location.href.split("&")[1].split("=")[1]
console.log(username)
cls_id=window.location.href.split("&")[0].split("=")[1]
console.log(cls_id)

function scroll(){
  obj=document.getElementById("post")
  h=obj.scrollHeight
  console.log(h);
  obj.animate({scrollTop:h},1000)
}
// *****************
// yet to check if post containts are
// *****************
function postdata(){

	file=false;
	fileInputElement=document.getElementById('file_post')
  text = document.getElementById('posting')

  if(fileInputElement.value!="")file=true;
	// console.log(file)
  if(!file && text.value=="")
    return;

	var xhttp= new XMLHttpRequest();
  	xhttp.onreadystatechange=function()
  	{

  		 if (this.readyState == 4 && this.status == 200) 
  		 {
			window.open(window.location.href,"_top");
  	  	 }
	}
	
		// console.log(username)
    // xhttp.send("username="+e.value+"&password="+f.value)
     url="/append_post"
     data= new FormData()
     data.append('username',username)
     data.append('cls_id',cls_id)
     if (!file)
     	data.append('text',text.value)
     else{
     	data.append('file',fileInputElement.files[0])
     	url="/upload"
     }
     data.append('time',new Date().toLocaleString())
     xhttp.open("POST",url,true)
     xhttp.send(data)

}
	    	
p_len = 0;
function updatePosts(){
    var xhttp= new XMLHttpRequest();
  	xhttp.onreadystatechange=function()
  	{

  		 if (this.readyState == 4 && this.status == 200) {

  		  x=JSON.parse(this.responseText)
          // console.log(x);
		  len = Object.keys(x).length;
		  if (len>p_len){
		  	col = document.getElementById("post")
		  	col.innerHTML="";
              for (var i = 0; i<len; i++) 
              {
              	idx = i;
              	console.log(x[i])
              	var div = document.createElement("div");
				div.innerHTML = `<div style='position:aboslute;'><div class='time'>${x[idx]['time']}</div>
				<div class='username'>${x[idx]['username']}</div></div>
				<div class='text'>${x[idx]['text']}</div>`
				
				if (x[idx]['occ']=='Teacher'){
					div.style.float='left'
					div.className='container'
					col.appendChild(div);
				}
				else{
					div.style.float='right'
					div.className='container'
					col.appendChild(div)
				// document.getElementById("classes").appendChild( document.createElement("div"));
              	}
              }
              p_len=len;
          }
  	  }
	}
	xhttp.open("POST","/retrieve_post",true)
	 // console.log(username)
   
	 data= new FormData()
	 data.append('username',username)
	 data.append('cls_id',cls_id)
    xhttp.send(data)
    setTimeout(updatePosts,5000);
} 
// updatePosts()

obj=document.getElementById("post")
h=obj.scrollHeight
console.log(h);
  // obj.animate({scrollTop:h},1000)
obj.scrollTop=h;

