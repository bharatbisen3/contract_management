// frappe.ui.form.on('Time And Daily Allowance', {
//     // Triggered when the Work Team field is changed
//     work_team: function (frm) {
//         if (frm.doc.work_team) {
//             frappe.call({
//                 method: "frappe.client.get",
//                 args: {
//                     doctype: "Work Team",
//                     name: frm.doc.work_team
//                 },
//                 callback: function (response) {
//                     if (response.message) {
//                         let work_team = response.message;

//                         // Check for valid start and end dates
//                         if (frm.doc.start_date && frm.doc.end_date) {
//                             let start_date = new Date(frm.doc.start_date);
//                             let end_date = new Date(frm.doc.end_date);

//                             // Clear existing rows in allowance_details table
//                             frm.clear_table("allowance_details");

//                             // Create a set of employee_id and date combinations from allowance_marked
//                             let marked_combinations = new Set();
//                             if (frm.doc.allowance_marked) {
//                                 frm.doc.allowance_marked.forEach(row => {
//                                     let row_date = new Date(row.date);
//                                     if (row_date >= start_date && row_date <= end_date) {
//                                         marked_combinations.add(`${row.employee_id}-${row.date}`);
//                                     }
//                                 });
//                             }

//                             // Loop through each date in the range
//                             for (let d = new Date(start_date); d <= end_date; d.setDate(d.getDate() + 1)) {
//                                 let current_date = frappe.datetime.obj_to_str(d);

//                                 if (work_team.team_members_list) {
//                                     work_team.team_members_list.forEach(member => {
//                                         // Check if the employee_id and date combination is already marked
//                                         let combination = `${member.employee_id}-${current_date}`;
//                                         let is_marked = marked_combinations.has(combination);

//                                         // Only add if not marked and not already in allowance_details
//                                         if (!is_marked) {
//                                             let exists = frm.doc.allowance_details.some(row =>
//                                                 row.employee_id === member.employee_id &&
//                                                 row.date === current_date
//                                             );

//                                             if (!exists) {
//                                                 let row = frm.add_child("allowance_details");
//                                                 row.employee_id = member.employee_id;
//                                                 row.full_name = member.full_name;
//                                                 row.first_name = member.first_name;
//                                                 row.last_name = member.last_name;
//                                                 row.email = member.email;
//                                                 row.date = current_date;
//                                                 row.present = "";
//                                                 row.allowance = "";
//                                                 row.duration = 8;
//                                             }
//                                         }
//                                     });
//                                 }
//                             }

//                             frm.refresh_field("allowance_details");
//                         }

//                         // Populate team_members table (no clearing)
//                         work_team.team_members_list.forEach(member => {
//                             let exists = frm.doc.team_members.some(row =>
//                                 row.employee_id === member.employee_id
//                             );

//                             if (!exists) {
//                                 let row = frm.add_child("team_members");
//                                 row.employee_id = member.employee_id;
//                                 row.full_name = member.full_name;
//                                 row.first_name = member.first_name;
//                                 row.last_name = member.last_name;
//                                 row.email = member.email;
//                             }
//                         });

//                         frm.refresh_field("team_members");
//                     }
//                 },
//                 error: function () {
//                     frappe.msgprint(__("Error fetching Work Team details. Please try again."));
//                 }
//             });
//         }
//     },

//     // Triggered when the start_date field is changed
//     start_date: function (frm) {
//         frm.trigger('refresh_allowance_marked');
//         frm.trigger('work_team');
//     },

//     // Triggered when the end_date field is changed
//     end_date: function (frm) {
//         frm.trigger('refresh_allowance_marked');
//         frm.trigger('work_team');
//     },

//     // Triggered when the project__client field is changed
//     project__client: function (frm) {
//         frm.trigger('refresh_allowance_marked');
//     },

//     // Function to refresh the allowance_marked table
//     refresh_allowance_marked: function (frm) {
//         if (frm.doc.project__client && frm.doc.start_date && frm.doc.end_date) {
//             let start_date = new Date(frm.doc.start_date);
//             let end_date = new Date(frm.doc.end_date);

//             // Fetch marked attendance records for the matching project and date range
//             frappe.call({
//                 method: "frappe.client.get_list",
//                 args: {
//                     doctype: "Marked Attandance",
//                     filters: {
//                         project: frm.doc.project__client, // Match project with project__client
//                         date: ["between", [frm.doc.start_date, frm.doc.end_date]] // Filter by date range
//                     },
//                     fields: ["employee", "date", "duration", "present", "allowance", "project"]
//                 },
//                 callback: function (response) {
//                     if (response.message) {
//                         let marked_attendances = response.message;

//                         // Clear existing rows in allowance_marked table
//                         frm.clear_table("allowance_marked");

