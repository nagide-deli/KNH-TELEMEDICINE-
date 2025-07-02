function getGreeting() {
        let name = "{{ request.user.first_name|escapejs }}"; // Fetch first name from Django
        let hour = new Date().getHours();
        let greetingText = "";

        if (hour < 12) {
            greetingText = `Good Morning, ${name}`;
        } else if (hour < 18) {
            greetingText = `Good Afternoon, ${name}`;
        } else {
            greetingText = `Good Evening, ${name}`;
        }

        document.getElementById("greeting").innerText = greetingText;
    }
    document.addEventListener("DOMContentLoaded", getGreeting); // Ensures DOM is fully loaded before running

    window.onload = getGreeting;