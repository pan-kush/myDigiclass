// //  document.getElementById("sub").addEventListener("click", function(event)
// // {
// // event.preventDefault()
// // // sendclg_id()
// // }); 

// console.log(window.location.href)

    
// function check_avl2(f) {

//     e=document.getElementById('user_data1')
//     h=document.getElementById('clg_id')
//     data= new FormData()
//     data.append('username',e.value)
//     data.append('clg_id',h.value)
//     // data.append('password',f.value)
//     console.log(e.value,h.value)
//     var xhttp = new XMLHttpRequest();

//     xhttp.onreadystatechange = function() {
//       if (this.readyState == 4 && this.status == 200) {

//           console.log(this.responseText);
//           g=document.getElementById('print')
//           g.innerHTML=this.responseText
//       }
//     };

//     xhttp.open("POST","/check_avl2",true)
//     console.log(""+e.value)
//     // xhttp.send("username="+e.value+"&password="+f.value)
//     xhttp.send(data)


// }

// function create_id2() 
// {
//     h=document.getElementById('clg_id')
//     f=document.getElementById('print')
//     if(f.innerHTML=='In_use')
//     {
//       f.style.color='red'
//       return
//     }
//     data= new FormData()
//     for(i=1;i<=3;i++)
//     {
//       e=document.getElementById('user_data'+i)
//       data.append('user_data'+i,e.value)
//       console.log('user_data'+i,e.value)
//     }
//     data.append('clg_id',h.value)
//     // data.append('password',f.value)
//     console.log(data)
//     var xhttp = new XMLHttpRequest();

//     xhttp.onreadystatechange = function() 
//     {
//       if (this.readyState == 4 && this.status == 200) 
//       {

//           console.log(this.responseText);
//           // g=document.getElementById('print1')
//           // g.innerHTML=this.responseTex

//           f.innerHTML=""
//           for(i=1;i<=3;i++)
//           {
//             document.getElementById('user_data'+i).value=""
//           }
//         window.open("/teach_or_stud","_top")
//       }
//      };

//     xhttp.open("POST","/create_id2",true)
//     // console.log(""e.value)
//     // xhttp.send("username="+e.value+"&password="+f.value)
//     xhttp.send(data)
// }

// available_clgs=[]

// var xhttp = new XMLHttpRequest();
// xhttp.onreadystatechange = function() 
// {
//   if (this.readyState == 4 && this.status == 200) 
//   {
//       available_clgs=this.responseText.split(" ");
//       console.log(available_clgs);
//   }
//  };

// xhttp.open("GET","/availableClgs",true)
// xhttp.send()

// function fetch() {
  
// }

function fun(){
  ele=document.getElementById("clginput").style
  ele.display="block"
  ele.height=screen.height+'px'
  ele.width=screen.width+'px'
  inp=document.getElementById("myUL").style
  inp.opacity=1;
  // inp.width=screen.width*3/10 + 'px'
  // inp.top='30%'
  // inp.left=(screen.width-inp.width)/2 + 'px'
  // console.log(inp.left,inp.width)
}