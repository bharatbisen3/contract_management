// // // // Copyright (c) 2025, bharat and contributors
// // // // For license information, please see license.txt

// // // // frappe.ui.form.on("Total Compensation", {
// // // // 	refresh(frm) {

// // // // 	},
// // // // });

// // // Copyright (c) 2025, bharat and contributors
// // // For license information, please see license.txt

// // // frappe.ui.form.on("Total Compensation", {
// // // 	refresh(frm) {

// // // 	},
// // // });

// // frappe.ui.form.on("Total Compensation", {
// //   refresh(frm) {
// //     // Always show these sections if data already exists
// //     if ((frm.doc.object_list || []).length > 0) {
// //       frm.set_df_property("obj_list_section_section", "hidden", 0);
// //       frm.set_df_property("section_break_qjwb", "hidden", 0); // for Calculate button section
// //     }

// //     if ((frm.doc.not_even_distribution || []).length > 0) {
// //       frm.set_df_property(
// //         "objects_with_not_even_distribution_section",
// //         "hidden",
// //         0
// //       );
// //     }

// //     if ((frm.doc.employee_compensation_list || []).length > 0) {
// //       frm.set_df_property(
// //         "detailed_emp_compensation_list_section",
// //         "hidden",
// //         0
// //       );
// //     }

// //     if ((frm.doc.employee_compensetion_summery || []).length > 0) {
// //       frm.set_df_property("section_break_xkna", "hidden", 0);
// //     }

// //     frm.refresh_fields();
// //   },

// //   month: function (frm) {
// //     if (frm.doc.month) {
// //       frm.set_df_property("obj_list_section_section", "hidden", 0);
// //     }
// //     populate_object_list(frm);
// //     frm.refresh_fields();
// //   },

// //   get_members: function (frm) {
// //     const objectList = frm.doc.object_list || [];
// //     const hasNotEven = objectList.some(
// //       (row) => row.completion_type === "Not Even"
// //     );

// //     if (objectList.length > 0) {
// //       // Show section for Calculate button
// //       frm.set_df_property("section_break_qjwb", "hidden", 0);
// //     }

// //     // Show Not Even section only if applicable
// //     frm.set_df_property(
// //       "objects_with_not_even_distribution_section",
// //       "hidden",
// //       !hasNotEven
// //     );

// //     // Execute the get members functionality
// //     get_team_members(frm);

// //     // Also execute the original get_members logic for not even distribution
// //     frm.clear_table("not_even_distribution");

// //     // Loop through each object
// //     (frm.doc.object_list || []).forEach((obj) => {
// //       if (!obj.object || obj.completion_type !== "Not Even") return;

// //       // Fetch object to get work_team
// //       frappe.db.get_doc("Project Setup", obj.object).then((project_setup) => {
// //         const work_team = project_setup.work_team;

// //         if (!work_team) return;

// //         // Fetch team members
// //         frappe.db.get_doc("Work Team", work_team).then((team) => {
// //           (team.team_members_list || []).forEach((member) => {
// //             frm.add_child("not_even_distribution", {
// //               employee: member.employee_id,
// //               object: obj.object,
// //               object_title: obj.object_title,
// //               task: obj.task,
// //             });
// //             frm.refresh_field("not_even_distribution");
// //           });
// //         });
// //       });
// //     });

// //     frappe.show_alert("Members loaded for Not Even distribution");
// //     frm.refresh_fields();
// //   },

// //   // calculate: function(frm) {
// //   //     // Calculate compensation when Calculate button is clicked
// //   //     calculate_compensation(frm);
// //   //     frm.set_df_property('detailed_emp_compensation_list_section', 'hidden', 0);

// //   //     setTimeout(function() {
// //   //         frm.trigger("summery_of_employee");
// //   //         frm.refresh_fields();
// //   //     }, 2000);
// //   // },

// //   calculate: function (frm) {
// //     // First validate not even distribution percentages
// //     let not_even_objects = frm.doc.not_even_distribution || [];
// //     let object_percentages = {};

// //     // Group by object and sum percentages
// //     not_even_objects.forEach((obj) => {
// //       if (obj.object && obj.percentage) {
// //         if (!object_percentages[obj.object]) {
// //           object_percentages[obj.object] = 0;
// //         }
// //         object_percentages[obj.object] += obj.percentage;
// //       }
// //     });

// //     // Check if any object has percentage != 100%
// //     let hasError = false;
// //     for (let object in object_percentages) {
// //       if (Math.abs(object_percentages[object] - 100) > 0.01) {
// //         hasError = true;
// //         frappe.msgprint(
// //           __(
// //             "Total percentage for object {0} should be 100%. Current total: {1}%",
// //             [object, object_percentages[object].toFixed(2)]
// //           )
// //         );
// //       }
// //     }

// //     // If there are percentage errors, stop calculation
// //     if (hasError) {
// //       frappe.msgprint(
// //         __(
// //           "Please fix percentage distribution errors before calculating compensation."
// //         )
// //       );
// //       return;
// //     }

// //     // If no errors, proceed with calculation
// //     calculate_compensation(frm);
// //     frm.set_df_property("detailed_emp_compensation_list_section", "hidden", 0);

// //     setTimeout(function () {
// //       frm.trigger("summery_of_employee");
// //       frm.refresh_fields();

// //       setTimeout(function () {
// //         frm.trigger("generate_net_compensation");
// //         frm.refresh_fields();
// //       }, 2000);

// //     }, 2000);

// //   },

// //   summery_of_employee: function (frm) {
// //     const summaryMap = {};

// //     // Step 1: Loop through each row in employee_compensation_list
// //     (frm.doc.employee_compensation_list || []).forEach((row) => {
// //       if (!row.employee) return;

// //       const empId = row.employee;
// //       const empName = row.employee_name || "";
// //       const task = (row.task || "").trim();
// //       const compensation = flt(row.compensation || 0);

// //       if (!summaryMap[empId]) {
// //         summaryMap[empId] = {
// //           employee_id: empId,
// //           employee_name: empName,
// //           clearing_compensation: 0,
// //           planting_compensation: 0,
// //         };
// //       }

// //       if (task === "Forest Clearing") {
// //         summaryMap[empId].clearing_compensation += compensation;
// //       } else if (task === "Forest Planting") {
// //         summaryMap[empId].planting_compensation += compensation;
// //       }
// //     });

// //     // Step 2: Clear existing rows in employee_compensetion_summery
// //     frm.clear_table("employee_compensetion_summery");

// //     // Step 3: Add new rows to the summary table
// //     Object.values(summaryMap).forEach((entry) => {
// //       const newRow = frm.add_child("employee_compensetion_summery");
// //       newRow.employee_id = entry.employee_id;
// //       newRow.employee_name = entry.employee_name;
// //       newRow.clearing_compensation = entry.clearing_compensation;
// //       newRow.planting_compensation = entry.planting_compensation;
// //     });

// //     frm.refresh_field("employee_compensetion_summery");
// //     frm.set_df_property("section_break_xkna", "hidden", 0);

// //     frappe.msgprint("Summary table has been updated successfully.");
// //     frm.refresh_fields();
// //   },

// //   // validate: function(frm) {
// //   //     // Validate not even distribution percentages
// //   //     let not_even_objects = frm.doc.not_even_distribution || [];
// //   //     let object_percentages = {};

// //   //     // Group by object and sum percentages
// //   //     not_even_objects.forEach(obj => {
// //   //         if (obj.object && obj.percentage) {
// //   //             if (!object_percentages[obj.object]) {
// //   //                 object_percentages[obj.object] = 0;
// //   //             }
// //   //             object_percentages[obj.object] += obj.percentage;
// //   //         }
// //   //     });

// //   //     // Check if any object has percentage != 100%
// //   //     for (let object in object_percentages) {
// //   //         if (Math.abs(object_percentages[object] - 100) > 0.01) {
// //   //             frappe.validated = false;
// //   //             frappe.msgprint(__('Total percentage for object {0} should be 100%. Current total: {1}%',
// //   //                 [object, object_percentages[object]]));
// //   //             return;
// //   //         }
// //   //     }
// //   // }

// //   generate_net_compensation: async function (frm) {
// //     if (!(frm.doc.year && frm.doc.month)) {
// //       frappe.msgprint(
// //         "Please set Fiscal Year and Month before generating Net Compensation."
// //       );
// //       return;
// //     }

// //     // Clear table before regeneration
// //     frm.clear_table("net_compensation");

// //     // Loop over summary employees
// //     for (let row of frm.doc.employee_compensetion_summery || []) {
// //       let emp = row.employee_id;

// //       // Fetch attendance + piecework data from backend
// //       let r = await frappe.call({
// //         method:
// //           "contract_management.contract_management.doctype.net_compensation.net_compensation.get_employee_attendance",
// //         args: {
// //           employee: emp,
// //           month: frm.doc.month,
// //           year: frm.doc.year,
// //         },
// //       });

// //       let data = r.message || {};

// //       // 🧮 Perform calculations (JS version of your Python formulas)
// //       let attendance = data.attendance || 0;
// //       let total_hours = data.total_hours || 0;
// //       let daily_allowance_rate = data.daily_allowance_rate || 0;
// //       let daily_allowance_total = attendance * daily_allowance_rate;

// //       let piecework = data.piecework_compensation || 0;

// //       let holiday_comp = piecework * 0.13;
// //       let reduction_hours = piecework * 0.0362;

// //       let gross_salary = piecework + holiday_comp + reduction_hours;
// //       let tax_percentage = 30;
// //       let tax_amount = (gross_salary * tax_percentage) / 100;

// //       let net_excl_allowance = gross_salary - tax_amount;
// //       let total_net = net_excl_allowance + daily_allowance_total;

// //       // Append to child table
// //       let child = frm.add_child("net_compensation");
// //       child.employee = emp;
// //       child.attendance = attendance;
// //       child.total_hours = total_hours;
// //       child.daily_allowance_rate_sek = daily_allowance_rate;
// //       child.daily_allowance_total_sek = daily_allowance_total;
// //       child.piecework_compensation = piecework;
// //       child.holiday_compensation_13 = holiday_comp;
// //       child.reduction_in_working_hours_362 = reduction_hours;
// //       child.gross_salary_total = gross_salary;
// //       child.tax_percentage = tax_percentage;
// //       child.tax_amount = tax_amount;
// //       child.net_compensation_excluding_daily_allowance = net_excl_allowance;
// //       child.total_net_compensation = total_net;
// //     }