//                         // Populate allowance_marked table with fetched data
//                         marked_attendances.forEach(attendance => {
//                             let row = frm.add_child("allowance_marked");
//                             row.employee_id = attendance.employee;
//                             row.date = attendance.date;
//                             row.duration = attendance.duration;
//                             row.present = attendance.present;
//                             row.allowance = attendance.allowance;
//                             row.project = attendance.project;
//                         });

//                         // Refresh the allowance_marked table to reflect changes
//                         frm.refresh_field("allowance_marked");

//                         // Trigger work_team to update allowance_details based on new marked data
//                         frm.trigger('work_team');
//                     }
//                 },
//                 error: function () {
//                     frappe.msgprint(__("Error fetching Marked Attandance records. Please try again."));
//                 }
//             });
//         }
//     },

//     // Triggered when the document is refreshed
//     refresh: function (frm) {
//         frm.trigger('refresh_allowance_marked');
//     },

//     // Triggered after the document is saved
//     after_save: function (frm) {
//         // Refresh both tables to ensure data is displayed correctly
//         frm.refresh_field("allowance_details");
//         frm.refresh_field("allowance_marked");

//         // Logic to insert data into "Marked Attandance" doctype
//         frappe.call({
//             method: "frappe.client.get",
//             args: {
//                 doctype: "Time And Daily Allowance",
//                 name: frm.doc.name
//             },
//             callback: function (r) {
//                 if (r.message) {
//                     let doc = r.message;

//                     (doc.allowance_details || []).forEach(row => {
//                         if (["Yes", "No"].includes(row.present)) {
//                             frappe.call({
//                                 method: "frappe.client.get_list",
//                                 args: {
//                                     doctype: "Marked Attandance",
//                                     filters: {
//                                         employee: row.employee_id,
//                                         date: row.date
//                                     },
//                                     limit_page_length: 1
//                                 },
//                                 callback: function (res) {
//                                     if (res.message.length === 0) {
//                                         frappe.call({
//                                             method: "frappe.client.insert",
//                                             args: {
//                                                 doc: {
//                                                     doctype: "Marked Attandance",
//                                                     employee: row.employee_id,
//                                                     date: row.date,
//                                                     duration: row.duration,
//                                                     present: row.present,
//                                                     allowance: row.allowance,
//                                                     project: doc.project__client,
//                                                     object: doc.object
//                                                 }
//                                             },
//                                             callback: function (insert_res) {
//                                                 frappe.msgprint(`✅ Attendance Marked for: ${row.employee_id}`);
//                                             }
//                                         });
//                                     } else {
//                                         frappe.msgprint(`⚠️ Entry already exists for ${row.employee_id} on ${row.date} Backend Code`);
//                                     }
//                                 }
//                             });
//                         }
//                     });
//                 }
//             }
//         });
//     },

//     // Triggered when the document is saved
//     save: function (frm) {
//         // Refresh both tables immediately before saving
//         frm.refresh_field("allowance_details");
//         frm.refresh_field("allowance_marked");

//         // Save the document after refreshing the tables
//         frm.save().then(() => {
//             // Show a success message
//             frappe.msgprint(__("Document saved successfully."));
//         }).catch(() => {
//             frappe.msgprint(__("Error saving the document. Please try again."));
//         });
//     },

//     // Triggered when the present field in allowance_details is changed
//     allowance_details_custom_present: function (frm, cdt, cdn) {
//         let row = frappe.get_doc(cdt, cdn);
//         if (row.present === "Yes" || row.present === "No") {
//             // Save the marked attendance in the "Marked Attandance" doctype
//             frappe.call({
//                 method: "frappe.client.insert",
//                 args: {
//                     doc: {
//                         doctype: "Marked Attandance",
//                         employee: row.employee_id,
//                         date: row.date,
//                         duration: row.duration,
//                         present: row.present,
//                         allowance: row.allowance,
//                         project: frm.doc.project__client
//                     }
//                 },
//                 callback: function (response) {
//                     if (response.message) {
//                         // Add the marked attendance to the "allowance_marked" table
//                         let marked_row = frm.add_child("allowance_marked");
//                         marked_row.employee_id = row.employee_id;
//                         marked_row.date = row.date;
//                         marked_row.duration = row.duration;
//                         marked_row.present = row.present;
//                         marked_row.allowance = row.allowance;
//                         marked_row.project = frm.doc.project__client;

//                         // Remove the row from the "allowance_details" table
//                         frm.remove_from_child_table("allowance_details", row.name);

//                         // Refresh both tables
//                         frm.refresh_field("allowance_details");
//                         frm.refresh_field("allowance_marked");

//                         // Save the document immediately
//                         frm.save();
//                     }
//                 },
//                 error: function () {
//                     frappe.msgprint(__("Error saving Marked Attandance. Please try again."));
//                 }
//             });
//         }
//     }
// });