<?php
$status = session_status();
if($status == PHP_SESSION_NONE){
    //There is no active session
    session_start();
}
session_unset();
session_destroy();
// Redirect to the login page:
header('Location: index.php');
?>