// //     frm.refresh_field("net_compensation");
// //     frappe.msgprint("Net Compensation calculated instantly (JS)");
// //   },

// // });

// // function populate_object_list(frm) {
// //   let work_team = frm.doc.work_team;
// //   let month = frm.doc.month;

// //   if (!work_team) return;

// //   // Optional message
// //   // frappe.msgprint(`Loading objects for Work Team: ${work_team} for ${month} Month`);

// //   frm.clear_table("object_list");

// //   frappe.call({
// //     method: "frappe.client.get_list",
// //     args: {
// //       doctype: "Project Setup",
// //       filters: {
// //         work_team: work_team,
// //         status: "Completed",
// //         completion_month: month,
// //       },
// //       fields: [
// //         "name",
// //         "object_title",
// //         "task",
// //         "distribution_type",
// //         "sla_class",
// //         "project__object_size_in_hecter",
// //         "completion_date",
// //         "clearing_cost",
// //         "planting_cost",
// //         "completion_month",
// //       ],
// //       limit_page_length: 100,
// //     },
// //     callback: function (r) {
// //       if (!r.message) return;

// //       r.message.forEach((project) => {
// //         let total_comp = 0;
// //         if (project.task === "Forest Clearing") {
// //           total_comp = parseFloat(project.clearing_cost || 0);
// //         } else if (project.task === "Forest Planting") {
// //           total_comp = parseFloat(project.planting_cost || 0);
// //         }

// //         frm.add_child("object_list", {
// //           object: project.name,
// //           object_title: project.object_title,
// //           // task: project.task === "Forest Clearing" ? "Clearing" : "Planting",
// //           task: project.task,
// //           completion_type: project.distribution_type,
// //           sla_class: project.sla_class,
// //           quantity_hectare_or_plants: project.project__object_size_in_hecter,
// //           completion_date: project.completion_date,
// //           total_compensation: total_comp,
// //         });
// //       });

// //       frm.refresh_field("object_list");

// //       // Show the object list section and calculate button section if data exists
// //       if ((frm.doc.object_list || []).length > 0) {
// //         frm.set_df_property("obj_list_section_section", "hidden", 0);
// //         frm.set_df_property("section_break_qjwb", "hidden", 0);
// //       }
// //       frm.refresh_fields();
// //     },
// //   });
// // }

// // function calculate_compensation(frm) {
// //   // Clear existing data in employee_compensation_list
// //   frm.clear_table("employee_compensation_list");

// //   // Get all completed objects
// //   let objects = frm.doc.object_list || [];
// //   let not_even_objects = frm.doc.not_even_distribution || [];

// //   if (objects.length === 0) {
// //     frappe.msgprint(
// //       __("No completed objects found to calculate compensation.")
// //     );
// //     return;
// //   }

// //   // Get team members first, then process compensation
// //   get_team_members_for_calculation(frm).then((team_members) => {
// //     if (!team_members || team_members.length === 0) {
// //       frappe.msgprint(
// //         __('No team members found. Please use "Get Members" button first.')
// //       );
// //       return;
// //     }

// //     let employee_compensation = [];

// //     // Process each completed object
// //     objects.forEach((obj) => {
// //       if (!obj.object || !obj.total_compensation) return;

// //       // Check if this object has not even distribution
// //       let object_not_even = not_even_objects.filter(
// //         (ne) => ne.object === obj.object
// //       );

// //       if (obj.completion_type === "Not Even" && object_not_even.length > 0) {
// //         // Process not even distribution
// //         object_not_even.forEach((ne_obj) => {
// //           if (ne_obj.employee && ne_obj.percentage) {
// //             employee_compensation.push({
// //               employee: ne_obj.employee,
// //               object: obj.object,
// //               object_title: obj.object_title,
// //               task: obj.task,
// //               percentage: ne_obj.percentage,
// //               compensation: (obj.total_compensation * ne_obj.percentage) / 100,
// //             });
// //           }
// //         });
// //       } else if (obj.completion_type === "Even") {
// //         // Process even distribution
// //         let even_percentage = 100 / team_members.length;

// //         team_members.forEach((member) => {
// //           employee_compensation.push({
// //             employee: member,
// //             object: obj.object,
// //             object_title: obj.object_title,
// //             task: obj.task,
// //             percentage: even_percentage,
// //             compensation: (obj.total_compensation * even_percentage) / 100,
// //           });
// //         });
// //       }
// //     });

// //     // Add all calculated compensation to the table
// //     employee_compensation.forEach((ec) => {
// //       let row = frm.add_child("employee_compensation_list");
// //       row.employee = ec.employee;
// //       row.object = ec.object;
// //       row.object_title = ec.object_title;
// //       row.task = ec.task;
// //       row.percentage = ec.percentage;
// //       row.compensation = ec.compensation;
// //     });

// //     frm.refresh_field("employee_compensation_list");

// //     // Show the detailed compensation section if data exists
// //     if ((frm.doc.employee_compensation_list || []).length > 0) {
// //       frm.set_df_property(
// //         "detailed_emp_compensation_list_section",
// //         "hidden",
// //         0
// //       );
// //     }

// //     frappe.msgprint(
// //       __("Compensation calculated successfully for {0} records.", [
// //         employee_compensation.length,
// //       ])
// //     );
// //     frm.refresh_fields();
// //   });
// // }

// // function get_team_members(frm) {
// //   if (!frm.doc.work_team) {
// //     frappe.msgprint(__("Please select a Work Team first."));
// //     return;
// //   }

// //   frappe.call({
// //     method: "frappe.client.get",
// //     args: {
// //       doctype: "Work Team",
// //       name: frm.doc.work_team,
// //     },
// //     callback: function (r) {
// //       if (r.message && r.message.team_members_list) {
// //         // Clear existing not_even_distribution entries
// //         frm.clear_table("not_even_distribution");

// //         // Add team members to not_even_distribution table for manual percentage entry
// //         r.message.team_members_list.forEach((member) => {
// //           // You can optionally populate the not_even_distribution table here
// //           // if you want to show all members for percentage entry
// //         });

// //         frm.refresh_field("not_even_distribution");
// //         // frappe.msgprint(__('Team members loaded successfully.'));
// //       } else {
// //         frappe.msgprint(
// //           __("No team members found for the selected work team.")
// //         );
// //       }
// //     },
// //   });
// // }

// // function get_team_members_for_calculation(frm) {
// //   return new Promise((resolve, reject) => {
// //     if (!frm.doc.work_team) {
// //       resolve([]);
// //       return;
// //     }

// //     frappe.call({
// //       method: "frappe.client.get",
// //       args: {
// //         doctype: "Work Team",
// //         name: frm.doc.work_team,
// //       },
// //       callback: function (r) {
// //         if (r.message && r.message.team_members_list) {
// //           let team_members = r.message.team_members_list.map(
// //             (m) => m.employee_id
// //           );
// //           resolve(team_members);
// //         } else {
// //           resolve([]);
// //         }
// //       },
// //       error: function (r) {
// //         reject(r);
// //       },
// //     });
// //   });
// // }

// // 🔹 Helper: Client-side equivalent of get_employee_attendance
// async function get_employee_attendance_js(employee, month, year) {
//   if (!employee || !month || !year) return {};

//   // Month name → number
//   const months = [
//     "January",
//     "February",
//     "March",
//     "April",
//     "May",
//     "June",
//     "July",
//     "August",
//     "September",
//     "October",
//     "November",
//     "December",
//   ];
//   let monthNum = months.indexOf(month) + 1;
//   if (monthNum === 0) return {};

//   // Fiscal year handling
//   let [startYear, endYear] = year.split("-").map((y) => parseInt(y));
//   let actualYear = monthNum >= 4 ? startYear : endYear;

//   // from_date and to_date
//   let from_date = `${actualYear}-${String(monthNum).padStart(2, "0")}-01`;
//   let to_date = new Date(actualYear, monthNum, 0);
//   let to_date_str = `${to_date.getFullYear()}-${String(
//     to_date.getMonth() + 1
//   ).padStart(2, "0")}-${String(to_date.getDate()).padStart(2, "0")}`;

//   // Query attendance directly
//   let res = await frappe.db.get_list("Employee Attendance Master", {
//     filters: {
//       employee: employee,
//       date: ["between", [from_date, to_date_str]],
//     },
//     fields: [
//       "employee",
//       "full_name",
//       "date",
//       "duration",
//       "present",
//       "allowance",
//       "project",
//       "project_name",
//       "team_leader",
//       "tl_name",
//     ],
//     order_by: "date asc",
//     limit: 500,
//   });

//   if (!res || !res.length)
//     return {
//       attendance: 0,
//       total_hours: 0,
//       allowance_days: 0,
//       daily_allowance_rate: 0,
//       piecework_compensation: 0,
//     };

//   // Summarize
//   let total_days = 0,
//     total_hours = 0,
//     allowance_days = 0;
//   res.forEach((r) => {
//     r.present = r.present === "Yes" ? 1 : 0;
//     r.allowance = r.allowance === "Yes" ? 1 : 0;
//     r.duration = parseInt(r.duration || 0);

//     if (r.present) total_days += 1;
//     if (r.allowance) allowance_days += 1;
//     total_hours += r.duration;
//   });

//   return {
//     records: res,
//     attendance: total_days,
//     total_hours: total_hours,
//     allowance_days: allowance_days,
//     daily_allowance_rate: 0, // placeholder
//     piecework_compensation: 0,
//   };
// }

// // Copyright (c) 2025, bharat and contributors
// // For license information, please see license.txt

// // frappe.ui.form.on("Total Compensation", {
// // 	refresh(frm) {

// // 	},
// // });

