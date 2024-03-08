<div class="col">
  <div class="card mb-3 border-dark">
    <div class="card-header bg-dark text-success">
      <i class="fas fa-wrench"></i>
      Команды для пользователей
    </div>
    <div class="card-body bg-dark">
      <div class="table-responsive pb-4 text-success">
        <table class="table table-bordered text-success" width="100%" cellspacing="0">
          <thead>
            <tr>
              <th>Команды</th>
              <th>Номер пользователя</th>
              <th>Выполнить</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <!-- Commands row -->
                <select class="form-control bg-dark text-success" id="select1" name="cmd">
                  <option value="nocommand" selected>Выберите Команду</option>
                  <optgroup label="Пользователи">
                    <option value="cmd_user_add">Добавить пользователя</option>
                    <option value="cmd_user_edit">Изменить пользователя</option>
                    <option value="cmd_user_delete">Удалить пользователя</option>
                  </optgroup>
                </select>
              </td>
              <!-- User Number row -->
              <td>
                <?php
                include("inc/config.php");
                $statement = $db->prepare("SELECT `id_users` FROM users_bot ORDER BY `id_users`");
                $statement->execute();
                $task_tracker = $statement->get_result();

                echo ('<select class="form-control bg-dark text-success" id="target_user" name="target_user" required="required">');
                echo ("<option selected='all'>ВСЕ ПОЛЬЗОВАТЕЛИ</option>");
                echo ("<option disabled selected>Выберите номер пользователя</option>");

                #Output users id
                while ($userrow = $task_tracker->fetch_array()) {
                  echo ("<option>" . $userrow[0] . "</option>");
                }
                ?>
              </td>
              <!-- Execute row -->
              <td>
                <button type="submit" name="Form_tousers" for="Form_tousers"
                  class="btn btn-block btn-success text-dark">
                  Выполнить команду
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- User options -->
        <!-- Create user -->
        <p><input id="add_user_tg_id" type="number" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите tg_id пользователя" name="add_user_tg_id" style="display: none">
          <input id="add_user_name" type="text" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите ник пользователя" name="add_user_name" style="display: none">
          <input id="add_user_wallet" type="text" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите кошелек пользователя" name="add_user_wallet" style="display: none">
          <input id="add_user_referral" type="number" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите реферальный ид пользователя" name="add_user_referral" style="display: none">
          <input id="add_user_points" type="number" class="form-control form-control-sm bg-secondary text-success"
            placeholder="Укажите сумму поинтов пользователя" name="add_user_points" style="display: none">
        </p>
        <!-- Edit task -->
        <input id="edit_user_wallet" type="text" class="form-control form-control-sm bg-secondary text-success"
          placeholder="Укажите кошелек пользователя" name="edit_user_wallet" style="display: none">
        <select id="edit_user_signup" class="form-control form-control-sm bg-secondary text-success"
          name="edit_user_signup" style="display: none">
          <option value="captcha" disabled selected>Укажите статус регистрации пользователя</option>
          <option value="captcha">captcha</option>
          <option value="balance">balance</option>
          <option value="reaction">reaction</option>
          <option value="invite_friend">invite_friend</option>
          <option value="wallet">wallet</option>
          <option value="done">done</option>
        </select>
        <input id="edit_user_referral" type="number" class="form-control form-control-sm bg-secondary text-success"
          placeholder="Укажите реферальный ид пользователя" name="edit_user_referral" style="display: none">
        <input id="edit_user_points" type="number" class="form-control form-control-sm bg-secondary text-success"
          placeholder="Укажите сумму поинтов пользователя" name="edit_user_points" style="display: none">
        <select id="edit_user_language" class="form-control form-control-sm bg-secondary text-success"
          placeholder="Укажите язык пользователя" name="edit_user_language" style="display: none">
          <option value="ru" disabled selected>Укажите язык пользователя</option>
          <option value="ru">ru</option>
          <option value="en">en</option>
        </select>
        </p>

        <!-- User options check -->
        <script type="text/javascript">
          var doc = document,
            sel = doc.getElementById('select1'),
            //Add user
            adds1 = doc.getElementById('add_user_tg_id'),
            adds2 = doc.getElementById('add_user_name'),
            adds3 = doc.getElementById('add_user_wallet'),
            adds4 = doc.getElementById('add_user_referral'),
            adds5 = doc.getElementById('add_user_points'),

            //Edit user
            adds6 = doc.getElementById('edit_user_wallet'),
            adds7 = doc.getElementById('edit_user_signup'),
            adds8 = doc.getElementById('edit_user_referral'),
            adds9 = doc.getElementById('edit_user_points'),
            adds10 = doc.getElementById('edit_user_language');
          sel.addEventListener('change', function () {
            //Add
            adds1.style.display = this.value == "cmd_user_add" ? 'block' : 'none';
            adds2.style.display = this.value == "cmd_user_add" ? 'block' : 'none';
            adds3.style.display = this.value == "cmd_user_add" ? 'block' : 'none';
            adds4.style.display = this.value == "cmd_user_add" ? 'block' : 'none';
            adds5.style.display = this.value == "cmd_user_add" ? 'block' : 'none';

            //Edit
            adds6.style.display = this.value == "cmd_user_edit" ? 'block' : 'none';
            adds7.style.display = this.value == "cmd_user_edit" ? 'block' : 'none';
            adds8.style.display = this.value == "cmd_user_edit" ? 'block' : 'none';
            adds9.style.display = this.value == "cmd_user_edit" ? 'block' : 'none';
            adds10.style.display = this.value == "cmd_user_edit" ? 'block' : 'none';
          },
            false);
        </script>
      </div>
    </div>
  </div>
</div>