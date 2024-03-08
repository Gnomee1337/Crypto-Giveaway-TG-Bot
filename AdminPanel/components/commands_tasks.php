<div class="col">
  <div class="card mb-3 border-dark">
    <div class="card-header bg-dark text-success">
      <i class="fas fa-wrench"></i>
      Команды для задач
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
                  <optgroup label="Задачи">
                    <option value="cmd_task_add">Добавить задачу</option>
                    <option value="cmd_task_edit">Изменить задачу</option>
                    <option value="cmd_task_delete">Удалить задачу</option>
                  </optgroup>
                </select>
              </td>
              <!-- Task Number row -->
              <td>
                <?php
                include("inc/config.php");
                $statement = $db->prepare("SELECT `id_tasks` FROM tasks_bot ORDER BY `id_tasks`");
                $statement->execute();
                $task_tracker = $statement->get_result();;

                echo ('<select class="form-control bg-dark text-success" id="target_task" name="target_task" required="required">');
                echo ("<option selected='all'>ВСЕ ЗАДАЧИ</option>");
                echo ("<option disabled selected>Выберите номер задачи</option>");

                #Output tasks id
                while ($taskrow = $task_tracker->fetch_array()) {
                  echo ("<option>" . $taskrow[0] . "</option>");
                }
                ?>
              </td>
              <!-- Execute row -->
              <td>
                <button type="submit" name="Form_totasks" for="Form_totasks"
                  class="btn btn-block btn-success text-dark">
                  Выполнить команду
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- User options -->
        <!-- Create task -->
        <p><input id="add_task_name" type="text" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите имя задачи" name="add_task_name" style="display: none">
          <input id="add_task_counter" type="number" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите кол-во выполнений" name="add_task_counter" style="display: none">
          <input id="add_task_reward" type="number" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите сумму награды" name="add_task_reward" style="display: none">
        </p>
        <!-- Edit task -->
        <p><input id="edit_task_name" type="text" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите имя задачи" name="edit_task_name" style="display: none">
          <input id="edit_task_counter" type="number" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите кол-во выполнений" name="edit_task_counter" style="display: none">
          <input id="edit_task_reward" type="number" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите сумму награды" name="edit_task_reward" style="display: none">
        </p>

        <!-- User options check -->
        <script type="text/javascript">
          var doc = document,
            sel = doc.getElementById('select1'),
            adds1 = doc.getElementById('add_task_name'),
            adds2 = doc.getElementById('add_task_counter'),
            adds3 = doc.getElementById('add_task_reward'),
            adds4 = doc.getElementById('edit_task_name'),
            adds5 = doc.getElementById('edit_task_counter'),
            adds6 = doc.getElementById('edit_task_reward');
          sel.addEventListener('change', function () {
            adds1.style.display = this.value == "cmd_task_add" ? 'block' : 'none';
            adds2.style.display = this.value == "cmd_task_add" ? 'block' : 'none';
            adds3.style.display = this.value == "cmd_task_add" ? 'block' : 'none';
            adds4.style.display = this.value == "cmd_task_edit" ? 'block' : 'none';
            adds5.style.display = this.value == "cmd_task_edit" ? 'block' : 'none';
            adds6.style.display = this.value == "cmd_task_edit" ? 'block' : 'none';
          },
            false);
        </script>
      </div>
    </div>
  </div>
</div>