// frappe.ui.form.on("Total Compensation", {
//   refresh(frm) {
//     // Always show these sections if data already exists
//     if ((frm.doc.object_list || []).length > 0) {
//       frm.set_df_property("obj_list_section_section", "hidden", 0);
//       frm.set_df_property("section_break_qjwb", "hidden", 0); // for Calculate button section
//     }

//     if ((frm.doc.not_even_distribution || []).length > 0) {
//       frm.set_df_property(
//         "objects_with_not_even_distribution_section",
//         "hidden",
//         0
//       );
//     }

//     if ((frm.doc.employee_compensation_list || []).length > 0) {
//       frm.set_df_property(
//         "detailed_emp_compensation_list_section",
//         "hidden",
//         0
//       );
//     }

//     if ((frm.doc.employee_compensetion_summery || []).length > 0) {
//       frm.set_df_property("section_break_xkna", "hidden", 0);
//     }

//     frm.refresh_fields();
//   },

//   // month: function (frm) {
//   //   if (!work_team || !year) return;
//   //   populate_object_list(frm);

//   //   // if (frm.doc.month) {
//   //   //   frm.set_df_property("obj_list_section_section", "hidden", 0);
//   //   // }
//   //   // populate_object_list(frm);
//   //   // frm.refresh_fields();
//   // },

//   month: function (frm) {
//     populate_object_list(frm);
//   },
//   year: function (frm) {
//     // trigger when fiscal year changes
//     populate_object_list(frm);
//   },

//   get_members: function (frm) {
//     const objectList = frm.doc.object_list || [];
//     const hasNotEven = objectList.some(
//       (row) => row.completion_type === "Not Even"
//     );

//     if (objectList.length > 0) {
//       // Show section for Calculate button
//       frm.set_df_property("section_break_qjwb", "hidden", 0);
//     }

//     // Show Not Even section only if applicable
//     frm.set_df_property(
//       "objects_with_not_even_distribution_section",
//       "hidden",
//       !hasNotEven
//     );

//     // Execute the get members functionality
//     get_team_members(frm);

//     // Also execute the original get_members logic for not even distribution
//     frm.clear_table("not_even_distribution");

//     // Loop through each object
//     (frm.doc.object_list || []).forEach((obj) => {
//       if (!obj.object || obj.completion_type !== "Not Even") return;

//       // Fetch object to get work_team
//       frappe.db.get_doc("Project Setup", obj.object).then((project_setup) => {
//         const work_team = project_setup.work_team;

//         if (!work_team) return;

//         // Fetch team members
//         frappe.db.get_doc("Work Team", work_team).then((team) => {
//           (team.team_members_list || []).forEach((member) => {
//             frm.add_child("not_even_distribution", {
//               employee: member.employee_id,
//               object: obj.object,
//               object_title: obj.object_title,
//               task: obj.task,
//             });
//             frm.refresh_field("not_even_distribution");
//           });
//         });
//       });
//     });

//     frappe.show_alert("Members loaded for Not Even distribution");
//     frm.refresh_fields();
//   },

//   // calculate: function(frm) {
//   //     // Calculate compensation when Calculate button is clicked
//   //     calculate_compensation(frm);
//   //     frm.set_df_property('detailed_emp_compensation_list_section', 'hidden', 0);

//   //     setTimeout(function() {
//   //         frm.trigger("summery_of_employee");
//   //         frm.refresh_fields();
//   //     }, 2000);
//   // },

//   calculate: function (frm) {
//     // First validate not even distribution percentages
//     let not_even_objects = frm.doc.not_even_distribution || [];
//     let object_percentages = {};

//     // Group by object and sum percentages
//     not_even_objects.forEach((obj) => {
//       if (obj.object && obj.percentage) {
//         if (!object_percentages[obj.object]) {
//           object_percentages[obj.object] = 0;
//         }
//         object_percentages[obj.object] += obj.percentage;
//       }
//     });

//     // Check if any object has percentage != 100%
//     let hasError = false;
//     for (let object in object_percentages) {
//       if (Math.abs(object_percentages[object] - 100) > 0.01) {
//         hasError = true;
//         frappe.msgprint(
//           __(
//             "Total percentage for object {0} should be 100%. Current total: {1}%",
//             [object, object_percentages[object].toFixed(2)]
//           )
//         );
//       }
//     }

//     // If there are percentage errors, stop calculation
//     if (hasError) {
//       frappe.msgprint(
//         __(
//           "Please fix percentage distribution errors before calculating compensation."
//         )
//       );
//       return;
//     }

//     // If no errors, proceed with calculation
//     calculate_compensation(frm);
//     frm.set_df_property("detailed_emp_compensation_list_section", "hidden", 0);

//     setTimeout(function () {
//       frm.trigger("summery_of_employee");
//       frm.refresh_fields();

//       setTimeout(function () {
//         frm.trigger("generate_net_compensation");
//         frm.refresh_fields();
//       }, 2000);
//     }, 2000);
//   },

//   summery_of_employee: function (frm) {
//     const summaryMap = {};

//     // Step 1: Loop through each row in employee_compensation_list
//     (frm.doc.employee_compensation_list || []).forEach((row) => {
//       if (!row.employee) return;

//       const empId = row.employee;
//       const empName = row.employee_name || "";
//       const task = (row.task || "").trim();
//       const compensation = flt(row.compensation || 0);

//       if (!summaryMap[empId]) {
//         summaryMap[empId] = {
//           employee_id: empId,
//           employee_name: empName,
//           clearing_compensation: 0,
//           planting_compensation: 0,
//         };
//       }

//       if (task === "Forest Clearing") {
//         summaryMap[empId].clearing_compensation += compensation;
//       } else if (task === "Forest Planting") {
//         summaryMap[empId].planting_compensation += compensation;
//       }
//     });

//     // Step 2: Clear existing rows in employee_compensetion_summery
//     frm.clear_table("employee_compensetion_summery");

//     // Step 3: Add new rows to the summary table
//     Object.values(summaryMap).forEach((entry) => {
//       const newRow = frm.add_child("employee_compensetion_summery");
//       newRow.employee_id = entry.employee_id;
//       newRow.employee_name = entry.employee_name;
//       newRow.clearing_compensation = entry.clearing_compensation;
//       newRow.planting_compensation = entry.planting_compensation;
//     });

//     frm.refresh_field("employee_compensetion_summery");
//     frm.set_df_property("section_break_xkna", "hidden", 0);

//     frappe.msgprint("Summary table has been updated successfully.");
//     frm.refresh_fields();
//   },

//   // generate_net_compensation: async function (frm) {
//   //   debugger;
//   //   if (!(frm.doc.year && frm.doc.month)) {
//   //     frappe.msgprint(
//   //       "Please set Fiscal Year and Month before generating Net Compensation."
//   //     );
//   //     return;
//   //   }

//   //   frm.clear_table("net_compensation");

//   //   for (let row of frm.doc.employee_compensetion_summery || []) {
//   //     let emp = row.employee_id;

//   //     // 1️⃣ Get attendance + piecework data
//   //     let r = await frappe.call({
//   //       method:
//   //         "contract_management.contract_management.doctype.net_compensation.net_compensation.get_employee_attendance",
//   //       args: { employee: emp, month: frm.doc.month, year: frm.doc.year },
//   //     });
//   //     let data = r.message || {};

//   //     // 2️⃣ Get employee info (for tax fields)
//   //     let empDoc = await frappe.db.get_doc("Employee", emp);

//   //     // Base salary calculations
//   //     let attendance = data.attendance || 0;
//   //     let total_hours = data.total_hours || 0;
//   //     let daily_allowance_rate = data.daily_allowance_rate || 0;
//   //     let daily_allowance_total = attendance * daily_allowance_rate;

//   //     let piecework = data.piecework_compensation || 0;
//   //     let holiday_comp = piecework * 0.13;
//   //     let reduction_hours = piecework * 0.0362;
//   //     let gross_salary = piecework + holiday_comp + reduction_hours;

//   //     // Tax fields (defaults)
//   //     let tax_table = empDoc.custom_tax_table || null;
//   //     let tax_column = empDoc.custom_tax_column || null;
//   //     let sink_tax = empDoc.custom_sink_tax || 0;
//   //     let tax_relief = empDoc.custom_tax_adjustment__tax_relief || null;

//   //     let tax_percentage = null;
//   //     let tax_amount = 0;

//   //     // 3️⃣ Tax logic
//   //     if (sink_tax) {
//   //       // If sink tax TRUE → 25%
//   //       tax_percentage = 25;
//   //       tax_amount = gross_salary * 0.25;
//   //     } else if (tax_table && tax_column) {
//   //       // Use Tax Table Monthly Salary
//   //       let taxRows = await frappe.db.get_list("Tax Table Monthly Salary", {
//   //         filters: { table: tax_table },
//   //         fields: ["inkomst_from", "inkomst_tom", `Column 1`, `Column 2`, `Column 3`, `Column 4`, `Column 5`, `Column 6`],
//   //         limit_page_length: 1000,
//   //       });

//   //       console.log(taxRows);

//   //       let matched = taxRows.find(
//   //         (row) =>
//   //           gross_salary >= (row.inkomst_from) &&
//   //           gross_salary <= (row.inkomst_tom)
//   //       );

//   //       console.log(matched)

//   //       if (matched) {
//   //         tax_amount = matched[`${tax_column}`] || 0;
//   //         tax_percentage = null; // we don’t use %
//   //       } else {
//   //         // fallback → tax relief or 25%
//   //         tax_percentage = tax_relief || 25;
//   //         tax_amount = (gross_salary * tax_percentage) / 100;
//   //       }
//   //     } else if (tax_relief) {
//   //       // If no table/column, use relief
//   //       tax_percentage = tax_relief;
//   //       tax_amount = (gross_salary * tax_percentage) / 100;
//   //     } else {
//   //       // Final fallback → 25%
//   //       tax_percentage = 25;
//   //       tax_amount = gross_salary * 0.25;
//   //     }

//   //     // 4️⃣ Net salary
//   //     let net_excl_allowance = gross_salary - tax_amount;
//   //     let total_net = net_excl_allowance + daily_allowance_total;

