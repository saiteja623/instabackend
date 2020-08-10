function search(e) {
        var val = document.getElementById("search").value;
        if (val == "") {
                document.getElementById("res").style.display = "none";
        }
        else {
                /*xhr =new XMLHttpRequest();*/
                params = "client=chrome&q=" + val + "&hl=en";
                url = "https://cors-anywhere.herokuapp.com/http://suggestqueries.google.com/complete/search?" + params;
                fetch(url)
                        .then(response => response.json())
                        .then(data => {
                                var res = document.getElementById("res");
                                res.innerHTML = " ";
                                res.style.display = "block";
                                if (data[1].length > 4) {
                                        for (var i = 0; i < 4; i++) {
                                                res.innerHTML += '<h3>' + data[1][i] + '</h3>';
                                        }
                                }
                                else {
                                        for (var i = 0; i < data[1].length; i++) {
                                                res.innerHTML += '<h3>' + data[1][i] + '</h3>';
                                        }
                                }
                                var v = document.getElementsByTagName("h3");
                                for (var i = 0; i < v.length; i++) {
                                        v[i].addEventListener('click', googleit);
                                }
                        });
        }
}
function googleit() {
        var val = this.innerHTML;
        url = "https://www.google.com/search?q=" + val;
        window.open(url, "_self");
}
document.getElementById("clear").addEventListener("click", function () {
        document.getElementById("search").value = "";
        search();
});
document.getElementById("search").addEventListener('keydown', function (e) {
        if (e.keyCode == 13) {
                var val = document.getElementById("search").value;
                url = "https://www.google.com/search?q=" + val;
                window.open(url, "_self");
        }
})