

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

            sta = rese.context[0].status

            if (sta == 0) {
                var checkbox = "<input type='checkbox' id='checkbox2'>"
            }
            else {

                var checkbox = "<input type='checkbox' id='checkbox1' checked>"
            }



            var html = `<table class="table table-striped" id=tableData>
                            <tr>
                              <th>Status</th>
                              <th>Bucket List</th>
                              <th>Date created</th>
                              
                              
                            </tr>`;

            for (var i = 0; i < rese.context.length; i++) {
                html += `<tr>
                           <td>${checkbox}</td>
                           <td>${rese.context[i].task}</td>
                           <td>${rese.context[i].dt}</td>
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
            $(document).on("change", "#checkbox1", function () {
                status = 0;
                var id = $(this).closest('tr').find('#taskid').val();

                $(this).closest("tr").remove();
                sendAjaxPOST(status, id);
            });

        });


        $(document).ready(function () {
            $(document).on("change", "#checkbox2", function () {
                status = 1;
                var id = $(this).closest('tr').find('#taskid').val();

                $("#tableData input[type='checkbox']:checked").closest("tr").remove();
                sendAjaxPOST(status, id);
            });

        });
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
