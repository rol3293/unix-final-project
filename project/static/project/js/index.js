function remove(id, csrf_token) {
    const li = document.getElementById(`user${id}`);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/project/delete/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrf_token);
    xhr.send(JSON.stringify({
        id: id
    }));
    xhr.onreadystatechange = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const status = xhr.status;
            // if post request is good, redirect to index
            if (status === 200)
                li.remove();
            else if (status >= 500 && status < 600)
                alert("internal error")
            else if ((status !== 0 || !(status >= 200 && status < 400))) {
                alert(JSON.parse(xhr.response).error);
            }
        }
    }
}