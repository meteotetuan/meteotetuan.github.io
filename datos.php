<?php
// Permitir que tu página HTML lea este archivo
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

$archivo_cache = "cache_meteo.json";
$tiempo_espera = 600; // 10 minutos en segundos

// 1. Buscamos el archivo clave.txt en el servidor
$archivo_clave = "clave.txt";
if (!file_exists($archivo_clave)) {
    die(json_encode(["error" => "Falta el archivo clave.txt en el servidor"]));
}
$mi_clave = trim(file_get_contents($archivo_clave));

// 2. Construimos la URL uniendo la base con tu clave secreta
$url = "https://www.climameteoinfo.com/bd/api.php?id_est=MAD_232106844758&key=bb46a5b59a796bcca0e2f576de0834b8a280b708bd71d66253ba5f8a79f460e4&format=json" . $mi_clave . "&format=json";

// 3. Sistema para no gastar tus 144 llamadas diarias
if (file_exists($archivo_cache) && (time() - filemtime($archivo_cache) < $tiempo_espera)) {
    echo file_get_contents($archivo_cache);
} else {
    $json = file_get_contents($url);
    if ($json !== false) {
        file_put_contents($archivo_cache, $json);
    }
    echo $json;
}
?>