$(document).ready(function() {
    $('.js-example-basic-multiple').select2();
});

// $("#description").submit(function(e) {
//     e.preventDefault();
// });


 // $("#description").on('shown.bs.modal', function() {
 //    refresh = "false";}
 // );

// $("#description").on('shown.bs.modal', function() {
//     window.stop()}
// );

if (('#description').is(':visible')) {
    console.log("widać")
}

if (!$('#description').is(':visible')) {
    console.log("nie widać")
}





 // $(window).on('hidden.bs.modal', function(){
 // ('#description').modal('hide');
 // refresh = "true";}
 // );