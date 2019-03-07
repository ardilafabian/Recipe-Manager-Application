function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  console.log("Strat dragging")
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  console.log(data)

  //Remove message of empty ingredients
  var emptyRow = document.getElementById("empty");
  if(emptyRow){
    emptyRow.parentNode.removeChild(emptyRow);
  }

  var tr = document.createElement('tr');

  //Create and Fill ID ingredient field on recipe table
  var inputID = document.createElement('input');
  inputID.type = "text";
  inputID.disabled = true;
  inputID.name = "ingredient_id";
  inputID.required = true;
  inputID.className = "form-control text-dark";
  inputID.value = data;
  var td4 = tr.appendChild(document.createElement('td'));
  td4.appendChild(inputID);

  //Fill name field on recipe table
  var td2 = tr.appendChild(document.createElement('td'));
  td2.innerHTML = $("#name"+ data)[0].innerHTML;

  //Create and Fill quantity field on recipe table
  var input = document.createElement('input');
  input.type = "number";
  input.step = "0.01";
  input.name = "quantity";
  input.required = true;
  input.className = "form-control text-dark";
  input.value = 1.0;
  var td1 = tr.appendChild(document.createElement('td'));
  td1.appendChild(input);

  //Fill quantity field on recipe table
  var td3 = tr.appendChild(document.createElement('td'));
  td3.innerHTML = $("#unit"+ data)[0].innerHTML;

  var table = document.getElementById("table");

  table.appendChild(tr);
}
