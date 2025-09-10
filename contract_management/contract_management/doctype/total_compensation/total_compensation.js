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

//   month: function (frm) {
//     if (frm.doc.month) {
//       frm.set_df_property("obj_list_section_section", "hidden", 0);
//     }
//     populate_object_list(frm);
//     frm.refresh_fields();
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

//   // validate: function(frm) {
//   //     // Validate not even distribution percentages
//   //     let not_even_objects = frm.doc.not_even_distribution || [];
//   //     let object_percentages = {};

//   //     // Group by object and sum percentages
//   //     not_even_objects.forEach(obj => {
//   //         if (obj.object && obj.percentage) {
//   //             if (!object_percentages[obj.object]) {
//   //                 object_percentages[obj.object] = 0;
//   //             }
//   //             object_percentages[obj.object] += obj.percentage;
//   //         }
//   //     });

//   //     // Check if any object has percentage != 100%
//   //     for (let object in object_percentages) {
//   //         if (Math.abs(object_percentages[object] - 100) > 0.01) {
//   //             frappe.validated = false;
//   //             frappe.msgprint(__('Total percentage for object {0} should be 100%. Current total: {1}%',
//   //                 [object, object_percentages[object]]));
//   //             return;
//   //         }
//   //     }
//   // }

//   // generate_net_compensation: function (frm) {
//   //   // frm.call("generate_net_compensation").then(() => {
//   //   //     frm.reload_doc();
//   //   // });

//   //   frappe.call({
//   //     method:
//   //       "contract_management.contract_management.doctype.total_compensation.total_compensation.TotalCompensation.generate_net_compensation",
//   //     doc: frm.doc,
//   //     callback: function () {
//   //       frm.reload_doc();
//   //     },
//   //   });
//   // },

//   generate_net_compensation: function (frm) {
//   frappe.call({
//     method: "generate_net_compensation", // method inside total_compensation.py
//     doc: frm.doc,
//     callback: function (r) {
//       // Refresh the specific field first
//       frm.refresh_field("net_compensation");

//       // Show the net compensation section if data exists
//       if ((frm.doc.net_compensation || []).length > 0) {
//         frm.set_df_property("net_compensation_section", "hidden", 0);
//       }

//       // Refresh all fields to ensure UI updates
//       frm.refresh_fields();

//       // Then reload the document to ensure all data is synced
//       frm.reload_doc();
//     },
//     error: function(r) {
//       frappe.msgprint(__("Error generating net compensation. Please try again."));
//     }
//   });
// },

//   // generate_net_compensation: function (frm) {
//   //   frappe.call({
//   //     method: "generate_net_compensation", // method inside total_compensation.py
//   //     doc: frm.doc,
//   //     callback: function () {
//   //       frm.reload_doc();
//   //     },
//   //   });
//   // },

