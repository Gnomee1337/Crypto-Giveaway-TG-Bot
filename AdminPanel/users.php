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
              <a>База пользователей</a>
            </li>
          </ol>
          <div class="card mb-3 border border-dark">
            <div class="card-header bg-dark text-success">
              <i class="fas fa-clipboard-check text-success"></i>
              Пользователи
            </div>
            <div class="card-body bg-dark">
              <div class="container text-center bg-sondary text-success">
                <div class="table-center pt-4 pb-4 bg-dark">
                  <table class="table table-bordered bg-dark text-success" id="dataTable" width="100%" cellspacing="0">
                    <thead>
                      <tr>
                        <th>Телеграм Никнейм</th>
                        <th>Кошелек</th>
                        <th>Статус регистрации</th>
                        <th>Получил рефералку от</th>
                        <th>Баллы</th>
                        <th>Язык</th>
                        <th>Номер пользователя</th>
                      </tr>
                    </thead>
                    <tbody>
                      <?php
                      include('inc/config.php');
                      $statement = $db->prepare("SELECT `tg_id`,`tg_nickname`,`wallet`,`signup`,`referral_id`,`user_points`,`language`,`id_users` FROM users_bot");
                      $statement->execute();
                      $db_users = $statement->get_result();

                      #Output data
                      while ($usersrow = $db_users->fetch_array()) {

                        // #Change referral_id to nickname
                        // $converted_referral_id = "";
                        //  while ($referralrow = $db_users->fetchArray()) {
                        //    if (strval($referralrow[0]) ==  strval($usersrow[4])){
                        //      #$referralrow[0] = $taskrow[1];
                        //      #$usersrow[4] = $usersrow[1];
                        //      $converted_referral_id = strval($referralrow[1]);
                        //    }
                        // }
                    
                        // #Change referral_id to nickname
                        // $converted_referral_id = "";
                        // while ($referralrow = $db_users->fetchArray()) {
                        //   if (strval($referralrow[0]) == strval($usersrow[4])) {
                        //     #$referralrow[0] = $taskrow[1];
                        //     #$usersrow[4] = $usersrow[1];
                        //     $converted_referral_id = strval($referralrow[1]);
                        //     continue;
                        //   }
                        //   else{
                        //     break;
                        //   }
                        // }
                    
                        echo
                          "<tr><td class='supertable'>", "@" . $usersrow[1],
                          "</td><td class='txt'>", $usersrow[2],
                          "</td><td class='txt'>", $usersrow[3],

                          #"</td><td class='txt'>", $converted_referral_id,
                          "</td><td class='txt'>", $usersrow[4],

                          "</td><td class='txt'>", $usersrow[5],
                          "</td><td class='txt'>", $usersrow[6],
                          "</td><td class='txt'>", $usersrow[7],
                          "</td></tr>";
                      }
                      ?>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <form method="POST" action="server.php" id="Form_tousers" name="Form_tousers">
              <div class="card-footer bg-dark">
                <?php include_once 'components/commands_users.php'; ?>
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