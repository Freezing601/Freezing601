<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timetable Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        tr:hover {
            background-color: #f1f1f1;
        }

        @media screen and (max-width: 600px) {
            table, thead, tbody, th, td, tr {
                display: block;
            }

            th, td {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <h1>Timetable Data</h1>
    <?php
    // Here is the code to read data from the database and display it
    // Sample code, please modify according to the actual situation
    $servername = "sql211.infinityfree.com";
    $username = "if0_37507235";
    $password = "662218Zhy";
    $dbname = "if0_37507235_timetable_db";

    // Create a connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check the connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $sql = "SELECT subject, day, time, teacher FROM timetable";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        echo "<table>";
        echo "<thead><tr><th>Subject</th><th>Day</th><th>Time</th><th>Teacher</th></tr></thead>";
        echo "<tbody>";
        while($row = $result->fetch_assoc()) {
            echo "<tr><td>".$row["subject"]."</td><td>".$row["day"]."</td><td>".$row["time"]."</td><td>".$row["teacher"]."</td></tr>";
        }
        echo "</tbody></table>";
    } else {
        echo "No data found";
    }
    $conn->close();
    ?>
</body>
</html>