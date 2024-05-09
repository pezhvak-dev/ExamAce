function sendData(question_number, selectedAnswer, slug) {
    $.ajax({
        url: `/course/exam/${slug}/submit/temp/`,
        method: 'POST',
        data: {
            'question_number': question_number,
            'selected_answer': selectedAnswer
        },
        success: function (response) {
            console.log("Success");
        },
        error: function (xhr, status, error) {
            console.log("Error");
        }
    });
}