//   //     // 5️⃣ Add row
//   //     let child = frm.add_child("net_compensation");
//   //     child.employee = emp;
//   //     child.attendance = attendance;
//   //     child.total_hours = total_hours;
//   //     child.daily_allowance_rate_sek = daily_allowance_rate;
//   //     child.daily_allowance_total_sek = daily_allowance_total;
//   //     child.piecework_compensation = piecework;
//   //     child.holiday_compensation_13 = holiday_comp;
//   //     child.reduction_in_working_hours_362 = reduction_hours;
//   //     child.gross_salary_total = gross_salary;

//   //     child.tax_table = tax_table;
//   //     child.tax_column = tax_column;
//   //     child.tax_percentage = tax_percentage;
//   //     child.tax_amount = tax_amount;

//   //     child.net_compensation_excluding_daily_allowance = net_excl_allowance;
//   //     child.total_net_compensation = total_net;
//   //   }

//   //   frm.refresh_field("net_compensation");
//   //   frappe.msgprint("Net Compensation recalculated with updated Tax rules.");
//   // },

// generate_net_compensation: async function (frm) {
//   debugger;
//     if (!(frm.doc.year && frm.doc.month)) {
//         frappe.msgprint(
//             "Please set Fiscal Year and Month before generating Net Compensation."
//         );
//         return;
//     }

//     frm.clear_table("net_compensation");

//     for (let row of frm.doc.employee_compensetion_summery || []) {
//         let emp = row.employee_id;

//         // 1️⃣ Get attendance + piecework data
//         let r = await frappe.call({
//             method:
//                 "contract_management.contract_management.doctype.net_compensation.net_compensation.get_employee_attendance",
//             args: { employee: emp, month: frm.doc.month, year: frm.doc.year },
//         });
//         let data = r.message || {};

//         // 2️⃣ Get employee info (for tax fields)
//         let empDoc = await frappe.db.get_doc("Employee", emp);

//         // Base salary calculations
//         let attendance = data.attendance || 0;
//         let total_hours = data.total_hours || 0;
//         let daily_allowance_rate = data.daily_allowance_rate || 0;
//         let daily_allowance_total = attendance * daily_allowance_rate;

//         let piecework = data.piecework_compensation || 0;
//         let holiday_comp = piecework * 0.13;
//         let reduction_hours = piecework * 0.0362;
//         let gross_salary = piecework + holiday_comp + reduction_hours;

//         // Tax fields (defaults)
//         let tax_table = empDoc.custom_tax_table || null;
//         let tax_column = empDoc.custom_tax_column || null;
//         let sink_tax = empDoc.custom_sink_tax || 0;
//         let tax_relief = empDoc.custom_tax_adjustment__tax_relief || null;

//         let tax_percentage = null;
//         let tax_amount = 0;

//         // 3️⃣ Tax logic
//         if (sink_tax) {
//             // If sink tax TRUE → 25%
//             tax_percentage = 25;
//             tax_amount = gross_salary * 0.25;
//         } else if (tax_table && tax_column) {
//             // Use Tax Table Monthly Salary
//             let taxRows = await frappe.db.get_list("Tax Table Monthly Salary", {
//                 filters: {
//                     table: parseInt(tax_table)
//                 },
//                 fields: ["inkomst_from", "inkomst_tom", "column_1", "column_2", "column_3", "column_4", "column_5", "column_6"],
//             });

//             console.log("Tax table rows found:", taxRows.length);
//             console.log("Looking for table:", tax_table, "column:", tax_column);
//             console.log("Gross salary:", gross_salary);

//             // Find the row where gross_salary falls within the range
//             let matchedRow = null;

//             for (let row of taxRows) {
//                 let inkomst_tom = row.inkomst_tom || Infinity;
//                 console.log(`Checking range: ${row.inkomst_from} to ${inkomst_tom}`);

//                 if (gross_salary >= row.inkomst_from && gross_salary <= inkomst_tom) {
//                     matchedRow = row;
//                     console.log("Matched row found:", matchedRow);
//                     break;
//                 }
//             }

//             if (matchedRow) {
//                 // Get the column value based on tax_column
//                 // Handle different formats of tax_column (could be "Column 1", "1", "column_1", etc.)
//                 let columnValue = 0;

//                 // Clean the tax_column value
//                 let cleanTaxColumn = tax_column.toString().toLowerCase().replace(/\s+/g, '').replace('column', '');

//                 // Extract just the number
//                 let columnNumber = parseInt(cleanTaxColumn.replace(/\D/g, '')) || 1;

//                 // Ensure column number is between 1-6
//                 columnNumber = Math.max(1, Math.min(6, columnNumber));

//                 // Map to actual field name
//                 let columnField = "column_" + columnNumber;
//                 columnValue = matchedRow[columnField] || 0;

//                 tax_amount = columnValue;
//                 tax_percentage = null; // we don't use % when using tax table

//                 console.log(`Tax calculation: Table ${tax_table}, Column ${tax_column} -> ${columnField}, Gross Salary: ${gross_salary}, Tax Amount: ${tax_amount}`);
//             } else {
//                 // fallback → tax relief or 25%
//                 tax_percentage = tax_relief || 25;
//                 tax_amount = (gross_salary * tax_percentage) / 100;
//                 console.log(`No matching tax row found. Using fallback tax percentage: ${tax_percentage}%`);
//             }
//         } else if (tax_relief) {
//             // If no table/column, use relief
//             tax_percentage = tax_relief;
//             tax_amount = (gross_salary * tax_percentage) / 100;
//         } else {
//             // Final fallback → 25%
//             tax_percentage = 25;
//             tax_amount = gross_salary * 0.25;
//         }

//         // 4️⃣ Net salary
//         let net_excl_allowance = gross_salary - tax_amount;
//         let total_net = net_excl_allowance + daily_allowance_total;

//         // 5️⃣ Add row
//         let child = frm.add_child("net_compensation");
//         child.employee = emp;
//         child.attendance = attendance;
//         child.total_hours = total_hours;
//         child.daily_allowance_rate_sek = daily_allowance_rate;
//         child.daily_allowance_total_sek = daily_allowance_total;
//         child.piecework_compensation = piecework;
//         child.holiday_compensation_13 = holiday_comp;
//         child.reduction_in_working_hours_362 = reduction_hours;
//         child.gross_salary_total = gross_salary;

//         child.tax_table = tax_table;
//         child.tax_column = tax_column;
//         child.tax_percentage = tax_percentage;
//         child.tax_amount = tax_amount;

//         child.net_compensation_excluding_daily_allowance = net_excl_allowance;
//         child.total_net_compensation = total_net;
//     }

//     frm.refresh_field("net_compensation");
//     frappe.msgprint("Net Compensation recalculated with updated Tax rules.");
// },

// });

// // function populate_object_list(frm) {
// //   let work_team = frm.doc.work_team;
// //   let month = frm.doc.month;

// //   if (!work_team) return;

// //   // Optional message
// //   // frappe.msgprint(`Loading objects for Work Team: ${work_team} for ${month} Month`);

// //   frm.clear_table("object_list");

// //   frappe.call({
// //     method: "frappe.client.get_list",
// //     args: {
// //       doctype: "Project Setup",
// //       filters: {
// //         work_team: work_team,
// //         status: "Completed",
// //         completion_month: month,
// //       },
// //       fields: [
// //         "name",
// //         "object_title",
// //         "task",
// //         "distribution_type",
// //         "sla_class",
// //         "project__object_size_in_hecter",
// //         "completion_date",
// //         "clearing_cost",
// //         "planting_cost",
// //         "completion_month",
// //       ],
// //       limit_page_length: 100,
// //     },
// //     callback: function (r) {
// //       if (!r.message) return;

// //       r.message.forEach((project) => {
// //         let total_comp = 0;
// //         if (project.task === "Forest Clearing") {
// //           total_comp = parseFloat(project.clearing_cost || 0);
// //         } else if (project.task === "Forest Planting") {
// //           total_comp = parseFloat(project.planting_cost || 0);
// //         }

// //         frm.add_child("object_list", {
// //           object: project.name,
// //           object_title: project.object_title,
// //           // task: project.task === "Forest Clearing" ? "Clearing" : "Planting",
// //           task: project.task,
// //           completion_type: project.distribution_type,
// //           sla_class: project.sla_class,
// //           quantity_hectare_or_plants: project.project__object_size_in_hecter,
// //           completion_date: project.completion_date,
// //           total_compensation: total_comp,
// //         });
// //       });

// //       frm.refresh_field("object_list");

// //       // Show the object list section and calculate button section if data exists
// //       if ((frm.doc.object_list || []).length > 0) {
// //         frm.set_df_property("obj_list_section_section", "hidden", 0);
// //         frm.set_df_property("section_break_qjwb", "hidden", 0);
// //       }
// //       frm.refresh_fields();
// //     },
// //   });
// // }

// frappe.ui.form.on("Total Compensation", {
//   month: function (frm) {
//     populate_object_list(frm);
//   },
//   year: function (frm) {
//     // trigger when fiscal year changes
//     populate_object_list(frm);
//   },
// });

// function populate_object_list(frm) {
//   let work_team = frm.doc.work_team;
//   let month = frm.doc.month;

//   if (!work_team || !month) return;

//   const months = [
//     "January",
//     "February",
//     "March",
//     "April",
//     "May",
//     "June",
//     "July",
//     "August",
//     "September",
//     "October",
//     "November",
//     "December",
//   ];

//   let selectedIndex = months.indexOf(month);
//   if (selectedIndex === -1) return;

//   // previous month index (0-11)
//   let prevIndex = (selectedIndex - 1 + 12) % 12;
//   let prevMonthName = months[prevIndex];

//   // Determine which calendar year the SELECTED month belongs to.
//   // If fiscal year is selected (fy_start present), use that mapping.
//   let selectedMonthYear = new Date().getFullYear(); // fallback
//   if (frm.doc && frm.doc.fy_start) {
//     let fyStart = new Date(frm.doc.fy_start);
//     let fyStartMonthIdx = fyStart.getMonth(); // 0-based
//     let fyStartYear = fyStart.getFullYear();
//     // months from fy_start month .. Dec => belong to fyStartYear
//     // months from Jan .. month before fy_start => belong to fyStartYear + 1
//     if (selectedIndex >= fyStartMonthIdx) {
//       selectedMonthYear = fyStartYear;
//     } else {
//       selectedMonthYear = fyStartYear + 1;
//     }
//   } else {
//     // No fiscal year provided: assume selected month belongs to current calendar year
//     selectedMonthYear = new Date().getFullYear();
//   }

