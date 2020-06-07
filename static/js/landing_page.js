  document.getElementById("sub").addEventListener("click", function(event)
  {
  event.preventDefault()
  // sendclg_id()
  });

 console.log(window.location.href)

  function sendclg_id() {
    e=document.getElementById('clg_id');
    f=document.getElementById('clg_pass');
    data= new FormData()
    data.append('username',e.value)
    data.append('password',f.value)
    console.log(e.value,f.value)
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {

          console.log(this.responseText);
          if (this.response=='Invalid Credentials')
          {
            g=document.getElementsByClassName('a')
            for (var i =g.length - 1; i >= 0; i--) {
             
                  g[i].value=""
                  g[i].placeholder="Wrong Info"
                  g[i].style.borderColor="red"
                  console.log(console.dir(g[i].style))

            }

          }
          else
          {
            window.open(this.response+"?"+'clg_id='+e.value)
          }
      }
    };
     xhttp.open("POST","/loginrequest",true)
    console.log("username="+e.value+"&password="+f.value)
    // xhttp.send("username="+e.value+"&password="+f.value)
    xhttp.send(data)

  }
    
  function check_avl(f) {

      e=document.getElementById('clg_data2')
      data= new FormData()
      data.append('Colg_id',e.value)
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

      xhttp.open("POST","/check_avl",true)
      console.log(""+e.value)
      // xhttp.send("username="+e.value+"&password="+f.value)
      xhttp.send(data)


  }

  function create_id() {


      f=document.getElementById('print')
      if(f.innerHTML=='In_use'){
        f.style.color='red'
        return
      }
      data= new FormData()
      for(i=1;i<=3;i++){
        e=document.getElementById('clg_data'+i)
        data.append('clg_data'+i,e.value)
        console.log('clg_data'+i,e.value)
      }
      // data.append('password',f.value)
      console.log(data)
      var xhttp = new XMLHttpRequest();

      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            console.log(this.responseText);
            g=document.getElementById('print1')
            g.innerHTML=this.responseText

            f.innerHTML=""
            for(i=1;i<=3;i++){
              document.getElementById('clg_data'+i).value=""
            }

        }
      };

      xhttp.open("POST","/create_id",true)
      // console.log(""e.value)
      // xhttp.send("username="+e.value+"&password="+f.value)
      xhttp.send(data)
}
  