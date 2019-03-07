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

  var emptyRow = document.getElementById("empty");
  if(emptyRow){
    emptyRow.parentNode.removeChild(emptyRow);
  }

  var tr = document.createElement('tr');
  var td2 = tr.appendChild(document.createElement('td'));
  td2.innerHTML = $("#name"+ data)[0].innerHTML;

  var input = document.createElement('input');
  input.type = "number";
  input.step = "0.01";
  input.name = "quantity";
  input.required = true;
  input.className = "form-control text-dark";
  var td1 = tr.appendChild(document.createElement('td'));
  td1.appendChild(input);

  var td3 = tr.appendChild(document.createElement('td'));
  td3.innerHTML = $("#unit"+ data)[0].innerHTML;

  var table = document.getElementById("table");

  table.appendChild(tr);
}
