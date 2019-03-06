$(document).ready(function() {
    console.log("Hide ptions!");
    $("#editOptions").hide();
    $("#saveButtonSection").hide();
    $("#idField").hide();
    $("#nameField").hide();

    $("#editButton").click(function() {
        console.log("Oculta acciones!");
        $("#readingOptions").hide();
        $("#editButtonSection").hide();
        $("#returnButtonSection").hide();
        $("#card-header").hide();
        $("#ingredientName").hide();

        $("#editOptions").show();
        $("#saveButtonSection").show();
        $("#idField").show();
        $("#nameField").show();
    });

    $("#saveButton").click(function() {
        $("#editOptions").hide();
        $("#saveButtonSection").hide();

        $("#readingOptions").show();
        $("#editButtonSection").show();
        $("#returnButtonSection").show();
        $("#ingredientName").hide();
    });

    $("#ingredientId").click(function() {
        alert("It is not possible to modify the ID.")
    });
});
