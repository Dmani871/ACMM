let mainForm = document.querySelector("#profile-form");
let qualificationForm = document.getElementsByClassName("qualification-form");
const emptyqualificationForm=qualificationForm[0].cloneNode(true);
let addButton = document.querySelector("#add-qualification-form");
let qualificationContainer = document.querySelector(
    "#qualification-container"
  );
let qualificationFormCount = qualificationForm.length - 1;
let totalForms = document.querySelector("#id_menteequalification_set_set-TOTAL_FORMS");
const formRegex = RegExp(`menteequalification_set_set-(\\d){1}-`, "g");
function updateForms() {
let count = 0;
for (let form of qualificationForm) {
    form.innerHTML = form.innerHTML.replace(formRegex, `menteequalification_set-${count++}-`);
}
}
addButton.addEventListener("click", function (e) {
e.preventDefault();
const newQualificationForm = emptyqualificationForm.cloneNode(true);
qualificationFormCount++;
newQualificationForm.innerHTML = newQualificationForm.innerHTML.replace(
    formRegex,
    `menteequalification_set_set-${qualificationFormCount}-`
);
qualificationContainer.append(newQualificationForm);
totalForms.setAttribute("value", `${qualificationFormCount + 1}`);
});


mainForm.addEventListener("click", function (event) {
if (event.target.classList.contains("delete-qualification-form")) {
    event.preventDefault();
    event.target.parentElement.remove();
    qualificationFormCount--;
    updateForms();
    totalForms.setAttribute("value", `${qualificationFormCount - 1}`);
}
});