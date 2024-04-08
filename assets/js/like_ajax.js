function like(id) {
    var element = document.getElementById("like");
    var count = document.getElementById("count");
    $.get(`/weblog/comment/like/${id}`).then(response => {
        if (response['response'] === "liked") {
            element.className = "flex items-center justify-center relative w-9 h-9 bg-secondary rounded-full text-muted transition-colors text-red-500"
            count.innerText = Number(count.innerText) + 1;
        } else {
            element.className = "flex items-center justify-center relative w-9 h-9 bg-secondary rounded-full text-muted transition-colors hover:text-red-500"
            count.innerText = Number(count.innerText) - 1;

        }
    })
}