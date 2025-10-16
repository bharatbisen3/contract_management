// Copyright (c) 2025, bharat and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Project Setup", {
// 	refresh(frm) {

// 	},
// });



frappe.ui.form.on("Project Setup", {
    
    //     refresh: function(frm) {
    //     // Override the status indicator to show custom status
    //     update_status_indicator(frm);
    // },
    
    // status: function(frm) {
    //     // Update indicator when user changes status manually
    //     update_status_indicator(frm);
    // },
    
    // onload: function(frm) {
    //     // Set default status to Open for new documents
    //     if (frm.is_new() && !frm.doc.status) {
    //         frm.set_value('status', 'Open');
    //     }
    // },


    after_save: function(frm) {
        frappe.call({
            method: "contract_management.contract_management.doctype.project_setup.project_setup.create_user_permission",
            args: {
                doc_name: frm.doc.name
            },
            callback: function(response) {
                // console.log(response)
                if (response.message) {
                    // frappe.msgprint(response.message);
                    console.log(response.message)
                }
            }
        });
    },
    before_submit: function(frm) {
        if (frm.doc.status !== "Completed") {
            frappe.msgprint(__('You can only submit this document when the Project is "Completed".'));
            frappe.validated = false;  // Prevent submission
        }
    },

    status: function(frm) {
        if (frm.doc.status === "Completed" && !frm.doc.completion_date) {
            frm.set_value("completion_date", frappe.datetime.get_today());
        }
    }

});



function update_status_indicator(frm) {
    if (frm.doc.status) {
        // Define colors for each status
        const status_colors = {
            'Open': 'blue',
            'Completed': 'green',
            'Cancelled': 'red'
        };
        
        let color = status_colors[frm.doc.status] || 'gray';
        
        // Override the page indicator
        frm.page.set_indicator(frm.doc.status, color);
    }
}







// this below code is not tested only pasted from chat GPT


// frappe.ui.form.on('Project Setup', {

//     // Trigger on load to setup read-only fields or defaults
//     onload: function(frm) {
//         // Auto-set object title if project name and task exist
//         if(frm.doc.project_name && frm.doc.task) {
//             frm.set_value('object_title', `${frm.doc.project_name} - ${frm.doc.task}`);
//         }
//     },

//     // Auto-calculate Object Compensation when relevant fields change
//     project__object_size_in_hecter: calculate_compensation,
//     clearing_cost: calculate_compensation,
//     planting_cost: calculate_compensation,
//     task: function(frm) {
//         // Update object title when task changes
//         if(frm.doc.project_name && frm.doc.task) {
//             frm.set_value('object_title', `${frm.doc.project_name} - ${frm.doc.task}`);
//         }
//         calculate_compensation(frm);
//     },

//     completion_date: function(frm) {
//         // Auto-set completion month
//         if(frm.doc.completion_date) {
//             const month = frappe.datetime.str_to_obj(frm.doc.completion_date).getMonth();
//             const monthNames = ["January","February","March","April","May","June","July",
//                                 "August","September","October","November","December"];
//             frm.set_value('completion_month', monthNames[month]);
//             // Auto-update status
//             frm.set_value('status', 'Completed');
//         }
//     },

//     expected_start_date: validate_dates,
//     expected_end_date: validate_dates
// });

// // Helper function: calculate Object Compensation
// function calculate_compensation(frm) {
//     if(!frm.doc.project__object_size_in_hecter) return;

//     let cost = 0;
//     if(frm.doc.task === 'Forest Clearing') cost = frm.doc.clearing_cost || 0;
//     else if(frm.doc.task === 'Forest Planting') cost = frm.doc.planting_cost || 0;

//     if(cost) {
//         const compensation = cost * frm.doc.project__object_size_in_hecter;
//         frm.set_value('object_compensation', compensation);
//     }
// }

// // Helper function: validate dates
// function validate_dates(frm) {
//     if(frm.doc.expected_start_date && frm.doc.expected_end_date) {
//         if(frappe.datetime.get_diff(frm.doc.expected_end_date, frm.doc.expected_start_date) < 0) {
//             frappe.msgprint(__('End Date must be after Start Date'));
//             frm.set_value('expected_end_date', '');
//         }
//     }
// }


