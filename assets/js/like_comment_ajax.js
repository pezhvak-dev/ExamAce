function like(id) {
    var element = document.getElementById("like");
    $.get(`/weblog/comment/like/${id}`).then(response => {
            if (response['response'] === "liked") {
                element.className = "flex items-center justify-center relative w-9 h-9 bg-secondary rounded-full text-muted transition-colors text-red-500"
            } else {
                element.className = "flex items-center justify-center relative w-9 h-9 bg-secondary rounded-full text-muted transition-colors hover:text-red-500"
            }
        }
    )
}