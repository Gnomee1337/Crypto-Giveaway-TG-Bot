<div class="row">
  <div class="col-xl-4 col-sm-6 mb-3">
    <div class="card text-white bg-dark o-hidden h-100">
      <div class="card-body">
        <div class="card-body-icon">
          <i class="fas fa-fw fa-id-card"></i>
        </div>
        <div class="mr-5 text-success text-center">
          Пользователей:
          <?php
          include("inc/config.php");
          $statement = $db->prepare("SELECT COUNT(`id_users`) FROM users_bot");
          $statement->execute();
          $result2 = $statement->get_result();
          $row = $result2->fetch_array();
          echo $row[0];
          ?>
        </div>
      </div>
      <div class="card-footer text-white clearfix small z-1"></div>
    </div>
  </div>

  <div class="col-xl-4 col-sm-6 mb-3">
    <div class="card text-white bg-dark o-hidden h-100">
      <div class="card-body">
        <div class="card-body-icon">
          <i class="fab fa fa-eye"></i>
        </div>
        <div class="mr-5 text-success text-center">
          Задач в трекере:
          <?php
          include("inc/config.php");
          $statement = $db->prepare("SELECT COUNT(`id_key_task_tracker`) FROM task_tracker_2");
          $statement->execute();
          $result2 = $statement->get_result();
          $row = $result2->fetch_array();
          echo $row[0];
          ?>
        </div>
      </div>
      <div class="card-footer text-white clearfix small z-1"></div>
    </div>
  </div>

  <div class="col-xl-4 col-sm-6 mb-3">
    <div class="card text-white bg-dark o-hidden h-100">
      <div class="card-body">
        <div class="card-body-icon">
          <i class="fab fa-fw fa-wpforms"></i>
        </div>
        <div class="mr-5 text-success text-center">
          Уникальных задач:
          <?php
          include("inc/config.php");
          $statement = $db->prepare("SELECT COUNT(`id_tasks`) FROM tasks_bot");
          $statement->execute();
          $result2 = $statement->get_result();
          $row = $result2->fetch_array();
          echo $row[0];
          ?>
        </div>
      </div>
      <div class="card-footer text-white clearfix small z-1"></div>
    </div>
  </div>
</div>