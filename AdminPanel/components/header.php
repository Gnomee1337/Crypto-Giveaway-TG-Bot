<nav class="navbar navbar-expand-lg  navbar-dark bg-dark">
  <a class="navbar-brand mr-1 text-success" href="index.php"><img src="favico.png" width="30" height="30" alt="">Админ
    Панель Бота</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav"
    aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav ml-auto">

      <li class="nav-item <?php if (strpos(urlencode(htmlentities($_SERVER['REQUEST_URI'])), "index.php")) {
        echo ("active");
      } ?>">
        <a class="nav-link text-success" href="index.php"><span class="fa fa-home"></span> Главная</a>
      </li>

      <li class="nav-item <?php if (strpos(urlencode(htmlentities($_SERVER['REQUEST_URI'])), "task_tracker.php")) {
        echo ("active");
      } ?>">
        <a class="nav-link text-success" href="task_tracker.php"><span class="fa fa-eye"></span> Трекер задач</a>
      </li>

      <li class="nav-item <?php if (strpos(urlencode(htmlentities($_SERVER['REQUEST_URI'])), "users.php")) {
        echo ("active");
      } ?>">
        <a class="nav-link text-success" href="users.php"><span class="fa fa-id-card"></span> Пользователи</a>
      </li>

      <li class="nav-item <?php if (strpos(urlencode(htmlentities($_SERVER['REQUEST_URI'])), "tasks.php")) {
        echo ("active");
      } ?>">
        <a class="nav-link text-success" href="tasks.php"><span class="fab fa-wpforms"></span> Задачи</a>
      </li>

      <li class="nav-item <?php if (strpos(urlencode(htmlentities($_SERVER['REQUEST_URI'])), "tasks.php")) {
        echo ("active");
      } ?>">
        <a class="nav-link text-success" href="tokens_log.php"><span class="fa fa-shopping-bag"></span> Транзакции</a>
      </li>

      <li class="nav-item <?php if (strpos(urlencode(htmlentities($_SERVER['REQUEST_URI'])), "tasks.php")) {
        echo ("active");
      } ?>">
        <a class="nav-link text-success" href="bundles.php"><span class="fa fa-shopping-bag"></span> Бандлы</a>
      </li>

      <li class="nav-item">
        <a class="nav-link text-success" data-toggle="modal" data-target="#logoutModal"><span
            class="fa fa-sign-out-alt"></span>Выйти</a>
      </li>
    </ul>
  </div>
</nav>