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
    ?>
<div class="card mb-3 border-dark">
  <div class="card-header bg-dark text-warning">
    <i class="fas  fa-user-circle text-warning"></i>
    На верификацию
  </div>
  <div class="card-body bg-dark text-success">
    <div class="table-responsive display responsive nowrap bg-dark">
      <table class="table table-bordered table-hover text-success" id="dataTable" width="100%" cellspacing="0">
        <thead>
          <tr>
            <th>Задача</th>
            <th>Имя пользователя</th>
            <th>Ссылка доказательство</th>
            <th>Выполнил раз</th>
            <th>Номер трекера</th>
            <!-- <th>test checkbox</th> -->
          </tr>
        </thead>
        <tbody>
          <?php
          include("inc/config.php");
          $statement = $db->prepare("SELECT `task_id_tracker`,`assigned_user`,`answer_field`,`task_completed_times`,`id_key_task_tracker` FROM task_tracker_2 WHERE `completed` = 1 AND `verified`= 0 ORDER BY `task_id_tracker`");
          $statement->execute();
          $task_tracker = $statement->get_result();

          $statement = $db->prepare("SELECT `id_users`,`tg_nickname` FROM users_bot");
          $statement->execute();
          $db_users = $statement->get_result();

          $statement = $db->prepare("SELECT `id_tasks`,`task`,`task_complete_counter` FROM tasks_bot");
          $statement->execute();
          $db_tasks = $statement->get_result();

          #Output data
          while ($trackerrow = $task_tracker->fetch_array()) {

            #Change db_user_id to nickname
            while ($userrow = $db_users->fetch_array()) {
              if ($userrow[0] == $trackerrow[1])
                $trackerrow[1] = $userrow[1];
            }

            #Max and current Task_Counter
            $completed_times = "";
            while ($taskrow = $db_tasks->fetch_array()) {
              if ($taskrow[0] == $trackerrow[0]) {
                $trackerrow[0] = $taskrow[1];
                $completed_times = strval($trackerrow[3]) . "/" . strval($taskrow[2]);
              }
            }

            #Output in table
            echo
              "<tr><td class='supertable'>", $trackerrow[0],
              "</td><td class='txt'>", '@' . $trackerrow[1],
              "</td><td class='txt'>", $trackerrow[2],
              "</td><td class='txt'>", $completed_times,
              "</td><td class='txt'>", $trackerrow[4],
              // "</td><td>","<input type=\"checkbox\" style=\"text-align:center;\" ng-model=\"x.dedbuffer\">",
              "</td></tr>";
          }
          ?>
        </tbody>
      </table>
    </div>
  </div>
</div>
<?php
}
?>