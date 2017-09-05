// check when frame was reloaded
var iframe = document.getElementById("includer");
iframe.onload = function() {
    var url = iframe.contentWindow.location.href;

    var commit = getCommitFromUrl(url);
    var hash = getHashFromUrl(url);

    if (commit) {
        highlight(commit, hash);
    }
}

// highlight commit
function highlight(commit, hash) {
    var iframe = document.getElementById("includer");
    var inner = iframe.contentDocument || iframe.contentWindow.document;


    document.title = inner.title;

    var commits = inner.getElementsByClassName("list subject");
    for (var i = 0; i < commits.length; i++) {
        if (commits[i].innerText.includes(commit) &&
                commits[i].href.includes(hash)) {
            commits[i].style.color="red";
            commits[i].textContent = "--> " + commits[i].textContent;
        }
    }
}

// parce commit from url
function getCommitFromUrl(url) {
        var splitted = url.split(';');

        for (var i = 0; i < splitted.length; i++) {
            if (splitted[i].includes("cm=")) {
                var commit = splitted[i];

                commit = commit.replace("cm=", "");
                commit = commit.replace(/%20/g, " ");

                return commit;
            }
        }
    return "";
}

// parce hash from url
function getHashFromUrl(url) {
        var splitted = url.split(';');

        for (var i = 0; i < splitted.length; i++) {
            if (splitted[i].includes("ch=")) {
                var hash = splitted[i];

                hash = hash.replace("ch=", "");

                return hash;
            }
        }
    return "";

}