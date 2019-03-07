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

  $("#data").hide();
  var emptyRow = document.getElementById("empty");
  if(emptyRow){
    emptyRow.parentNode.removeChild(emptyRow);
  }

  var tr = document.createElement('tr');
  var td1 = tr.appendChild(document.createElement('td'));
  td1.innerHTML = 1.0;
  var td2 = tr.appendChild(document.createElement('td'));
  td2.innerHTML = $("#name"+ data)[0].innerHTML;

  var table = document.getElementById("table");

  table.appendChild(tr);
}
