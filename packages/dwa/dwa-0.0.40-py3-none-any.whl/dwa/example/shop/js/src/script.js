$.post("/api", "request=test&a=123", function(response){
    $("body").html(response.toString());
});