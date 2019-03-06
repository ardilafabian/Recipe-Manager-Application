$(document).ready(function() {
    console.log("Hide ptions!");
    $("#editOptions").hide();
    $("#saveButtonSection").hide();
    $("#idField").hide();

    $("#editButton").click(function() {
        console.log("Oculta acciones!");
        $("#readingOptions").hide();
        $("#editButtonSection").hide();
        $("#returnButtonSection").hide();
        $("#card-header").hide();

        $("#editOptions").show();
        $("#saveButtonSection").show();
        $("#idField").show();
    });

    $("#saveButton").click(function() {
        $("#editOptions").hide();
        $("#saveButtonSection").hide();

        $("#readingOptions").show();
        $("#editButtonSection").show();
        $("#returnButtonSection").show();
    });

    $("#ingredientId").click(function() {
        alert("It is not possible to modify the ID.")
    });
});
