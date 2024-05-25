// const ROLE_TO_HIDE_NAVBAR = ["Projects User"];

// function hideElements() {
//   document.querySelector(".navbar").style.display = "none";
//   document.querySelector(".page-head").style.display = "none";
//   document.querySelector(".layout-side-section").style.display = "none";
// }

// function fetchUserDetails() {
//   const currentUser = frappe.session.user;
//   frappe.call({
//     method: "frappe.client.get",
//     args: {
//       doctype: "User",
//       name: currentUser,
//     },
//     callback: function (response) {
//       const user = response.message;
//       if (user) {
//         const userRoles = user.roles.map((role) => role.role);
//         if (
//           userRoles.some((role) => ROLE_TO_HIDE_NAVBAR.includes(role)) &&
//           window.location.pathname.includes("/app/communication/view/report")
//         ) {
//           hideElements();
//         }
//       } else {
//         console.log("User not found");
//       }
//     },
//   });
// }

// setTimeout(fetchUserDetails, 100);