//   // Compute the year for the previous month (handles January -> December previous year)
//   let prevMonthYear =
//     prevIndex > selectedIndex ? selectedMonthYear - 1 : selectedMonthYear;

//   // Build start and end dates for previous month (YYYY-MM-DD)
//   let startDate = new Date(prevMonthYear, prevIndex, 1);
//   let endDate = new Date(prevMonthYear, prevIndex + 1, 0); // last day of prevMonth

//   function formatDate(d) {
//     const y = d.getFullYear();
//     const m = String(d.getMonth() + 1).padStart(2, "0");
//     const dd = String(d.getDate()).padStart(2, "0");
//     return `${y}-${m}-${dd}`;
//   }

//   const startDateStr = formatDate(startDate);
//   const endDateStr = formatDate(endDate);

//   frappe.msgprint(
//     `Loading objects for Work Team: ${work_team} — previous month: ${prevMonthName} ${prevMonthYear} (from ${startDateStr} to ${endDateStr})`
//   );

//   frm.clear_table("object_list");

//   frappe.call({
//     method: "frappe.client.get_list",
//     args: {
//       doctype: "Project Setup",
//       filters: [
//         ["work_team", "=", work_team],
//         ["status", "=", "Completed"],
//         ["completion_date", "between", [startDateStr, endDateStr]],
//       ],
//       fields: [
//         "name",
//         "object_title",
//         "task",
//         "distribution_type",
//         "sla_class",
//         "project__object_size_in_hecter",
//         "completion_date",
//         "clearing_cost",
//         "planting_cost",
//         "completion_month",
//       ],
//       limit_page_length: 100,
//     },
//     callback: function (r) {
//       if (!r.message || !r.message.length) {
//         frm.refresh_field("object_list");
//         return;
//       }

//       r.message.forEach((project) => {
//         let total_comp = 0;
//         if (project.task === "Forest Clearing") {
//           total_comp = parseFloat(project.clearing_cost || 0);
//         } else if (project.task === "Forest Planting") {
//           total_comp = parseFloat(project.planting_cost || 0);
//         }

//         frm.add_child("object_list", {
//           object: project.name,
//           object_title: project.object_title,
//           task: project.task,
//           completion_type: project.distribution_type,
//           sla_class: project.sla_class,
//           quantity_hectare_or_plants: project.project__object_size_in_hecter,
//           completion_date: project.completion_date,
//           total_compensation: total_comp,
//         });
//       });

//       frm.refresh_field("object_list");
//     },
//   });
// }

// // function populate_object_list(frm) {
// //     let work_team = frm.doc.work_team;
// //     let month = frm.doc.month;

// //     if (!work_team || !month) return;

// //     // Convert month to previous month
// //     let months = [
// //         "January","February","March","April","May","June",
// //         "July","August","September","October","November","December"
// //     ];

// //     let selectedIndex = months.indexOf(month);
// //     if (selectedIndex === -1) return;  // safety check

// //     // Calculate previous month index
// //     let prevIndex = (selectedIndex - 1 + 12) % 12;
// //     let prevMonth = months[prevIndex];

// //     frappe.msgprint(`Loading objects for Work Team: ${work_team} of PREVIOUS month (${prevMonth})`);

// //     frm.clear_table("object_list");

// //     frappe.call({
// //         method: "frappe.client.get_list",
// //         args: {
// //             doctype: "Project Setup",
// //             filters: {
// //                 work_team: work_team,
// //                 status: "Completed",
// //                 completion_month: prevMonth   // ✅ using previous month here
// //             },
// //             fields: [
// //                 "name", "object_title", "task", "distribution_type", "sla_class",
// //                 "project__object_size_in_hecter", "completion_date",
// //                 "clearing_cost", "planting_cost", "completion_month"
// //             ],
// //             limit_page_length: 100
// //         },
// //         callback: function(r) {
// //             if (!r.message) return;

// //             r.message.forEach(project => {
// //                 let total_comp = 0;
// //                 if (project.task === "Forest Clearing") {
// //                     total_comp = parseFloat(project.clearing_cost || 0);
// //                 } else if (project.task === "Forest Planting") {
// //                     total_comp = parseFloat(project.planting_cost || 0);
// //                 }

// //                 frm.add_child("object_list", {
// //                     object: project.name,
// //                     object_title: project.object_title,
// //                     task: project.task,
// //                     completion_type: project.distribution_type,
// //                     sla_class: project.sla_class,
// //                     quantity_hectare_or_plants: project.project__object_size_in_hecter,
// //                     completion_date: project.completion_date,
// //                     total_compensation: total_comp
// //                 });
// //             });

// //             frm.refresh_field("object_list");
// //         }
// //     });
// // }

// function calculate_compensation(frm) {
//   // Clear existing data in employee_compensation_list
//   frm.clear_table("employee_compensation_list");

//   // Get all completed objects
//   let objects = frm.doc.object_list || [];
//   let not_even_objects = frm.doc.not_even_distribution || [];

//   if (objects.length === 0) {
//     frappe.msgprint(
//       __("No completed objects found to calculate compensation.")
//     );
//     return;
//   }

//   // Get team members first, then process compensation
//   get_team_members_for_calculation(frm).then((team_members) => {
//     if (!team_members || team_members.length === 0) {
//       frappe.msgprint(
//         __('No team members found. Please use "Get Members" button first.')
//       );
//       return;
//     }

//     let employee_compensation = [];

//     // Process each completed object
//     objects.forEach((obj) => {
//       if (!obj.object || !obj.total_compensation) return;

//       // Check if this object has not even distribution
//       let object_not_even = not_even_objects.filter(
//         (ne) => ne.object === obj.object
//       );

//       if (obj.completion_type === "Not Even" && object_not_even.length > 0) {
//         // Process not even distribution
//         object_not_even.forEach((ne_obj) => {
//           if (ne_obj.employee && ne_obj.percentage) {
//             employee_compensation.push({
//               employee: ne_obj.employee,
//               object: obj.object,
//               object_title: obj.object_title,
//               task: obj.task,
//               percentage: ne_obj.percentage,
//               compensation: (obj.total_compensation * ne_obj.percentage) / 100,
//             });
//           }
//         });
//       } else if (obj.completion_type === "Even") {
//         // Process even distribution
//         let even_percentage = 100 / team_members.length;

//         team_members.forEach((member) => {
//           employee_compensation.push({
//             employee: member,
//             object: obj.object,
//             object_title: obj.object_title,
//             task: obj.task,
//             percentage: even_percentage,
//             compensation: (obj.total_compensation * even_percentage) / 100,
//           });
//         });
//       }
//     });

//     // Add all calculated compensation to the table
//     employee_compensation.forEach((ec) => {
//       let row = frm.add_child("employee_compensation_list");
//       row.employee = ec.employee;
//       row.object = ec.object;
//       row.object_title = ec.object_title;
//       row.task = ec.task;
//       row.percentage = ec.percentage;
//       row.compensation = ec.compensation;
//     });

//     frm.refresh_field("employee_compensation_list");

//     // Show the detailed compensation section if data exists
//     if ((frm.doc.employee_compensation_list || []).length > 0) {
//       frm.set_df_property(
//         "detailed_emp_compensation_list_section",
//         "hidden",
//         0
//       );
//     }

//     frappe.msgprint(
//       __("Compensation calculated successfully for {0} records.", [
//         employee_compensation.length,
//       ])
//     );
//     frm.refresh_fields();
//   });
// }

// function get_team_members(frm) {
//   if (!frm.doc.work_team) {
//     frappe.msgprint(__("Please select a Work Team first."));
//     return;
//   }

//   frappe.call({
//     method: "frappe.client.get",
//     args: {
//       doctype: "Work Team",
//       name: frm.doc.work_team,
//     },
//     callback: function (r) {
//       if (r.message && r.message.team_members_list) {
//         // Clear existing not_even_distribution entries
//         frm.clear_table("not_even_distribution");

//         // Add team members to not_even_distribution table for manual percentage entry
//         r.message.team_members_list.forEach((member) => {
//           // You can optionally populate the not_even_distribution table here
//           // if you want to show all members for percentage entry
//         });

//         frm.refresh_field("not_even_distribution");
//         // frappe.msgprint(__('Team members loaded successfully.'));
//       } else {
//         frappe.msgprint(
//           __("No team members found for the selected work team.")
//         );
//       }
//     },
//   });
// }

// function get_team_members_for_calculation(frm) {
//   return new Promise((resolve, reject) => {
//     if (!frm.doc.work_team) {
//       resolve([]);
//       return;
//     }

//     frappe.call({
//       method: "frappe.client.get",
//       args: {
//         doctype: "Work Team",
//         name: frm.doc.work_team,
//       },
//       callback: function (r) {
//         if (r.message && r.message.team_members_list) {
//           let team_members = r.message.team_members_list.map(
//             (m) => m.employee_id
//           );
//           resolve(team_members);
//         } else {
//           resolve([]);
//         }
//       },
//       error: function (r) {
//         reject(r);
//       },
//     });
//   });
// }













































