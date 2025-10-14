// // // frappe.ui.form.on('Project Attendance', {
// // // 	refresh(frm) {
// // // 		// your code here
// // // 	}
// // // })





// frappe.ui.form.on('Project Attendance', {

//     onload: function(frm) {
//         if(frm.doc.project__client) {
//             // Auto-fill work team, task, SLA class, total area
//             frm.trigger('fetch_project_data');
//         }
//     },

//     project__client: function(frm) {
//         if(frm.doc.project__client) {
//             frm.trigger('fetch_project_data');
//         }
//     },

//     show_work_team_members: function(frm) {
//         frm.refresh_field('team_members_section');
//     },

//     area_completed_for_this_submission: function(frm) {
//         validate_area(frm);
//     },

//     start_date: validate_date_fields,
//     end_date: validate_date_fields
// });

// // Fetch project-related fields from linked Project Setup
// frappe.ui.form.on('Project Attendance', 'fetch_project_data', function(frm) {
//     if(frm.doc.project__client) {
//         frappe.db.get_doc('Project Setup', frm.doc.project__client)
//         .then(project => {
//             frm.set_value('work_team', project.work_team);
//             frm.set_value('task', project.task);
//             frm.set_value('classified_sla_class', project.sla_class);
//             frm.set_value('total_area_in_hecter', project.project__object_size_in_hecter);
//             frm.set_value('total_compleated_work_till_now', project.total_compleated_work_till_now);
//         });
//     }
// });

// // Validate completed area
// function validate_area(frm) {
//     const total_area = frm.doc.total_area_in_hecter || 0;
//     const previous_work = frm.doc.total_compleated_work_till_now || 0;
//     const submission = frm.doc.area_completed_for_this_submission || 0;

//     if(submission + previous_work > total_area) {
//         frappe.msgprint(__('Total completed area cannot exceed project total area.'));
//         frm.set_value('area_completed_for_this_submission', '');
//     }
// }

// // Validate start and end dates
// function validate_date_fields(frm) {
//     if(frm.doc.start_date && frm.doc.end_date) {
//         if(frappe.datetime.get_diff(frm.doc.end_date, frm.doc.start_date) < 0) {
//             frappe.msgprint(__('End Date must be after Start Date'));
//             frm.set_value('end_date', '');
//         }
//     }
// }


















frappe.ui.form.on('Project Attendance', {
    project__client: function(frm) {
        if (frm.is_new()) {
            calculate_total_completed_work(frm);
        }
    },

    validate: function(frm) {
        const total_completed = frm.doc.total_compleated_work_till_now || 0;
        const new_submission = frm.doc.area_completed_for_this_submission || 0;
        const total_allowed = frm.doc.total_area_in_hecter || 0;

        const projected_total = total_completed + new_submission;

        if (projected_total > total_allowed) {
            frappe.throw(__('Total completed area ({0}) cannot exceed allowed area ({1}) in Project Setup.', [projected_total, total_allowed]));
        }
    },

    on_submit: function(frm) {
        update_total_completed_in_project_setup(frm.doc.project__client);
    },

    after_cancel: function(frm) {
        update_total_completed_in_project_setup(frm.doc.project__client);
    }
});

// Calculate total completed work till now for display
function calculate_total_completed_work(frm) {
    if (!frm.doc.project__client) return;

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Project Attendance",
            filters: {
                project__client: frm.doc.project__client,
                docstatus: ["!=", 2]  // Exclude cancelled
            },
            fields: ["area_completed_for_this_submission"]
        },
        callback: function(response) {
            if (response.message && frm.is_new()) {
                let total = response.message.reduce((sum, record) => {
                    return sum + (record.area_completed_for_this_submission || 0);
                }, 0);
                frm.set_value("total_compleated_work_till_now", total);
            }
        }
    });
}

// Update total completed area in Project Setup and status
function update_total_completed_in_project_setup(project_name) {
    if (!project_name) return;

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Project Attendance",
            filters: {
                project__client: project_name,
                docstatus: 1  // Only submitted
            },
            fields: ["area_completed_for_this_submission"]
        },
        callback: function(response) {
            if (response.message) {
                let total = response.message.reduce((sum, record) => {
                    return sum + (record.area_completed_for_this_submission || 0);
                }, 0);

                // First update the total completed work
                frappe.db.set_value("Project Setup", project_name, "total_compleated_work_till_now", total)
                    .then(() => {
                        console.log("Updated Project Setup total completed work:", total);

                        // Now fetch project size to check if work is complete
                        frappe.db.get_value("Project Setup", project_name, "project__object_size_in_hecter")
                            .then(res => {
                                let project_size = res.message.project__object_size_in_hecter || 0;

                                // If completed, update status to Completed
                                if (total >= project_size) {
                                    frappe.db.set_value("Project Setup", project_name, "status", "Completed")
                                        .then(() => {
                                            console.log("Project Setup status updated to Completed.");
                                        });
                                }
                            });
                    });
            }
        }
    });
}








// Update total completed area in Project Setup
function update_total_completed_in_project_setup(project_name) {
    if (!project_name) return;

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Project Attendance",
            filters: {
                project__client: project_name,
                docstatus: 1  // Only submitted
            },
            fields: ["area_completed_for_this_submission"]
        },
        callback: function(response) {
            if (response.message) {
                let total = response.message.reduce((sum, record) => {
                    return sum + (record.area_completed_for_this_submission || 0);
                }, 0);

                // First update total completed work
                frappe.db.set_value("Project Setup", project_name, "total_compleated_work_till_now", total)
                    .then(() => {
                        console.log("Updated Project Setup with new total after submit/cancel:", total);

                        // Now check if project is fully completed
                        frappe.db.get_value("Project Setup", project_name, "project__object_size_in_hecter")
                            .then(r => {
                                const project_size = r.message.project__object_size_in_hecter || 0;

                                if (total >= project_size) {

                                    const today = frappe.datetime.get_today();
                                    const monthIndex = new Date(today).getMonth(); // 0-11
                                    const monthNames = [
                                        "January", "February", "March", "April", "May", "June",
                                        "July", "August", "September", "October", "November", "December"
                                    ];
                                    const currentMonth = monthNames[monthIndex];

                                    // Update status to Completed
                                    frappe.db.set_value("Project Setup", project_name, {
                                        status: "Completed",
                                        completion_date: today,
                                        completion_month: currentMonth
                                    }).then(() => {
                                            console.log("Project Setup marked as Completed");
                                        });
                                }
                            });
                    });
            }
        }
    });
}


