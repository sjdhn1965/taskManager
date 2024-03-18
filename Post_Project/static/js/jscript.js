

////View Pending Tasks
$(document).on("click", "#pending", function (o) {

    o.preventDefault()
    var status = 1

    $.ajax({
        type: "POST",
        url: "/viewtask/",
        dataType: 'json',
        data: {
            'status': status,
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
        },
        success: function (response) {


            display_data(response);
        },



        error: function (xhr, textStatus, errorThrown) {
            // handle error response from server, if necessary
            console.log("error", textStatus);
        }
    });

});

//// View Completed Tasks
$(document).on("click", "#complist", function (o) {

    o.preventDefault()
    var status = 0

    $.ajax({
        type: "POST",
        url: "/viewtask/",
        dataType: 'json',
        data: {
            'status': status,
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
        },
        success: function (response) {

            display_data(response);

        },



        error: function (xhr, textStatus, errorThrown) {
            // handle error response from server, if necessary
            console.log("error", textStatus);
        }
    });

});


////// Display data in html page div tag Pending or completed tasks
function display_data(response) {
    var rese = JSON.parse(JSON.stringify(response));


    var imageTag1 = "<img src='/static/img/BL.jpg' class='logo'>";
    var imageTag2 = "<img src='/static/img/oip.jpg' class='logo'>";
    var html = `<table class="table table-striped" id=tableData>
                            <tr>
                              <th>Status</th>
                              <th>Your Bucket List</th>
                              <th>task date set on</th>
                              
                              <th>message for You</th>
                              
                              
                            </tr>`;
    for (var i = 0; i < rese.context.length; i++) {
        var checkboxId = 'checkbox_' + i; // Create a unique ID for each checkbox
        sta = rese.context[0].status
        var checkbox = (sta === 0)
            ? `<input type='checkbox' class='checkbox_class' id='${checkboxId}'>`
            : `<input type='checkbox' class='checkbox_class' id='${checkboxId}' checked>`;

        html += `<tr>
                                    <td>${checkbox}</td>
                                    <td>${rese.context[i].task}</td>
                                    <td>${rese.context[i].dt}</td>
                                    <td>${rese.context[i].task_message}</td>
                                    <td>${imageTag1}</td>
                                    <input type=hidden id=taskid value=${rese.context[i].taskid}>
                                   
                                                                                              </tr>`;



    }
    html += '</table>';

    $(".card-body").html(html);


}

//// logout of user
$(document).on("click", "#logout", function (o) {
    $.ajax({

        url: "/logout/",
        success: function (response) {
            // $("html").html(response);
            window.location.href = '/login/';
        },

    });


});


//// Checkbox Select - unSelect and move to Pending or Completed
$(document).ready(function () {
    var status = 0;
    $(document).on("change", ".checkbox_class", function () {
        const currentRow = $(this).closest('tr'); // 'this' refers to the context where you're handling the event

        // Find the checkbox within the current row
        const checkbox = currentRow.find('input[type="checkbox"]');

        // Check if the checkbox is checked
        if (checkbox.prop('checked')) {
            status = 1;
        }
        var id = $(this).closest('tr').find('#taskid').val();

        $(this).closest("tr").remove();
        sendAjaxPOST(status, id);
    });

});


// $(document).ready(function () {
//     $(document).on("change", ".checkbox_class", function () {
//         var status = 1;
//         var id = $(this).closest('tr').find('#taskid').val();

//         $("#tableData input[type='checkbox']:checked").closest("tr").remove();
//         sendAjaxPOST(status, id);
//     });

// });
//// checkbox selected function call to update to completed or pending
function sendAjaxPOST(status, id) {

    var id = id;

    $.ajax({
        type: "POST",
        url: "/movetask/",
        data: {
            'status': status,
            'id': id,
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
        },
        success: function (response) {


        },

        error: function (xhr, textStatus, errorThrown) {
            // handle error response from server, if necessary
            console.log("error", textStatus);
        }
    });



}
