SCRIPTS =  \
"// check when frame was reloaded\n\r" \
"var iframe = document.getElementById(\" %s\");\n\r" \
"iframe.onload = function() {{\n\r" \
"    var url = iframe.contentWindow.location.href;\n\r" \
"\n\r" \
"    var commit = getCommitFromUrl(url);\n\r" \
"\n\r" \
"    if (commit) {{\n\r" \
"        highlight(commit);\n\r" \
"    }}\n\r" \
"}}\n\r" \
"\n\r" \
"// highlight commit\n\r" \
"function highlight(commit) {{\n\r" \
"    var iframe = document.getElementById(\" %s\");\n\r" \
"    var inner = iframe.contentDocument || iframe.contentWindow.document;\n\r" \
"\n\r" \
"\n\r" \
"    document.title = inner.title;\n\r" \
"\n\r" \
"    var commits = inner.getElementsByClassName(\"list subject\");\n\r" \
"    for (var i = 0; i < commits.length; i++) {{\n\r" \
"        if (commits[i].innerText.includes(commit)) {{\n\r" \
"            commits[i].style.color=\"red\";\n\r" \
"            commits[i].textContent = \"--> \" + commits[i].textContent;\n\r" \
"        }}\n\r" \
"    }}\n\r" \
"}}\n\r" \
"\n\r" \
"// parce commit from url\n\r" \
"function getCommitFromUrl(url) {{\n\r" \
"        var splitted = url.split(';');\n\r" \
"\n\r" \
"        for (var i = 0; i < splitted.length; i++) {{\n\r" \
"            if (splitted[i].includes(\"commit=\")) {{\n\r" \
"                var commit = splitted[i];\n\r" \
"\n\r" \
"                commit = commit.replace(\"commit=\", \"\");\n\r" \
"                commit = commit.replace(/%20/g, \" \");\n\r" \
"\n\r" \
"                return commit;\n\r" \
"            }}\n\r" \
"        }}\n\r" \
"    return \"\";\n\r" \
"}}\n\r"