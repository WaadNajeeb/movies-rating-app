
if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
        navigator.serviceWorker
            .register("static/js/service-worker.js")
            .then((res) => console.log("service worker registered"))
            .catch((err) => console.log("service worker not registered", err));
    });
}



setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => alert.classList.remove('show'));
}, 5000);

document.getElementById("loginBtn")?.addEventListener("click", function () {
    window.location.href = '/auth/login';  // Redirect to the registration page
});


document.addEventListener("DOMContentLoaded", function () {
    const myRatingCustomFeedback = document.getElementById('myRatingResettable');
    const ratingInput = document.getElementById('ratingInput');
    if (myRatingCustomFeedback) {

        myRatingCustomFeedback.addEventListener('change.coreui.rating', event => {
            var ratingValue = event.value;
            ratingInput.value = ratingValue;
        });
    }

    document.getElementById("reviewBtn").addEventListener("click", async function (event) {
        const userExists = await checkUserExists();
        const movieId = document.getElementById("reviewBtn").getAttribute("movie-id");
        if (!userExists) {
            location.reload(true);
            return;
        }
        const reviewExists = await checkReview(movieId);

        if (reviewExists) {
            location.reload(true);
            return;
        }
        const baseUrl = window.location.origin;
        window.location.href = `${baseUrl}/movies/${movieId}/reviews`;
    });

    document.getElementById("movie-card").addEventListener("click", async function (event) {
        const movieId = document.getElementById("reviewBtn").getAttribute("movie-id");
        const baseUrl = window.location.origin;
        window.location.href = `${baseUrl}/movies/${movieId}`;
    });
});

async function checkUserExists() {
    try {
        const response = await fetch('/auth/check_user');
        const data = await response.json();

        return data.LoggedIn;
    } catch (error) {
        console.error("Error checking user:", error);
        return false;
    }
}

async function checkReview(movieId) {
    try {
        const response = await fetch(`/check_review/${movieId}`);
        const data = await response.json();

        return data.exists;
    } catch (error) {
        console.error("Error checking user:", error);
        return false;
    }
}

