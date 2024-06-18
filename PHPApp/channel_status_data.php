<?php
$connStr = getenv('CUSTOMCONNSTR_strConn');
list($host, $dbname, $user, $password) = explode(';', $connStr);
$message = '';
$conn = new mysqli($host, $user, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT a.channel, MAX(insert_timestamp) as last_insert_timestamp FROM situation2 a GROUP BY a.channel";
$result = $conn->query($sql);

$data = array();
if ($result->num_rows > 0) {
  while($row = $result->fetch_assoc()) {
    $data[] = $row;
  }
} else {
  echo "0 results";
}
$conn->close();

$response = array(
  'current_time' => date("Y-m-d H:i:s"),
  'data' => $data
);

echo json_encode($response);
?>
