// $(document).ready(function() {
//     $('.js-example-basic-multiple').select2();
// });

$("#delete_user").on('shown.bs.modal', function(){
    console.log("show")
   alert("show");
});

$("#delete_user").on('hidden.bs.modal', function(){
    console.log("hide")
   alert("hide");
});

