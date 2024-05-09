function registerExam(courseId) {
    Swal.fire({
        title: 'ثبت نام',
        text: 'آیا از ثبت نام در آزمون اطمینان دارید؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'بله',
        cancelButtonText: 'خیر',
        cancelButtonColor: '#d33'

    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: 'POST',
                url: `/course/exam/register/`,
                data: {
                    "courseId": courseId
                },
                success: function (response) {
                    Swal.fire({
                        icon: 'success',
                        title: 'ثبت نام در آزمون',
                        text: response.message,
                        confirmButtonText: 'باشه',
                        timer: 3000
                    });
                    window.location.reload();
                },
                error: function (xhr, status, error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'ثبت نام در آزمون',
                        text: xhr.responseJSON.message,
                        confirmButtonText: 'باشه',
                        confirmButtonColor: '#d33',
                        timer: 3000
                    });
                }
            });
        }
    });
}