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
    <title>Наборы Bot-Panel</title>
    <?php include_once 'components/css.php'; ?>
  </head>

  <body id="page-top" class="bg-secondary">
    <?php include_once 'components/header.php'; ?>
    <div id="wrapper">
      <div id="content-wrapper">
        <div class="container-fluid bg-secondary">
          <ol class="breadcrumb bg-dark">
            <li class="breadcrumb-item bg-dark text-success">
              <a>Наборы для продаж</a>
            </li>
          </ol>
          <div class="card mb-3 border border-dark">
            <div class="card-header bg-dark text-success">
              <i class="fas fa-clipboard-check text-success"></i>
              Наборы
            </div>
            <div class="card-body bg-dark">
              <div class="container text-center bg-sondary text-success">
                <div class="table-center pt-4 pb-4 bg-dark">
                  <table class="table table-bordered bg-dark text-success" id="dataTable" width="100%" cellspacing="0">
                    <thead>
                      <tr>
                        <th>Имя Набора</th>
                        <th>Кол-во Токенов</th>
                        <th>Цена</th>
                        <th>Статус</th>
                        <th>Номер бандла</th>
                      </tr>
                    </thead>
                    <tbody>
                      <?php
                      include('inc/config.php');
                      $statement = $db->prepare("SELECT `bundle_name`,`tokens_amount`,`price_amount`,`bundle_status`,`id_bundle_shop` FROM bundle_shop");
                      $statement->execute();
                      $db_bundles = $statement->get_result();

                      #Output data
                      while ($bundlerow = $db_bundles->fetch_array()) {
                        $bundle_status = "";
                        if($bundlerow[3] == 1){
                            $bundle_status = "Активирован";
                        }
                        else{
                            $bundle_status = "Выключен";
                        }
                        echo
                          "<tr><td class='supertable'>", $bundlerow[0],
                          "</td><td class='txt'>", $bundlerow[1],
                          "</td><td class='txt'>", $bundlerow[2],
                          "</td><td class='txt'>", $bundle_status,
                          "</td><td class='txt'>", $bundlerow[4],
                          "</td></tr>";
                      }
                      ?>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <form method="POST" action="server.php" id="Form_tobundle" name="Form_tobundle">
              <div class="card-footer bg-dark">
                <?php include_once 'components/commands_bundles.php'; ?>
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