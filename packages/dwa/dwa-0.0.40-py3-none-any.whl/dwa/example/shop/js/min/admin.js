$("input#db__sql_execute").click(function () {
    if (!confirm("Are you sure?")) {return;}
    $.post("shop", "db=_sql&op=execute&_sql="+encodeURIComponent($(this).prev().val()), function(response) {
        if (typeof response == "string") {
            alert(response);
            return;
        }
        if (response.length === 0) {
            $("div#_sql_result").html("No result.");
            return;
        }
        var html = "<table>";
        html += "<tr>";
        for (var k of Object.keys(response[0])) {
            html += "<th>"+k+"</th>";
        }
        html += "</tr>";
        for (var i=0; i<response.length; i++) {
            html += "<tr>";
            for (var k of Object.keys(response[i])) {
                var v = response[i][k];
                if (v === null) {
                    v = "";
                }
                html += "<td>"+v+"</td>";
            }
            html += "</tr>";
        }
        html += "</table>";
        $("div#_sql_result").html(html);
    }).fail(function(response){
        alert(JSON.parse(response.responseText)["msg"]);
    });
});