// // // frappe.pages['get-emp-json'].on_page_load = function(wrapper) {
// // // 	var page = frappe.ui.make_app_page({
// // // 		parent: wrapper,
// // // 		title: 'Employee Json',
// // // 		single_column: true
// // // 	});
// // // }


// // // //









// frappe.pages['get-emp-json'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Employee Json',
//         single_column: true
//     });

//     // Container for table
//     $(`
//         <div class="employee-table-section">
//             <h4>Employee List</h4>
//             <div id="employee-table">Loading...</div>
//         </div>
//     `).appendTo(page.body);

//     // Call our server-side API (safe, no token in browser)
//     frappe.call({
//         method: "contract_management.contract_management.api.grist_api.get_employees_from_grist",
//         callback: function(r) {
//             if (r.message && r.message.length > 0) {
//                 render_employee_table(r.message);
//             } else {
//                 $("#employee-table").html("<p>No employees found.</p>");
//             }
//         },
//         error: function(err) {
//             console.error("Error fetching employee data:", err);
//             $("#employee-table").html("<p>Error loading data.</p>");
//         }
//     });
// };

// // Function to render employee data into a table
// function render_employee_table(records) {
//     // Get field keys from first record
//     let keys = Object.keys(records[0].fields);

//     let html = `<table class="table table-bordered table-striped"><thead><tr>`;
//     keys.forEach(k => {
//         html += `<th>${k}</th>`;
//     });
//     html += `</tr></thead><tbody>`;

//     records.forEach(rec => {
//         html += `<tr>`;
//         keys.forEach(k => {
//             let cell = rec.fields[k];
//             if (cell === null || cell === undefined) cell = "";
//             html += `<td>${cell}</td>`;
//         });
//         html += `</tr>`;
//     });

//     html += `</tbody></table>`;
//     $("#employee-table").html(html);
// }















let currentLimit = 10;
let currentOffset = 0;

frappe.pages['get-emp-json'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Employee Json',
        single_column: true
    });

    $(`
        <div class="employee-table-section">
            <h4>Employee List</h4>
            <div class="controls mb-3">
                <label>Show:
                    <select id="limit-select" class="form-select d-inline-block" style="width:auto;">
                        <option value="10" selected>10</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                        <option value="500">500</option>
                        <option value="1000">1000</option>
                    </select>
                </label>
                <button id="prev-btn" class="btn btn-sm btn-secondary ms-3">Previous</button>
                <button id="next-btn" class="btn btn-sm btn-secondary">Next</button>
            </div>
            <div id="employee-table">Loading...</div>
        </div>
    `).appendTo(page.body);

    // Fetch first time
    fetch_employees();

    // Change limit
    $("#limit-select").on("change", function() {
        currentLimit = parseInt($(this).val());
        currentOffset = 0; // reset to first page
        fetch_employees();
    });

    // Prev button
    $("#prev-btn").on("click", function() {
        if (currentOffset >= currentLimit) {
            currentOffset -= currentLimit;
            fetch_employees();
        }
    });

    // Next button
    $("#next-btn").on("click", function() {
        currentOffset += currentLimit;
        fetch_employees();
    });
};

// Fetch employees with current limit/offset
function fetch_employees() {
    $("#employee-table").html("Loading...");

    frappe.call({
        method: "contract_management.contract_management.api.grist_api.get_employees_from_grist",
        args: {
            limit: currentLimit,
            offset: currentOffset
        },
        callback: function(r) {
            if (r.message && r.message.records && r.message.records.length > 0) {
                render_employee_table(r.message.records);
            } else {
                $("#employee-table").html("<p>No employees found.</p>");
            }
        },
        error: function(err) {
            console.error("Error fetching employee data:", err);
            $("#employee-table").html("<p>Error loading data.</p>");
        }
    });
}

// Render table
function render_employee_table(records) {
    let keys = Object.keys(records[0].fields);

    let html = `<table class="table table-bordered table-striped"><thead><tr>`;
    keys.forEach(k => {
        html += `<th>${k}</th>`;
    });
    html += `</tr></thead><tbody>`;

    records.forEach(rec => {
        html += `<tr>`;
        keys.forEach(k => {
            let cell = rec.fields[k];
            if (cell === null || cell === undefined) cell = "";
            html += `<td>${cell}</td>`;
        });
        html += `</tr>`;
    });

    html += `</tbody></table>`;
    $("#employee-table").html(html);
}
