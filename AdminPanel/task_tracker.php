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
  <!DOCTYPE html>
  <html>

  <head>
    <?php include_once 'components/meta.php'; ?>
    <title>Трекер задач Bot-Panel</title>
    <?php include_once 'components/css.php'; ?>
  </head>

  <body id="page-top" class="bg-secondary">
    <?php include_once 'components/header.php'; ?>
    <div id="wrapper">
      <div id="content-wrapper">
        <div class="container-fluid bg-secondary">
          <ol class="breadcrumb bg-dark">
            <li class="breadcrumb-item bg-dark text-success">
              <a>Трекер задач</a>
            </li>
          </ol>
          <div class="card mb-3 border border-dark">
            <div class="card-header bg-dark text-success">
              <i class="fas fa-clipboard-check text-success"></i>
              Трекер
            </div>
            <div class="card-body bg-dark">
              <div class="container text-center bg-sondary text-success">
                <div class="table-center pt-4 pb-4 bg-dark">
                  <table class="table table-bordered bg-dark text-success" id="dataTable" width="100%" cellspacing="0">
                    <thead>
                      <tr>
                        <th>Задача</th>
                        <th>Имя пользователя</th>
                        <th>Ссылка доказательство</th>
                        <th>Пользователь выполнил задачу</th>
                        <th>Задача была верифицирована</th>
                        <th>Выполнил раз</th>
                      </tr>
                    </thead>
                    <tbody>
                      <?php
                      include("inc/config.php");
                      $statement = $db->prepare("SELECT `task_id_tracker`,`assigned_user`,`answer_field`,`completed`,`verified`,`task_completed_times` FROM task_tracker_2 ORDER BY `tasK_id_tracker`");
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
                            $completed_times = strval($trackerrow[5]) . "/" . strval($taskrow[2]);
                          }
                        }

                        echo
                          "<tr><td class='supertable'>", $trackerrow[0],
                          "</td><td class='txt'>", '@' . $trackerrow[1],
                          "</td><td class='txt'>", $trackerrow[2],
                          "</td><td class='txt'>", $trackerrow[3],
                          "</td><td class='txt'>", $trackerrow[4],
                          "</td><td class='txt'>", $trackerrow[5],
                          #"</td><td class='txt'>", $completed_times,
                          "</td></tr>";
                      }
                      ?>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <?php include_once 'components/footer.php'; ?>

    <?php include_once 'components/js.php'; ?>

    <script src="asset/vendor/datatables/jquery.dataTables.js"></script>
    <script src="asset/vendor/datatables/dataTables.bootstrap4.js"></script>
    <script src="asset/vendor/responsive/dataTables.responsive.js"></script>
    <script src="asset/vendor/responsive/responsive.bootstrap4.js"></script>
    <script src="asset/js/demo/datatables-demo.js"></script>
  </body>

  </html>
<?php } ?>