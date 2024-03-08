<?php
session_start();
include("../inc/config.php");

// Now we check if the data from the login form was submitted, isset() will check if the data exists.
if (!isset($_POST['username'], $_POST['password'])) {
    // Could not get the data that should have been sent.
    exit('Please fill both the username and password fields!');
} else {
    $username = $_POST['username'];
    $statement = $db->prepare("SELECT `id_accs`,`accs_password` FROM panel_accounts WHERE `accs_username` = '$username'");
    $statement->execute();
    $result = $statement->get_result();

    while ($accounts = $result->fetch_array())
        if (!empty($accounts)) {
            $id = $accounts[0];
            $password = $accounts[1];
            if (password_verify($_POST['password'], $password)) {
                session_regenerate_id();
                $_SESSION['loggedin'] = TRUE;
                $_SESSION['name'] = $_POST['username'];
                $_SESSION['id'] = $id;
                header('Location: ../index.php');
            } else {
                // Incorrect password
                echo 'Incorrect use rname and/or password!';
                header('Location: ../login_new.php');
            }
        } else {
            // Incorrect username
            echo 'Incorrect username and/or password!';
            #break;
            header('Location: ../login_new.php');
        }
}
?>