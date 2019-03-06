$(document).ready(function() {
    console.log("Hide ptions!");
    $("#editOptions").hide();
    $("#saveButtonSection").hide();
    $("#cancelButtonSection").hide();
    $("#idField").hide();
    $("#nameField").hide();
    $("#headerIngredientEditLabel").hide();

    $("#editButton").click(function() {
        console.log("Oculta acciones!");
        $("#readingOptions").hide();
        $("#editButtonSection").hide();
        $("#returnButtonSection").hide();
        $("#headerIngredientName").hide();
        $("#ingredientName").hide();

        $("#editOptions").show();
        $("#headerIngredientEditLabel").show();
        $("#saveButtonSection").show();
        $("#cancelButtonSection").show();
        $("#idField").show();
        $("#nameField").show();
    });

    $("#saveButton").click(function() {
        $("#editOptions").hide();
        $("#saveButtonSection").hide();
        $("#cancelButtonSection").hide();

        $("#readingOptions").show();
        $("#editButtonSection").show();
        $("#returnButtonSection").show();
        $("#ingredientName").hide();
    });

    $("#ingredientId").click(function() {
        alert("It is not possible to modify the ID.")
    });
});
