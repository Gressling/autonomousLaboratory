<?php

// DB
$connStr = getenv('CUSTOMCONNSTR_strConn');
list($host, $dbname, $user, $password) = explode(';', $connStr);
$message = '';
$conn = new mysqli($host, $user, $password, $dbname);
if ($conn->connect_error) {echo ("Connection failed: " . $conn->connect_error);}

$sql = "SELECT * FROM situation.situation2 order by PKey desc limit 20";
$result = $conn->query($sql);

$data = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
}

echo json_encode($data);

?>
