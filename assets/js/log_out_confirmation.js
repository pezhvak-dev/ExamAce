document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.querySelector('.logout-button');

    if (logoutButton) {
        logoutButton.addEventListener('click', function (e) {
            e.preventDefault();

            Swal.fire({
                title: 'خروج از حساب',
                text: 'آیا از خروج خود اطمینان دارید؟',
                icon: 'warning',
                showCancelButton: true,
                cancelButtonColor: '#d33',
                confirmButtonText: 'بله',
                cancelButtonText: 'خیر'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = logoutButton.parentElement.getAttribute('href');
                }
            });
        });
    }
});