<?php
// Database configuration
$servername = "sql211.infinityfree.com";
$username = "if0_37507235"; // Change to your database username
$password = "662218Zhy";     // Change to your database password
$dbname = "if0_37507235_timetable_db"; // Change to your database name

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$data = file_get_contents('php://input');
$classes = json_decode($data, true);

if (!empty($classes)) {

    $stmt = $conn->prepare("INSERT INTO timetable (subject, day, time, teacher) VALUES (?, ?, ?, ?)");

    foreach ($classes as $class) {
        $subject = $class['subject'];
        $day = $class['day'];
        $time = $class['time'];
        $teacher = $class['teacher'];

        $stmt->bind_param("ssss", $subject, $day, $time, $teacher);

        if (!$stmt->execute()) {
            echo json_encode(['status' => 'error', 'message' => 'Error inserting data: ' . $stmt->error]);
            exit;
        }
    }

    $stmt->close();

    echo json_encode(['status' => 'success', 'message' => 'Data saved successfully!']);
} else {
    echo json_encode(['status' => 'error', 'message' => 'No data received!']);
}

$conn->close();