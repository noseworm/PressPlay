   var counter = 2;
    var limit = 10;
    function addInput(divName){
      if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
       }
      else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = (counter +1) + <input type="text" class="form-control" placeholder="username" name="user_name2">
          "Entry " + (counter + 1) + " <br><input type='text' name='myInputs[]'>";
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     }
}