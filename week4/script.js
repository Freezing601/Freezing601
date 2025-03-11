let timetable = [];

function addClass() {
    const subject = document.getElementById('subject').value;
    const day = document.getElementById('day').value;
    const time = document.getElementById('time').value;
    const teacher = document.getElementById('teacher').value;
    if (subject && day && time && teacher) {
        const newClass = { subject, day, time, teacher };
        timetable.push(newClass);
        displayTimetable();
        localStorage.setItem('timetable', JSON.stringify(timetable));
    } else {
        alert('Please fill all fields');
    }
    document.getElementById('timetableForm').reset();
}

function displayTimetable() {
    const list = document.getElementById('timetableList');
    list.innerHTML = '';
    timetable.forEach((item, index) => {
        const li = document.createElement('li');
        li.textContent = `${item.subject} - ${item.day} - ${item.time} - ${item.teacher}`;
        li.onclick = () => {
            timetable.splice(index, 1);
            displayTimetable();
            localStorage.setItem('timetable', JSON.stringify(timetable));
        };
        list.appendChild(li);
    });
}

function exportToMySQL() {
    const data = JSON.stringify(timetable);
    fetch('save.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: data
    }).then(response => response.json()).then(result => {
        alert(result.message);
    }).catch(error => {
        console.error('Error:', error);
    });
}

window.onload = () => {
    const storedTimetable = localStorage.getItem('timetable');
    if (storedTimetable) {
        timetable = JSON.parse(storedTimetable);
        displayTimetable();
    }
};