<div class="col">
  <div class="card mb-3 border-dark">
    <div class="card-header bg-dark text-success">
      <i class="fas fa-wrench"></i>
      Команды для верификации
    </div>
    <div class="card-body bg-dark">
      <div class="table-responsive pb-4 text-success">
        <table class="table table-bordered text-success" width="100%" cellspacing="0">
          <thead>
            <tr>
              <th>Команды</th>
              <th>Номер задачи</th>
              <th>Выполнить</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <!-- Commands row -->
                <select class="form-control bg-dark text-success" id="select1" name="cmd">
                  <option value="nocommand" selected>Выберите Команду</option>
                  <optgroup label="Верификация">
                    <option value="cmd_verify_task">Верифицировать задачу</option>
                  </optgroup>
                </select>
              </td>
              <!-- Tracker Number row -->
              <td>
                <?php
                include("inc/config.php");
                $statement = $db->prepare("SELECT `task_id_tracker`,`assigned_user`,`answer_field`,`task_completed_times`,`id_key_task_tracker` FROM task_tracker_2 WHERE `completed` = 1 AND `verified`= 0 ORDER BY `task_id_tracker`");
                $statement->execute();
                $task_tracker = $statement->get_result();

                echo ('<select class="form-control bg-dark text-success" id="target_tracker" name="target_tracker" required="required">');
                echo ("<option disabled selected>Выберите номер трекера</option>");
                // echo ("<option selected='all'>ВСЕМ ПОЛЬЗОВАТЕЛЯМ</option>");
                
                #Output users
                while ($trackerrow = $task_tracker->fetch_array()) {
                  echo ("<option>" . $trackerrow[4] . "</option>");
                }
                ?>
              </td>
              <!-- Execute row -->
              <td>
                <button type="submit" name="Form_toverify" for="Form_toverify"
                  class="btn btn-block btn-success text-dark">
                  Изменить статус
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- User options -->
        <p>
          <select id="verify_status_input" class="form-control form-control-sm bg-secondary text-success"
            name="verify_status_input" style="display: none">
            <option value="0" disabled selected>Укажите статус верификации задачи</option>
            <option value="1" class="form-control form-control-sm bg-secondary text-primary">Одобрить</option>
            <option value="0" class="form-control form-control-sm bg-secondary text-danger">Отклонить</option>
          </select>
        </p>
        <!-- User options check -->
        <script type="text/javascript">
          var doc = document,
            sel = doc.getElementById('select1'),
            adds1 = doc.getElementById('verify_status_input');
          sel.addEventListener('change', function () {
            adds1.style.display = this.value == "cmd_verify_task" ? 'block' : 'none';
          },
            false);
        </script>
      </div>
    </div>
  </div>
</div>