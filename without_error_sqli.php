<?php
$server = "localhost";
$username = "recuero";
$password = "recuero123";
$database = "Recuero";

// Conexión a la db
$conn = new mysqli($server, $username, $password, $database);

// Ocultar errores de MySQL para que no muestre nada
mysqli_report(MYSQLI_REPORT_OFF);

$id = $_GET['id'];

echo "[+] Valor introducido: " . $id . "<br>---------------------------------------------------------------------------------------------------------------------------<br>";

$data = mysqli_query($conn, "SELECT username FROM users WHERE id = '$id'");

if ($data) {
    $response = mysqli_fetch_array($data);
    if ($response) {
        echo $response['username'];
    }
}
// Si hay error... no se muestra nada y la web sigue cargando normal
?>
