let mainForm = document.querySelector("#profile-form");
let qualificationForm = document.getElementsByClassName("qualification-form");
const emptyqualificationForm=qualificationForm[0].cloneNode(true);
let addButton = document.querySelector("#add-qualification-form");
let qualificationContainer = document.querySelector(
    "#qualification-container"
  );
let qualificationFormCount = qualificationForm.length - 1;
let totalForms = document.querySelector('[id$="qualification_set_set-TOTAL_FORMS"]');
const formRegex = RegExp(`_set-(\\d)-`, "g");
function updateForms() {
    let count = 0;
    for (let form of qualificationForm) {
        form.innerHTML = form.innerHTML.replace(formRegex, `_set-${count++}-`);
    }
}
addButton.addEventListener("click", function (e) {
    e.preventDefault();
    const newQualificationForm = emptyqualificationForm.cloneNode(true);
    qualificationFormCount++;
    newQualificationForm.innerHTML = newQualificationForm.innerHTML.replace(
        formRegex,
        `_set-${qualificationFormCount}-`
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