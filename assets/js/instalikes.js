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

var xhr;
function menu(id, self) {
  if (self.className == "fas fa-heart") {
    self.className = "far fa-heart";
    decreaseLikes(id);
  }
  else if (self.className == "far fa-heart") {
    self.className = "fas fa-heart";
    increaseLikes(id);
  }
}
function likeByImage(id, self) {
  var classname = self.parentNode.childNodes[3].childNodes[1].className;
  if (classname == "far fa-heart") {
    self.parentNode.childNodes[3].childNodes[1].className = "fas fa-heart";
    increaseLikes(id)
  }
}
function increaseLikes(id) {
  xhr = new XMLHttpRequest();
  var params = 'y=' + id;
  xhr.open("POST", "increaseLikes", true);
  xhr.onreadystatechange = callback;
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrfcookie());
  xhr.send(params);
}
function decreaseLikes(id) {
  xhr = new XMLHttpRequest();
  var params = 'y=' + id;
  xhr.open("POST", "decreaseLikes", true);
  xhr.onreadystatechange = callback;
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrfcookie());
  xhr.send(params);
}
function callback() {
  if (xhr.readyState == 4 && xhr.status == 200) {
    var res = JSON.parse(xhr.responseText);
    var image = JSON.stringify(res.image);
    var y = document.querySelector("img[src=" + image + "]");
    var parent = y.parentNode;
    var totaLikes = parent.childNodes[5];
    totaLikes.querySelector('a').innerHTML = res.likes + " others ";
    var colorofHeart = parent.childNodes[3];
  }
}
function image_loaded(id, self) {
  var ob = new XMLHttpRequest();
  var params = 'y=' + id;
  ob.open("POST", "checkForLike", true);
  ob.onreadystatechange = function () {
    if (ob.readyState == 4 && ob.status == 200) {
      var res = JSON.parse(ob.responseText);
      var classname = res.classname;
      if (classname == "fas fa-heart") {
        self.parentNode.childNodes[3].childNodes[1].className = "fas fa-heart";
      }
    }
  };
  ob.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  ob.setRequestHeader("X-CSRFToken", csrfcookie());
  ob.send(params);
};
document.getElementById("close").addEventListener('click', close);
function close() {
  document.getElementById("likedby").style.display = "none";
};
function getLikes(id) {
  var ob = new XMLHttpRequest();
  var params = 'y=' + id;
  ob.open("POST", "ajaxgetLikes", true);
  ob.onreadystatechange = function () {
    if (ob.readyState == 4 && ob.status == 200) {
      var res = JSON.parse(ob.responseText);
      document.getElementById("likedby").style.display = "flex";
      var content = document.getElementById("likes");
      content.innerHTML = "";
      for (var i = 0; i < res['usersLiked'].length; i++) {
        content.innerHTML += '<h3>' + res['usersLiked'][i]['name'] + '</h3>'
      }
    }
  };
  ob.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  ob.setRequestHeader("X-CSRFToken", csrfcookie());
  ob.send(params);

}