// });

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

  month: function (frm) {
    if (frm.doc.month) {
      frm.set_df_property("obj_list_section_section", "hidden", 0);
    }
    populate_object_list(frm);
    frm.refresh_fields();
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

  // validate: function(frm) {
  //     // Validate not even distribution percentages
  //     let not_even_objects = frm.doc.not_even_distribution || [];
  //     let object_percentages = {};

  //     // Group by object and sum percentages
  //     not_even_objects.forEach(obj => {
  //         if (obj.object && obj.percentage) {
  //             if (!object_percentages[obj.object]) {
  //                 object_percentages[obj.object] = 0;
  //             }
  //             object_percentages[obj.object] += obj.percentage;
  //         }
  //     });

  //     // Check if any object has percentage != 100%
  //     for (let object in object_percentages) {
  //         if (Math.abs(object_percentages[object] - 100) > 0.01) {
  //             frappe.validated = false;
  //             frappe.msgprint(__('Total percentage for object {0} should be 100%. Current total: {1}%',
  //                 [object, object_percentages[object]]));
  //             return;
  //         }
  //     }
  // }

  // generate_net_compensation: function (frm) {
  //   // frm.call("generate_net_compensation").then(() => {
  //   //     frm.reload_doc();
  //   // });

  //   frappe.call({
  //     method:
  //       "contract_management.contract_management.doctype.total_compensation.total_compensation.TotalCompensation.generate_net_compensation",
  //     doc: frm.doc,
  //     callback: function () {
  //       frm.reload_doc();
  //     },
  //   });
  // },

  //   generate_net_compensation: function (frm) {
  //   frappe.call({
  //     method: "generate_net_compensation", // method inside total_compensation.py
  //     doc: frm.doc,
  //     callback: function (r) {
  //       // Refresh the specific field first
  //       frm.refresh_field("net_compensation");

  //       // Show the net compensation section if data exists
  //       if ((frm.doc.net_compensation || []).length > 0) {
  //         frm.set_df_property("net_compensation_section", "hidden", 0);
  //       }

  //       // Refresh all fields to ensure UI updates
  //       frm.refresh_fields();

  //       // Then reload the document to ensure all data is synced
  //       frm.reload_doc();
  //     },
  //     error: function(r) {
  //       frappe.msgprint(__("Error generating net compensation. Please try again."));
  //     }
  //   });
  // },

  // generate_net_compensation: function (frm) {
  //   frappe.call({
  //     method: "generate_net_compensation", // method inside total_compensation.py
  //     doc: frm.doc,
  //     callback: function () {
  //       frm.reload_doc();
  //     },
  //   });
  // },

  generate_net_compensation: async function (frm) {
    if (!(frm.doc.year && frm.doc.month)) {
      frappe.msgprint(
        "Please set Fiscal Year and Month before generating Net Compensation."
      );
      return;
    }

    // Clear table before regeneration
    frm.clear_table("net_compensation");

    // Loop over summary employees
    for (let row of frm.doc.employee_compensetion_summery || []) {
      let emp = row.employee_id;

      // Fetch attendance + piecework data from backend
      let r = await frappe.call({
        method:
          "contract_management.contract_management.doctype.net_compensation.net_compensation.get_employee_attendance",
        args: {
          employee: emp,
          month: frm.doc.month,
          year: frm.doc.year,
        },
      });

      let data = r.message || {};

      // 🧮 Perform calculations (JS version of your Python formulas)
      let attendance = data.attendance || 0;
      let total_hours = data.total_hours || 0;
      let daily_allowance_rate = data.daily_allowance_rate || 0;
      let daily_allowance_total = attendance * daily_allowance_rate;

      let piecework = data.piecework_compensation || 0;

      let holiday_comp = piecework * 0.13;
      let reduction_hours = piecework * 0.0362;

      let gross_salary = piecework + holiday_comp + reduction_hours;
      let tax_percentage = 30;
      let tax_amount = (gross_salary * tax_percentage) / 100;

      let net_excl_allowance = gross_salary - tax_amount;
      let total_net = net_excl_allowance + daily_allowance_total;

      // Append to child table
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
      child.tax_percentage = tax_percentage;
      child.tax_amount = tax_amount;
      child.net_compensation_excluding_daily_allowance = net_excl_allowance;
      child.total_net_compensation = total_net;
    }

    frm.refresh_field("net_compensation");
    frappe.msgprint("Net Compensation calculated instantly (JS)");
  },
});

function populate_object_list(frm) {
  let work_team = frm.doc.work_team;
  let month = frm.doc.month;

  if (!work_team) return;

  // Optional message
  // frappe.msgprint(`Loading objects for Work Team: ${work_team} for ${month} Month`);

  frm.clear_table("object_list");

  frappe.call({
    method: "frappe.client.get_list",
    args: {
      doctype: "Project Setup",
      filters: {
        work_team: work_team,
        status: "Completed",
        completion_month: month,
      },
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
      if (!r.message) return;

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
          // task: project.task === "Forest Clearing" ? "Clearing" : "Planting",
          task: project.task,
          completion_type: project.distribution_type,
          sla_class: project.sla_class,
          quantity_hectare_or_plants: project.project__object_size_in_hecter,
          completion_date: project.completion_date,
          total_compensation: total_comp,
        });
      });

      frm.refresh_field("object_list");

      // Show the object list section and calculate button section if data exists
      if ((frm.doc.object_list || []).length > 0) {
        frm.set_df_property("obj_list_section_section", "hidden", 0);
        frm.set_df_property("section_break_qjwb", "hidden", 0);
      }
      frm.refresh_fields();
    },
  });
}

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
