<?php
$status = session_status();
if ($status == PHP_SESSION_NONE) {
    //There is no active session
    session_start();
}
if (!isset($_SESSION['loggedin'])) {
    header('Location: login_new.php');
    exit;
} else {
    error_reporting(E_ALL);
    ini_set('display_errors', TRUE);
    ini_set('display_startup_errors', TRUE);
    include("inc/config.php");
    function increasePoints($db, $user_id, $add_points)
    {
        $statement = $db->prepare("SELECT `user_points` FROM `users_bot` WHERE `id_users` = '$user_id'");
        $statement->execute();
        $user_points = $statement->get_result();

        while ($pointsrow = $user_points->fetch_array()) {
            $pointsrow[0] += $add_points;

            $statement = $db->prepare("UPDATE `users_bot` SET `user_points` = $pointsrow[0] WHERE `id_users` = '$user_id'");
            $statement->execute();
            break;
        }
    }

    #Get command from user
    if (isset($_POST['cmd']) && $_POST['cmd'] != "" && $_POST['cmd'] != null) {
        $cmd = $_POST['cmd'];
        $cmd = preg_replace("~[\\/:*?'<>|]~", ' ', $cmd);

        # Commands for verify
        //Verify task
        if ($cmd == "cmd_verify_task") {
            $target = $_POST['target_tracker'];
            $verify_status = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['verify_status_input']);
            #task_status approve
            if ($verify_status == 1 || $verify_status == "1") {
                #Get completed times for current task
                $statement = $db->prepare("SELECT `task_completed_times`, `task_id_tracker`, `assigned_user` FROM task_tracker_2 WHERE `completed` = 1 AND `verified`= 0 AND `id_key_task_tracker` = '$target'");
                $statement->execute();
                $completed_times = $statement->get_result();
                while ($completedrow = $completed_times->fetch_array()) {
                    #Get max completed times for this task
                    $statement = $db->prepare("SELECT `task_complete_counter`, `points_reward` FROM tasks_bot WHERE `id_tasks` = '$completedrow[1]'");
                    $statement->execute();
                    $max_times = $statement->get_result();
                    while ($maxcompletedrow = $max_times->fetch_array()) {
                        #If current completed counter less than max counter for task
                        if ($completedrow[0] < $maxcompletedrow[0]) {
                            #New counter completed 
                            $new_counter = $completedrow[0] + 1;
                            #Update completed task counter
                            $statement = $db->prepare("UPDATE `task_tracker_2` SET `task_completed_times` = '$new_counter', `completed` = '0', `verified` = '0' WHERE `id_key_task_tracker` = '$target'");
                            $statement->execute();
                            $update_counter = $statement->get_result();
                            #Give points to user
                            increasePoints($db, $completedrow[2], $maxcompletedrow[1]);
                            #If new counter >= completed counter
                            if ($new_counter >= $maxcompletedrow[0]) {
                                $statement = $db->prepare("UPDATE `task_tracker_2` SET `verified` = '1', `completed` = '1' WHERE `id_key_task_tracker` = '$target'");
                                $statement->execute();
                                $update_counter = $statement->get_result();
                            }
                        } else {
                            #Current complete counter >= to max complete counter
                            $statement = $db->prepare("UPDATE `task_tracker_2` SET `verified` = 1 WHERE `id_key_task_tracker` = '$target'");
                            $statement->execute();
                            $update_counter = $statement->get_result();
                        }
                    }
                }
            }
            #Task_status deny
            else {
                $statement = $db->prepare("UPDATE `task_tracker_2` SET `verified` = '$verify_status', `completed` = 0  WHERE `id_key_task_tracker` = '$target'");
                $statement->execute();
                $verify_update = $statement->get_result();
            }
            header('Location: ' . $url . 'index.php');
        }

        # Commands for tasks
        // Add task
        if ($cmd == "cmd_task_add") {
            #$target = $_POST['target_task'];
            $task_name = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_task_name']);
            $task_counter = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_task_counter']);
            $task_reward = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_task_reward']);
            // Create task to task table
            $statement = $db->prepare("INSERT INTO `tasks_bot` (`task`,`task_complete_counter`,`points_reward`) VALUES ('$task_name', '$task_counter', '$task_reward')");
            $statement->execute();
            $create_task = $statement->get_result();
            // Assign task to all users
            $last_task_id = mysqli_insert_id($db);
            #$last_task_id = $db->lastInsertRowID();
            $statement = $db->prepare("INSERT INTO `task_tracker_2` (`task_id_tracker`,`assigned_user`) SELECT `id_tasks`, `id_users` FROM `tasks_bot` CROSS JOIN `users_bot` WHERE `id_tasks` = '$last_task_id' AND `users_bot`.`signup`='done'");
            $statement->execute();
            $assign_task = $statement->get_result();
            header('Location: ' . $url . 'tasks.php');
        }
        // Edit task
        if ($cmd == "cmd_task_edit") {
            $target = $_POST['target_task'];
            $task_name = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_task_name']);
            $task_counter = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_task_counter']);
            $task_reward = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_task_reward']);
            $statement = $db->prepare("UPDATE `tasks_bot` SET `task` = CASE WHEN COALESCE('$task_name','') = '' THEN `task` ELSE '$task_name' END,
                                                              `task_complete_counter` = CASE WHEN COALESCE('$task_counter','') = '' THEN `task_complete_counter` ELSE '$task_counter' END, 
                                                              `points_reward` = CASE WHEN COALESCE('$task_reward','')='' THEN `points_reward` ELSE '$task_reward' END 
                                                        WHERE `id_tasks` = '$target'");
            $statement->execute();
            $edit_task = $statement->get_result();
            header('Location: ' . $url . 'tasks.php');
        }
        // Delete task
        if ($cmd == "cmd_task_delete") {
            $target = $_POST['target_task'];
            #echo $target;
            if ($target == 'ВСЕ ЗАДАЧИ') {
                $statement = $db->prepare("DELETE FROM tasks_bot");
                $statement->execute();
                $delete_task = $statement->get_result();
            } else {
                $statement = $db->prepare("DELETE FROM tasks_bot WHERE `id_tasks` = '$target'");
                $statement->execute();
                $delete_task = $statement->get_result();
            }
            header('Location: ' . $url . 'tasks.php');
        }

        # Commands for users
        // Add user
        if ($cmd == "cmd_user_add") {
            #$target = $_POST['target_user'];
            $user_tg_id = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_user_tg_id']);
            $user_name = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_user_name']);
            $user_wallet = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_user_wallet']);
            $user_referral = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_user_referral']);
            $user_points = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_user_points']);
            $statement = $db->prepare("INSERT INTO `users_bot` (`tg_id`,`tg_nickname`,`wallet`,`referral_id`,`user_points`) VALUES ('$user_tg_id', '$user_name', '$user_wallet', '$user_referral', '$user_points')");
            $statement->execute();
            $add_user = $statement->get_result();
            header('Location: ' . $url . 'users.php');
        }
        // Edit user
        if ($cmd == "cmd_user_edit") {
            $target = $_POST['target_user'];
            $user_wallet = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_user_wallet']);
            $user_signup = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_user_signup']);
            $user_referral = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_user_referral']);
            $user_points = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_user_points']);
            $user_language = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_user_language']);
            //$statement = $db->prepare("UPDATE `users_bot` SET `wallet` = COALESCE('$user_wallet',`wallet`), `signup` = '$user_signup', `referral_id` = '$user_referral', `user_points` = '$user_points', `language` = '$user_language' WHERE `id_users` = $target");
            $statement = $db->prepare("UPDATE `users_bot` SET   `wallet` = CASE WHEN COALESCE('$user_wallet','') = '' THEN `wallet` ELSE '$user_wallet' END, 
                                                                `signup` = CASE WHEN COALESCE('$user_signup','') = '' THEN `signup` ELSE '$user_signup' END, 
                                                                `referral_id` = CASE WHEN COALESCE('$user_referral','') = '' THEN `referral_id` ELSE '$user_referral' END, 
                                                                `user_points` = CASE WHEN COALESCE('$user_points','') = '' THEN `user_points` ELSE '$user_points' END,
                                                                `language` = CASE WHEN COALESCE('$user_language','') = '' THEN `language` ELSE '$user_language' END
                                                        WHERE `id_users` = '$target'");
            $statement->execute();
            $edit_user = $statement->get_result();
            header('Location: ' . $url . 'users.php');
        }
        // Delete user
        if ($cmd == "cmd_user_delete") {
            $target = $_POST['target_user'];
            #echo $target;
            if ($target == 'ВСЕ ПОЛЬЗОВАТЕЛИ') {
                $statement = $db->prepare("DELETE FROM users_bot");
                $statement->execute();
                $delete_user = $statement->get_result();
            } else {
                $statement = $db->prepare("DELETE FROM users_bot WHERE `id_users` = '$target'");
                $statement->execute();
                $delete_user = $statement->get_result();
            }
            header('Location: ' . $url . 'users.php');
        }

        # Commands for bundles
        // Add user
        if ($cmd == "cmd_bundle_add") {
            $bundle_name = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_bundle_name']);
            $bundle_tokens = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_tokens_amount']);
            $bundle_price = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_price_value']);
            $bundle_status = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['add_bundle_status_input']);
            $statement = $db->prepare("INSERT INTO `bundle_shop` (`bundle_name`,`tokens_amount`,`price_amount`,`bundle_status`) VALUES ('$bundle_name', '$bundle_tokens', '$bundle_price', '$bundle_status')");
            $statement->execute();
            $add_bundle = $statement->get_result();
            header('Location: ' . $url . 'bundles.php');
        }
        // Edit user
        if ($cmd == "cmd_bundle_edit") {
            $target = $_POST['target_bundle'];
            $bundle_name = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_bundle_name']);
            $bundle_tokens = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_tokens_amount']);
            $bundle_price = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_price_value']);
            $bundle_status = preg_replace("~[\\/:*?'<>|]~", ' ', $_POST['edit_bundle_status_input']);
            //$statement = $db->prepare("UPDATE `users_bot` SET `wallet` = COALESCE('$user_wallet',`wallet`), `signup` = '$user_signup', `referral_id` = '$user_referral', `user_points` = '$user_points', `language` = '$user_language' WHERE `id_users` = $target");
            $statement = $db->prepare("UPDATE `bundle_shop` SET   `bundle_name` = CASE WHEN COALESCE('$bundle_name','') = '' THEN `bundle_name` ELSE '$bundle_name' END, 
                                                                    `tokens_amount` = CASE WHEN COALESCE('$bundle_tokens','') = '' THEN `tokens_amount` ELSE '$bundle_tokens' END, 
                                                                    `price_amount` = CASE WHEN COALESCE('$bundle_price','') = '' THEN `price_amount` ELSE '$bundle_price' END, 
                                                                    `bundle_status` = CASE WHEN COALESCE('$bundle_status','') = '' THEN `bundle_status` ELSE '$bundle_status' END
                                                            WHERE `id_bundle_shop` = '$target'");
            $statement->execute();
            $edit_user = $statement->get_result();
            header('Location: ' . $url . 'bundles.php');
        }
        // Delete user
        if ($cmd == "cmd_bundle_delete") {
            $target = $_POST['target_bundle'];
            #echo $target;
            if ($target == 'ВСЕ БАНДЛЫ') {
                $statement = $db->prepare("DELETE FROM bundle_shop");
                $statement->execute();
                $delete_bundle = $statement->get_result();
            } else {
                $statement = $db->prepare("DELETE FROM bundle_shop WHERE `id_bundle_shop` = '$target'");
                $statement->execute();
                $delete_bundle = $statement->get_result();
            }
            header('Location: ' . $url . 'bundles.php');
        }

    } else {
        header('Location: ' . $url . 'index.php');
    }
}
?>