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
    <title>Пользователи Bot-Panel</title>
    <?php include_once 'components/css.php'; ?>
  </head>

  <body id="page-top" class="bg-secondary">
    <?php include_once 'components/header.php'; ?>
    <div id="wrapper">
      <div id="content-wrapper">
        <div class="container-fluid bg-secondary">
          <ol class="breadcrumb bg-dark">
            <li class="breadcrumb-item bg-dark text-success">
              <a>База задач</a>
            </li>
          </ol>
          <div class="card mb-3 border border-dark">

            <div class="card-header bg-dark text-success">
              <i class="fas fa-clipboard-check text-success"></i>
              Задачи
            </div>
            <div class="card-body bg-dark">
              <div class="container text-center bg-sondary text-success">
                <div class="table-center pt-4 pb-4 bg-dark">
                  <table class="table table-bordered bg-dark text-success" id="dataTable" width="100%" cellspacing="0">
                    <thead>
                      <tr>
                        <th>Задача</th>
                        <th>Автор задачи</th>
                        <th>Макс. кол-во выполнений</th>
                        <th>Награда за 1 выполнение</th>
                        <th>Номер задачи</th>
                      </tr>
                    </thead>
                    <tbody>
                      <?php
                      include('inc/config.php');
                      $statement = $db->prepare("SELECT `task_author`,`task`,`task_complete_counter`,`points_reward`,`id_tasks` FROM tasks_bot");
                      $statement->execute();
                      $db_tasks = $statement->get_result();

                      $statement = $db->prepare("SELECT `tg_id`,`tg_nickname` FROM users_bot");
                      $statement->execute();
                      $db_users = $statement->get_result();

                      #Output data
                      while ($tasksrow = $db_tasks->fetch_array()) {

                        #Change task_author to nickname
                        $converted_task_author = "";
                        while ($taskauthor = $db_users->fetch_array()) {
                          if (strval($tasksrow[0]) == strval($taskauthor[0]))
                            $tasksrow[0] = "@" . strval($taskauthor[1]);
                        }

                        echo
                          "<tr><td class='supertable'>", $tasksrow[1],
                          "</td><td class='txt'>", $tasksrow[0],
                          "</td><td class='txt'>", $tasksrow[2],
                          "</td><td class='txt'>", $tasksrow[3],
                          "</td><td class='txt'>", $tasksrow[4],
                          "</td></tr>";
                      }
                      ?>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <form method="POST" action="server.php" id="Form_totasks" name="Form_totasks">
              <div class="card-footer bg-dark">
                <?php include_once 'components/commands_tasks.php'; ?>
              </div>
            </form>
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