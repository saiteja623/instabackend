
var csrfcookie = function () {
    var cookieValue = null,
        name = "csrftoken";
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function accept_user(id, self) {
    var y = self.parentNode.parentNode;
    y.style.display = "none";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "accept_request", true);
    var params = 'id=' + id;
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log("done")
        }
    }
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrfcookie());
    xhr.send(params);
}

function decline_user(id, self) {
    var y = self.parentNode.parentNode;
    y.style.display = "none";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "decline_request", true);
    var params = 'id=' + id;
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log("done")
        }
    }
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrfcookie());
    xhr.send(params);
}