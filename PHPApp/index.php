<?php
/* 
require 'session.php'; // Ensure this is the correct path to your session script

if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {
    header('Location: login.php');
    exit;
}

$username = htmlspecialchars($_SESSION['username']);
*/
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../style.css">
    <title>Autonomous Laboratory</title>
</head>

<body>
    <div class="container">
        <h1 class="title">Autonomous Laboratory</h1>
        <div class="links">
            <h2 class="title">System</h2>
                <ul>
                <li><a class="link" target="_blank" href="situation.html">Situation (last 20, refresh 2 sec)</a></li>
                <li><a class="link" target="_blank" href="channel_status.html">Channel status</a></li>
                <li><a class="link" target="_blank" href="https://www.pythonanywhere.com/user/gressling/consoles/34294517/">Bash (private login)</a></li>
                <li><a class="link" target="_blank" href="https://github.com/Gressling/autonomousLaboratory">Github</a></li>
                <li><a class="link" target="_blank" href="https://console.hivemq.cloud/clusters/free/9b15b5bc687c4ecfb410a4fbe8df96b6">MQTT Monitor HiveMQ Bash (private login)</a></li>
                </ul>
        </div>
        <div class="license">MIT Licence - no commercial interest</div>
    </div>
</body>

</html>