// 🔹 Helper: Client-side equivalent of get_employee_attendance
async function get_employee_attendance_js(employee, month, year) {
  if (!employee || !month || !year) return {};

  // Month name → number
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  let monthNum = months.indexOf(month) + 1;
  if (monthNum === 0) return {};

  // Fiscal year handling
  let [startYear, endYear] = year.split("-").map((y) => parseInt(y));
  let actualYear = monthNum >= 4 ? startYear : endYear;

  // from_date and to_date
  let from_date = `${actualYear}-${String(monthNum).padStart(2, "0")}-01`;
  let to_date = new Date(actualYear, monthNum, 0);
  let to_date_str = `${to_date.getFullYear()}-${String(
    to_date.getMonth() + 1
  ).padStart(2, "0")}-${String(to_date.getDate()).padStart(2, "0")}`;

  // Query attendance directly
  let res = await frappe.db.get_list("Employee Attendance Master", {
    filters: {
      employee: employee,
      date: ["between", [from_date, to_date_str]],
    },
    fields: [
      "employee",
      "full_name",
      "date",
      "duration",
      "present",
      "allowance",
      "project",
      "project_name",
      "team_leader",
      "tl_name",
    ],
    order_by: "date asc",
    limit: 500,
  });

  if (!res || !res.length)
    return {
      attendance: 0,
      total_hours: 0,
      allowance_days: 0,
      daily_allowance_rate: 0,
      piecework_compensation: 0,
    };

  // Summarize
  let total_days = 0,
    total_hours = 0,
    allowance_days = 0;
  res.forEach((r) => {
    r.present = r.present === "Yes" ? 1 : 0;
    r.allowance = r.allowance === "Yes" ? 1 : 0;
    r.duration = parseInt(r.duration || 0);

    if (r.present) total_days += 1;
    if (r.allowance) allowance_days += 1;
    total_hours += r.duration;
  });

  return {
    records: res,
    attendance: total_days,
    total_hours: total_hours,
    allowance_days: allowance_days,
    daily_allowance_rate: 0, // placeholder
    piecework_compensation: 0,
  };
}

// Copyright (c) 2025, bharat and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Total Compensation", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Total Compensation", {
  refresh(frm) {
    // Always show these sections if data already exists
    if ((frm.doc.object_list || []).length > 0) {
      frm.set_df_property("obj_list_section_section", "hidden", 0);
      frm.set_df_property("section_break_qjwb", "hidden", 0); // for Calculate button section
    }

    if ((frm.doc.not_even_distribution || []).length > 0) {
      frm.set_df_property(
        "objects_with_not_even_distribution_section",
        "hidden",
        0
      );
    }

    if ((frm.doc.employee_compensation_list || []).length > 0) {
      frm.set_df_property(
        "detailed_emp_compensation_list_section",
        "hidden",
        0
      );
    }

    if ((frm.doc.employee_compensetion_summery || []).length > 0) {
      frm.set_df_property("section_break_xkna", "hidden", 0);
    }

    frm.refresh_fields();
  },

  // month: function (frm) {
  //   if (!work_team || !year) return;
  //   populate_object_list(frm);

  //   // if (frm.doc.month) {
  //   //   frm.set_df_property("obj_list_section_section", "hidden", 0);
  //   // }
  //   // populate_object_list(frm);
  //   // frm.refresh_fields();
  // },

  month: function (frm) {
    populate_object_list(frm);
  },
  year: function (frm) {
    // trigger when fiscal year changes
    populate_object_list(frm);
  },

  get_members: function (frm) {
    const objectList = frm.doc.object_list || [];
    const hasNotEven = objectList.some(
      (row) => row.completion_type === "Not Even"
    );

    if (objectList.length > 0) {
      // Show section for Calculate button
      frm.set_df_property("section_break_qjwb", "hidden", 0);
    }

    // Show Not Even section only if applicable
    frm.set_df_property(
      "objects_with_not_even_distribution_section",
      "hidden",
      !hasNotEven
    );

    // Execute the get members functionality
    get_team_members(frm);

    // Also execute the original get_members logic for not even distribution
    frm.clear_table("not_even_distribution");

    // Loop through each object
    (frm.doc.object_list || []).forEach((obj) => {
      if (!obj.object || obj.completion_type !== "Not Even") return;

      // Fetch object to get work_team
      frappe.db.get_doc("Project Setup", obj.object).then((project_setup) => {
        const work_team = project_setup.work_team;

        if (!work_team) return;

        // Fetch team members
        frappe.db.get_doc("Work Team", work_team).then((team) => {
          (team.team_members_list || []).forEach((member) => {
            frm.add_child("not_even_distribution", {
              employee: member.employee_id,
              object: obj.object,
              object_title: obj.object_title,
              task: obj.task,
            });
            frm.refresh_field("not_even_distribution");
          });
        });
      });
    });

    frappe.show_alert("Members loaded for Not Even distribution");
    frm.refresh_fields();
  },

  // calculate: function(frm) {
  //     // Calculate compensation when Calculate button is clicked
  //     calculate_compensation(frm);
  //     frm.set_df_property('detailed_emp_compensation_list_section', 'hidden', 0);

  //     setTimeout(function() {
  //         frm.trigger("summery_of_employee");
  //         frm.refresh_fields();
  //     }, 2000);
  // },

  calculate: function (frm) {
    // First validate not even distribution percentages
    let not_even_objects = frm.doc.not_even_distribution || [];
    let object_percentages = {};

    // Group by object and sum percentages
    not_even_objects.forEach((obj) => {
      if (obj.object && obj.percentage) {
        if (!object_percentages[obj.object]) {
          object_percentages[obj.object] = 0;
        }
        object_percentages[obj.object] += obj.percentage;
      }
    });

    // Check if any object has percentage != 100%
    let hasError = false;
    for (let object in object_percentages) {
      if (Math.abs(object_percentages[object] - 100) > 0.01) {
        hasError = true;
        frappe.msgprint(
          __(
            "Total percentage for object {0} should be 100%. Current total: {1}%",
            [object, object_percentages[object].toFixed(2)]
          )
        );
      }
    }

    // If there are percentage errors, stop calculation
    if (hasError) {
      frappe.msgprint(
        __(
          "Please fix percentage distribution errors before calculating compensation."
        )
      );
      return;
    }

    // If no errors, proceed with calculation
    calculate_compensation(frm);
    frm.set_df_property("detailed_emp_compensation_list_section", "hidden", 0);

    setTimeout(function () {
      frm.trigger("summery_of_employee");
      frm.refresh_fields();

      setTimeout(function () {
        frm.trigger("generate_net_compensation");
        frm.refresh_fields();
      }, 2000);
    }, 2000);
  },

  summery_of_employee: function (frm) {
    const summaryMap = {};

    // Step 1: Loop through each row in employee_compensation_list
    (frm.doc.employee_compensation_list || []).forEach((row) => {
      if (!row.employee) return;

      const empId = row.employee;
      const empName = row.employee_name || "";
      const task = (row.task || "").trim();
      const compensation = flt(row.compensation || 0);

      if (!summaryMap[empId]) {
        summaryMap[empId] = {
          employee_id: empId,
          employee_name: empName,
          clearing_compensation: 0,
          planting_compensation: 0,
        };
      }

      if (task === "Forest Clearing") {
        summaryMap[empId].clearing_compensation += compensation;
      } else if (task === "Forest Planting") {
        summaryMap[empId].planting_compensation += compensation;
      }
    });

    // Step 2: Clear existing rows in employee_compensetion_summery
    frm.clear_table("employee_compensetion_summery");

    // Step 3: Add new rows to the summary table
    Object.values(summaryMap).forEach((entry) => {
      const newRow = frm.add_child("employee_compensetion_summery");
      newRow.employee_id = entry.employee_id;
      newRow.employee_name = entry.employee_name;
      newRow.clearing_compensation = entry.clearing_compensation;
      newRow.planting_compensation = entry.planting_compensation;
    });

    frm.refresh_field("employee_compensetion_summery");
    frm.set_df_property("section_break_xkna", "hidden", 0);

    frappe.msgprint("Summary table has been updated successfully.");
    frm.refresh_fields();
  },


// this is woring propper with taxation


//   generate_net_compensation: async function (frm) {
//     debugger;
//     if (!(frm.doc.year && frm.doc.month)) {
//       frappe.msgprint(
//         "Please set Fiscal Year and Month before generating Net Compensation."
//       );
//       return;
//     }

//     frm.clear_table("net_compensation");

//     for (let row of frm.doc.employee_compensetion_summery || []) {
//       let emp = row.employee_id;

//       // 1️⃣ Get attendance + piecework data
//       let r = await frappe.call({
//         method:
//           "contract_management.contract_management.doctype.net_compensation.net_compensation.get_employee_attendance",
//         args: { employee: emp, month: frm.doc.month, year: frm.doc.year },
//       });
//       let data = r.message || {};

//       console.log(data)

//       // 2️⃣ Get employee info (for tax fields)
//       let empDoc = await frappe.db.get_doc("Employee", emp);

//       // Base salary calculations
//       let attendance = data.attendance || 0;
//       let total_hours = data.total_hours || 0;
//       let daily_allowance_rate = data.daily_allowance_rate || 0;
//       let daily_allowance_total = attendance * daily_allowance_rate;

//       let piecework = data.piecework_compensation || 0;
//       let holiday_comp = piecework * 0.13;
//       let reduction_hours = piecework * 0.0362;
//       let gross_salary = piecework + holiday_comp + reduction_hours;

//       // Tax fields (defaults)
//       let tax_table = empDoc.custom_tax_table || null;
//       let tax_column = empDoc.custom_tax_column || null;
//       let sink_tax = empDoc.custom_sink_tax || 0;
//       let tax_relief = empDoc.custom_tax_adjustment__tax_relief || null;

//       let tax_percentage = null;
//       let tax_amount = 0;

//       // 3️⃣ Tax logic
//       if (sink_tax) {
//         // If sink tax TRUE → 25%
//         tax_percentage = 25;
//         tax_amount = gross_salary * 0.25;
//       } 
//        if (tax_table && tax_column) {
//   // Use Tax Table Monthly Salary
//   let taxRows = await frappe.db.get_list("Tax Table Monthly Salary", {
//     filters: {
//       table: parseInt(tax_table),
//       inkomst_from: ["<=", gross_salary],
//       inkomst_tom: [">=", gross_salary]
//     },
//     fields: [
//       "name",
//       "inkomst_from",
//       "inkomst_tom",
//       "column_1",
//       "column_2",
//       "column_3",
//       "column_4",
//       "column_5",
//       "column_6",
//     ],
//   });

//   // console.log("Tax table rows found:", taxRows.length);
//   // console.log("Looking for table:", tax_table, "column:", tax_column);
//   // console.log("Gross salary:", gross_salary);

