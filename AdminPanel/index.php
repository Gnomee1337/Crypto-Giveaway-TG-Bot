<?php
$status = session_status();
if($status == PHP_SESSION_NONE){
  //There is no active session
  session_start();
}
if (!isset($_SESSION['loggedin'])) {
  header('Location: login_new.php');
  exit;
} else {
  header('Location: main_panel.php');
  exit;
}
?>