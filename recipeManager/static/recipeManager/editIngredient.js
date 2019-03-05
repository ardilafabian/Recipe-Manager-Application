$(document).ready(function() {
    console.log("Hide ptions!");
    $("#editOptions").hide();
    $("#saveButtonSection").hide();

    $("#editButton").click(function() {
        console.log("Oculta acciones!");
        $("#readingOptions").hide();
        $("#editButtonSection").hide();
        $("#returnButtonSection").hide();

        $("#editOptions").show();
        $("#saveButtonSection").show();
    });

    $("#saveButton").click(function() {
        $("#editOptions").hide();
        $("#saveButtonSection").hide();

        $("#readingOptions").show();
        $("#editButtonSection").show();
        $("#returnButtonSection").show();


    });
});