//   if (taxRows && taxRows.length > 0) {
//     let matchedRow = taxRows[0]; // Should only be one matching row
    
//     // Get the column value based on tax_column
//     let columnValue = 0;
//     let cleanTaxColumn = tax_column
//       .toString()
//       .toLowerCase()
//       .replace(/\s+/g, "")
//       .replace("column", "");
    
//     let columnNumber = parseInt(cleanTaxColumn.replace(/\D/g, "")) || 1;
//     columnNumber = Math.max(1, Math.min(6, columnNumber));
    
//     let columnField = "column_" + columnNumber;
//     columnValue = matchedRow[columnField] || 0;

//     tax_amount = columnValue;
//     tax_percentage = null;

//     // console.log(`Tax calculation: Table ${tax_table}, Column ${tax_column} -> ${columnField}, Gross Salary: ${gross_salary}, Tax Amount: ${tax_amount}`);

//   } else {
//     // fallback → tax relief or 25%
//     tax_percentage = tax_relief || 25;
//     tax_amount = (gross_salary * tax_percentage) / 100;
//     // console.log(      `No matching tax row found. Using fallback tax percentage: ${tax_percentage}%` );

//   }
// }  else if (tax_relief) {
//         // If no table/column, use relief
//         tax_percentage = tax_relief;
//         tax_amount = (gross_salary * tax_percentage) / 100;
//       } else {
//         // Final fallback → 25%
//         tax_percentage = 25;
//         tax_amount = gross_salary * 0.25;
//       }

//       // 4️⃣ Net salary
//       let net_excl_allowance = gross_salary - tax_amount;
//       let total_net = net_excl_allowance + daily_allowance_total;

//       // 5️⃣ Add row
//       let child = frm.add_child("net_compensation");
//       child.employee = emp;
//       child.attendance = attendance;
//       child.total_hours = total_hours;
//       child.daily_allowance_rate_sek = daily_allowance_rate;
//       child.daily_allowance_total_sek = daily_allowance_total;
//       child.piecework_compensation = piecework;
//       child.holiday_compensation_13 = holiday_comp;
//       child.reduction_in_working_hours_362 = reduction_hours;
//       child.gross_salary_total = gross_salary;

//       child.tax_table = tax_table;
//       child.tax_column = tax_column;
//       child.tax_percentage = tax_percentage;
//       child.tax_amount = tax_amount;

//       child.net_compensation_excluding_daily_allowance = net_excl_allowance;
//       child.total_net_compensation = total_net;
//     }

//     frm.refresh_field("net_compensation");
//     frappe.msgprint("Net Compensation recalculated with updated Tax rules.");
//   },








  generate_net_compensation: async function (frm) {
    debugger;
    if (!(frm.doc.year && frm.doc.month)) {
      frappe.msgprint(
        "Please set Fiscal Year and Month before generating Net Compensation."
      );
      return;
    }

    frm.clear_table("net_compensation");

    for (let row of frm.doc.employee_compensetion_summery || []) {
      let emp = row.employee_id;

      // 1️⃣ Get attendance + piecework data
      let r = await frappe.call({
        method:
          "contract_management.contract_management.doctype.net_compensation.net_compensation.get_employee_attendance",
        args: { employee: emp, month: frm.doc.month, year: frm.doc.year },
      });
      let data = r.message || {};


  //     for (let row of frm.doc.employee_compensetion_summery || []) {
  // let emp = row.employee_id;

  // 🔹 Get attendance records for this employee within selected month/year
  let startDate = frappe.datetime.month_start(frm.doc.month + " " + frm.doc.year);
  let endDate = frappe.datetime.month_end(frm.doc.month + " " + frm.doc.year);

  let attendanceRecords = await frappe.db.get_list("Employee Attendance Master", {
    filters: {
      employee: emp,
      present: "Yes",
      date: ["between", [startDate, endDate]]
    },
    fields: ["date", "duration", "present"]
  });

  // 🔹 Attendance count = number of present days
  let attendance = attendanceRecords.length;

  // 🔹 Total hours = sum of durations (convert string to int)
  let total_hours = attendanceRecords.reduce((sum, rec) => {
    return sum + (parseFloat(rec.duration) || 0);
  }, 0);

  // Now you can use these:
  // attendance -> number of present days
  // total_hours -> sum of hours worked



      // 2️⃣ Get employee info (for tax fields)
      let empDoc = await frappe.db.get_doc("Employee", emp);

      // Base salary calculations
      // let attendance = data.attendance || 0;
      // let total_hours = data.total_hours || 0;
      let daily_allowance_rate = data.daily_allowance_rate || 0;
      let daily_allowance_total = attendance * daily_allowance_rate;

      let piecework = data.piecework_compensation || 0;
      let holiday_comp = piecework * 0.13;
      let reduction_hours = piecework * 0.0362;
      let gross_salary = piecework + holiday_comp + reduction_hours;

      // Tax fields (defaults)
      let tax_table = empDoc.custom_tax_table || null;
      let tax_column = empDoc.custom_tax_column || null;
      let sink_tax = empDoc.custom_sink_tax || 0;
      let tax_relief = empDoc.custom_tax_adjustment__tax_relief || null;

      let tax_percentage = null;
      let tax_amount = 0;

      // 3️⃣ Tax logic
      if (sink_tax) {
        // If sink tax TRUE → 25%
        tax_percentage = 25;
        tax_amount = gross_salary * 0.25;
      } 
       if (tax_table && tax_column) {
  // Use Tax Table Monthly Salary
  let taxRows = await frappe.db.get_list("Tax Table Monthly Salary", {
    filters: {
      table: parseInt(tax_table),
      inkomst_from: ["<=", gross_salary],
      inkomst_tom: [">=", gross_salary]
    },
    fields: [
      "name",
      "inkomst_from",
      "inkomst_tom",
      "column_1",
      "column_2",
      "column_3",
      "column_4",
      "column_5",
      "column_6",
    ],
  });

  // console.log("Tax table rows found:", taxRows.length);
  // console.log("Looking for table:", tax_table, "column:", tax_column);
  // console.log("Gross salary:", gross_salary);

  if (taxRows && taxRows.length > 0) {
    let matchedRow = taxRows[0]; // Should only be one matching row
    
    // Get the column value based on tax_column
    let columnValue = 0;
    let cleanTaxColumn = tax_column
      .toString()
      .toLowerCase()
      .replace(/\s+/g, "")
      .replace("column", "");
    
    let columnNumber = parseInt(cleanTaxColumn.replace(/\D/g, "")) || 1;
    columnNumber = Math.max(1, Math.min(6, columnNumber));
    
    let columnField = "column_" + columnNumber;
    columnValue = matchedRow[columnField] || 0;

    tax_amount = columnValue;
    tax_percentage = null;

    // console.log(`Tax calculation: Table ${tax_table}, Column ${tax_column} -> ${columnField}, Gross Salary: ${gross_salary}, Tax Amount: ${tax_amount}`);

  } else {
    // fallback → tax relief or 25%
    tax_percentage = tax_relief || 25;
    tax_amount = (gross_salary * tax_percentage) / 100;
    // console.log(      `No matching tax row found. Using fallback tax percentage: ${tax_percentage}%` );

  }
}  else if (tax_relief) {
        // If no table/column, use relief
        tax_percentage = tax_relief;
        tax_amount = (gross_salary * tax_percentage) / 100;
      } else {
        // Final fallback → 25%
        tax_percentage = 25;
        tax_amount = gross_salary * 0.25;
      }

      // 4️⃣ Net salary
      let net_excl_allowance = gross_salary - tax_amount;
      let total_net = net_excl_allowance + daily_allowance_total;

      // 5️⃣ Add row
      let child = frm.add_child("net_compensation");
      child.employee = emp;
      child.attendance = attendance;
      child.total_hours = total_hours;
      child.daily_allowance_rate_sek = daily_allowance_rate;
      child.daily_allowance_total_sek = daily_allowance_total;
      child.piecework_compensation = piecework;
      child.holiday_compensation_13 = holiday_comp;
      child.reduction_in_working_hours_362 = reduction_hours;
      child.gross_salary_total = gross_salary;

      child.tax_table = tax_table;
      child.tax_column = tax_column;
      child.tax_percentage = tax_percentage;
      child.tax_amount = tax_amount;

      child.net_compensation_excluding_daily_allowance = net_excl_allowance;
      child.total_net_compensation = total_net;
    }

    frm.refresh_field("net_compensation");
    frappe.msgprint("Net Compensation recalculated with updated Tax rules.");
  },












});




// function populate_object_list(frm) {
//   let work_team = frm.doc.work_team;
//   let month = frm.doc.month;

//   if (!work_team) return;

//   // Optional message
//   // frappe.msgprint(`Loading objects for Work Team: ${work_team} for ${month} Month`);

//   frm.clear_table("object_list");

//   frappe.call({
//     method: "frappe.client.get_list",
//     args: {
//       doctype: "Project Setup",
//       filters: {
//         work_team: work_team,
//         status: "Completed",
//         completion_month: month,
//       },
//       fields: [
//         "name",
//         "object_title",
//         "task",
//         "distribution_type",
//         "sla_class",
//         "project__object_size_in_hecter",
//         "completion_date",
//         "clearing_cost",
//         "planting_cost",
//         "completion_month",
//       ],
//       limit_page_length: 100,
//     },
//     callback: function (r) {
//       if (!r.message) return;

//       r.message.forEach((project) => {
//         let total_comp = 0;
//         if (project.task === "Forest Clearing") {
//           total_comp = parseFloat(project.clearing_cost || 0);
//         } else if (project.task === "Forest Planting") {
//           total_comp = parseFloat(project.planting_cost || 0);
//         }

//         frm.add_child("object_list", {
//           object: project.name,
//           object_title: project.object_title,
//           // task: project.task === "Forest Clearing" ? "Clearing" : "Planting",
//           task: project.task,
//           completion_type: project.distribution_type,
//           sla_class: project.sla_class,
//           quantity_hectare_or_plants: project.project__object_size_in_hecter,
//           completion_date: project.completion_date,
//           total_compensation: total_comp,
//         });
//       });

