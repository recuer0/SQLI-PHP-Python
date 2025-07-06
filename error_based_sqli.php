<?php

$server = "localhost";
$username = "user";
$password = "user123";
$database = "Database";

$conn = new mysqli($server, $username, $password, $database);

// Mostrar errores de mysqli
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$id = $_GET['id'];

try {
    $data = mysqli_query($conn, "SELECT username FROM users WHERE id = '$id'");
    $response = mysqli_fetch_array($data);
    echo $response['username'];
} catch (Exception $e) {
    echo "Error SQL: " . $e->getMessage();
}

?>
