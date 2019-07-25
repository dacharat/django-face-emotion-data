const face_name = document.getElementById("face-name").textContent;
let csrftoken = Cookies.get("csrftoken") || '';
function csrfSafeMethod(method) {
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

editText = () => {
  let name = document.getElementById("face-name");
  let submitButton = document.getElementById("submit-button");
  let editButton = document.getElementById("edit-button");
  name.setAttribute("contenteditable", "true");
  name.focus()
  submitButton.setAttribute("style", "display: inline;");
  editButton.setAttribute("style", "display: none;");
}

submit = () => {
  let name = document.getElementById("face-name");
  let submitButton = document.getElementById("submit-button");
  let editButton = document.getElementById("edit-button");
  name.setAttribute("contenteditable", "flase");
  submitButton.setAttribute("style", "display: none;");
  editButton.setAttribute("style", "display: inline;");
  
  $.ajax({
    url: "http://localhost:3000/face/new/",
    type: "PUT",
    data: {
      face: face_name,
      newFaceName: name.textContent,
      action: "change_face_name"
    },
    success: data => {
      console.log(data);
      let currentpath = window.location.pathname.split('/');
      currentpath[1] = name.textContent
      let newpath = currentpath.join('/')
      console.log(newpath);
      window.location.replace(newpath);
    },
    error: err => {
      console.log(err);
    }
  });
}

cancel = () => {
  let name = document.getElementById("face-name");
  let submitButton = document.getElementById("submit-button");
  let editButton = document.getElementById("edit-button");
  name.setAttribute("contenteditable", "flase");
  submitButton.setAttribute("style", "display: none;");
  editButton.setAttribute("style", "display: inline;");
}