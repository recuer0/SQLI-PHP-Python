<?php

$server = "localhost";
$username = "recuero";
$password = "recuero123";
$database = "Recuero";

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
