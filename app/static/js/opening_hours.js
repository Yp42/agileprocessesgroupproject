
document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name^="day_open"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const day = checkbox.name.split('[')[1].split(']')[0];
            const openInput = document.querySelector(`input[name="${day.toLowerCase()}_open"]`);
            const closeInput = document.querySelector(`input[name="${day.toLowerCase()}_close"]`);
            if (checkbox.checked) {
                openInput.disabled = false;
                closeInput.disabled = false;
            } else {
                openInput.disabled = true;
                closeInput.disabled = true;
                openInput.value = '';
                closeInput.value = '';
            }
        });
    });
});