//       frm.refresh_field("object_list");

//       // Show the object list section and calculate button section if data exists
//       if ((frm.doc.object_list || []).length > 0) {
//         frm.set_df_property("obj_list_section_section", "hidden", 0);
//         frm.set_df_property("section_break_qjwb", "hidden", 0);
//       }
//       frm.refresh_fields();
//     },
//   });
// }

frappe.ui.form.on("Total Compensation", {
  month: function (frm) {
    populate_object_list(frm);
  },
  year: function (frm) {
    // trigger when fiscal year changes
    populate_object_list(frm);
  },
});

function populate_object_list(frm) {
  let work_team = frm.doc.work_team;
  let month = frm.doc.month;

  if (!work_team || !month) return;

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  let selectedIndex = months.indexOf(month);
  if (selectedIndex === -1) return;

  // previous month index (0-11)
  let prevIndex = (selectedIndex - 1 + 12) % 12;
  let prevMonthName = months[prevIndex];

  // Determine which calendar year the SELECTED month belongs to.
  // If fiscal year is selected (fy_start present), use that mapping.
  let selectedMonthYear = new Date().getFullYear(); // fallback
  if (frm.doc && frm.doc.fy_start) {
    let fyStart = new Date(frm.doc.fy_start);
    let fyStartMonthIdx = fyStart.getMonth(); // 0-based
    let fyStartYear = fyStart.getFullYear();
    // months from fy_start month .. Dec => belong to fyStartYear
    // months from Jan .. month before fy_start => belong to fyStartYear + 1
    if (selectedIndex >= fyStartMonthIdx) {
      selectedMonthYear = fyStartYear;
    } else {
      selectedMonthYear = fyStartYear + 1;
    }
  } else {
    // No fiscal year provided: assume selected month belongs to current calendar year
    selectedMonthYear = new Date().getFullYear();
  }

  // Compute the year for the previous month (handles January -> December previous year)
  let prevMonthYear =
    prevIndex > selectedIndex ? selectedMonthYear - 1 : selectedMonthYear;

  // Build start and end dates for previous month (YYYY-MM-DD)
  let startDate = new Date(prevMonthYear, prevIndex, 1);
  let endDate = new Date(prevMonthYear, prevIndex + 1, 0); // last day of prevMonth

  function formatDate(d) {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const dd = String(d.getDate()).padStart(2, "0");
    return `${y}-${m}-${dd}`;
  }

  const startDateStr = formatDate(startDate);
  const endDateStr = formatDate(endDate);

  frappe.msgprint(
    `Loading objects for Work Team: ${work_team} — previous month: ${prevMonthName} ${prevMonthYear} (from ${startDateStr} to ${endDateStr})`
  );

  frm.clear_table("object_list");

  frappe.call({
    method: "frappe.client.get_list",
    args: {
      doctype: "Project Setup",
      filters: [
        ["work_team", "=", work_team],
        ["status", "=", "Completed"],
        ["completion_date", "between", [startDateStr, endDateStr]],
      ],
      fields: [
        "name",
        "object_title",
        "task",
        "distribution_type",
        "sla_class",
        "project__object_size_in_hecter",
        "completion_date",
        "clearing_cost",
        "planting_cost",
        "completion_month",
      ],
      limit_page_length: 100,
    },
    callback: function (r) {
      if (!r.message || !r.message.length) {
        frm.refresh_field("object_list");
        return;
      }

      r.message.forEach((project) => {
        let total_comp = 0;
        if (project.task === "Forest Clearing") {
          total_comp = parseFloat(project.clearing_cost || 0);
        } else if (project.task === "Forest Planting") {
          total_comp = parseFloat(project.planting_cost || 0);
        }

        frm.add_child("object_list", {
          object: project.name,
          object_title: project.object_title,
          task: project.task,
          completion_type: project.distribution_type,
          sla_class: project.sla_class,
          quantity_hectare_or_plants: project.project__object_size_in_hecter,
          completion_date: project.completion_date,
          total_compensation: total_comp,
        });
      });

      frm.refresh_field("object_list");
    },
  });
}

// function populate_object_list(frm) {
//     let work_team = frm.doc.work_team;
//     let month = frm.doc.month;

//     if (!work_team || !month) return;

//     // Convert month to previous month
//     let months = [
//         "January","February","March","April","May","June",
//         "July","August","September","October","November","December"
//     ];

//     let selectedIndex = months.indexOf(month);
//     if (selectedIndex === -1) return;  // safety check

//     // Calculate previous month index
//     let prevIndex = (selectedIndex - 1 + 12) % 12;
//     let prevMonth = months[prevIndex];

//     frappe.msgprint(`Loading objects for Work Team: ${work_team} of PREVIOUS month (${prevMonth})`);

//     frm.clear_table("object_list");

//     frappe.call({
//         method: "frappe.client.get_list",
//         args: {
//             doctype: "Project Setup",
//             filters: {
//                 work_team: work_team,
//                 status: "Completed",
//                 completion_month: prevMonth   // ✅ using previous month here
//             },
//             fields: [
//                 "name", "object_title", "task", "distribution_type", "sla_class",
//                 "project__object_size_in_hecter", "completion_date",
//                 "clearing_cost", "planting_cost", "completion_month"
//             ],
//             limit_page_length: 100
//         },
//         callback: function(r) {
//             if (!r.message) return;

//             r.message.forEach(project => {
//                 let total_comp = 0;
//                 if (project.task === "Forest Clearing") {
//                     total_comp = parseFloat(project.clearing_cost || 0);
//                 } else if (project.task === "Forest Planting") {
//                     total_comp = parseFloat(project.planting_cost || 0);
//                 }

//                 frm.add_child("object_list", {
//                     object: project.name,
//                     object_title: project.object_title,
//                     task: project.task,
//                     completion_type: project.distribution_type,
//                     sla_class: project.sla_class,
//                     quantity_hectare_or_plants: project.project__object_size_in_hecter,
//                     completion_date: project.completion_date,
//                     total_compensation: total_comp
//                 });
//             });

//             frm.refresh_field("object_list");
//         }
//     });
// }

function calculate_compensation(frm) {
  // Clear existing data in employee_compensation_list
  frm.clear_table("employee_compensation_list");

  // Get all completed objects
  let objects = frm.doc.object_list || [];
  let not_even_objects = frm.doc.not_even_distribution || [];

  if (objects.length === 0) {
    frappe.msgprint(
      __("No completed objects found to calculate compensation.")
    );
    return;
  }

  // Get team members first, then process compensation
  get_team_members_for_calculation(frm).then((team_members) => {
    if (!team_members || team_members.length === 0) {
      frappe.msgprint(
        __('No team members found. Please use "Get Members" button first.')
      );
      return;
    }

    let employee_compensation = [];

    // Process each completed object
    objects.forEach((obj) => {
      if (!obj.object || !obj.total_compensation) return;

      // Check if this object has not even distribution
      let object_not_even = not_even_objects.filter(
        (ne) => ne.object === obj.object
      );

      if (obj.completion_type === "Not Even" && object_not_even.length > 0) {
        // Process not even distribution
        object_not_even.forEach((ne_obj) => {
          if (ne_obj.employee && ne_obj.percentage) {
            employee_compensation.push({
              employee: ne_obj.employee,
              object: obj.object,
              object_title: obj.object_title,
              task: obj.task,
              percentage: ne_obj.percentage,
              compensation: (obj.total_compensation * ne_obj.percentage) / 100,
            });
          }
        });
      } else if (obj.completion_type === "Even") {
        // Process even distribution
        let even_percentage = 100 / team_members.length;

        team_members.forEach((member) => {
          employee_compensation.push({
            employee: member,
            object: obj.object,
            object_title: obj.object_title,
            task: obj.task,
            percentage: even_percentage,
            compensation: (obj.total_compensation * even_percentage) / 100,
          });
        });
      }
    });

    // Add all calculated compensation to the table
    employee_compensation.forEach((ec) => {
      let row = frm.add_child("employee_compensation_list");
      row.employee = ec.employee;
      row.object = ec.object;
      row.object_title = ec.object_title;
      row.task = ec.task;
      row.percentage = ec.percentage;
      row.compensation = ec.compensation;
    });

    frm.refresh_field("employee_compensation_list");

    // Show the detailed compensation section if data exists
    if ((frm.doc.employee_compensation_list || []).length > 0) {
      frm.set_df_property(
        "detailed_emp_compensation_list_section",
        "hidden",
        0
      );
    }

    frappe.msgprint(
      __("Compensation calculated successfully for {0} records.", [
        employee_compensation.length,
      ])
    );
    frm.refresh_fields();
  });
}

function get_team_members(frm) {
  if (!frm.doc.work_team) {
    frappe.msgprint(__("Please select a Work Team first."));
    return;
  }

  frappe.call({
    method: "frappe.client.get",
    args: {
      doctype: "Work Team",
      name: frm.doc.work_team,
    },
    callback: function (r) {
      if (r.message && r.message.team_members_list) {
        // Clear existing not_even_distribution entries
        frm.clear_table("not_even_distribution");

        // Add team members to not_even_distribution table for manual percentage entry
        r.message.team_members_list.forEach((member) => {
          // You can optionally populate the not_even_distribution table here
          // if you want to show all members for percentage entry
        });

        frm.refresh_field("not_even_distribution");
        // frappe.msgprint(__('Team members loaded successfully.'));
      } else {
        frappe.msgprint(
          __("No team members found for the selected work team.")
        );
      }
    },
  });
}

function get_team_members_for_calculation(frm) {
  return new Promise((resolve, reject) => {
    if (!frm.doc.work_team) {
      resolve([]);
      return;
    }

    frappe.call({
      method: "frappe.client.get",
      args: {
        doctype: "Work Team",
        name: frm.doc.work_team,
      },
      callback: function (r) {
        if (r.message && r.message.team_members_list) {
          let team_members = r.message.team_members_list.map(
            (m) => m.employee_id
          );
          resolve(team_members);
        } else {
          resolve([]);
        }
      },
      error: function (r) {
        reject(r);
      },
    });
  });
}
