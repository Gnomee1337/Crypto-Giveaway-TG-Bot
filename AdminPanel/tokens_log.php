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
    <title>Транзации Bot-Panel</title>
    <?php include_once 'components/css.php'; ?>
  </head>

  <body id="page-top" class="bg-secondary">
    <?php include_once 'components/header.php'; ?>
    <div id="wrapper">
      <div id="content-wrapper">
        <div class="container-fluid bg-secondary">
          <ol class="breadcrumb bg-dark">
            <li class="breadcrumb-item bg-dark text-success">
              <a>История транзакций</a>
            </li>
          </ol>
          <div class="card mb-3 border border-dark">
            <div class="card-header bg-dark text-success">
              <i class="fas fa-clipboard-check text-success"></i>
              Транзакци
            </div>
            <div class="card-body bg-dark">
              <div class="container text-center bg-sondary text-success">
                <div class="table-center pt-4 pb-4 bg-dark">
                  <table class="table table-bordered bg-dark text-success" id="dataTable" width="100%" cellspacing="0">
                    <thead>
                      <tr>
                        <th>Телеграм Никнейм</th>
                        <th>Сумма покупки</th>
                        <th>Токенов куплено</th>
                        <th>Номер покупки</th>
                      </tr>
                    </thead>
                    <tbody>
                      <?php
                      include('inc/config.php');
                      $statement = $db->prepare("SELECT `id_payment_user`,`payment_sum`,`points_bought`,`id_payment_log` FROM payment_logs");
                      $statement->execute();
                      $db_transaction = $statement->get_result();

                      $statement = $db->prepare("SELECT `tg_id`,`tg_nickname` FROM users_bot");
                      $statement->execute();
                      $db_users = $statement->get_result();

                      #Output data
                      while ($transactionrow = $db_transaction->fetch_array()) {

                        #Change tg_id to tg_nickname
                        while ($userrow = $db_users->fetch_array()) {
                          if ($userrow[0] == $transactionrow[0])
                            $transactionrow[0] = $userrow[1];
                        }
                    
                        echo
                          "<tr><td class='supertable'>", "@" . $transactionrow[0],
                          "</td><td class='txt'>", $transactionrow[1],
                          "</td><td class='txt'>", $transactionrow[2],

                          "</td><td class='txt'>", $transactionrow[3],
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