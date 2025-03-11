<?php
// Database configuration
$servername = "sql211.infinityfree.com";
$username = "if0_37507235"; // Change to your database username
$password = "662218Zhy";    // Change to your database password
$dbname = "if0_37507235_timetable_db"; // Change to your database name

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM timetable";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "Subject: " . $row["subject"]. " - Day: " . $row["day"]. " - Time: " . $row["time"]. " - Teacher: " . $row["teacher"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>