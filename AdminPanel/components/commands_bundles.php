<div class="col">
    <div class="card mb-3 border-dark">
        <div class="card-header bg-dark text-success">
            <i class="fas fa-wrench"></i>
            Команды для бандлов
        </div>
        <div class="card-body bg-dark">
            <div class="table-responsive pb-4 text-success">
                <table class="table table-bordered text-success" width="100%" cellspacing="0">
                    <thead>
                        <tr>
                            <th>Команды</th>
                            <th>Номер бандла</th>
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
                                        <option value="cmd_bundle_add">Добавить бандл</option>
                                        <option value="cmd_bundle_edit">Изменить бандл</option>
                                        <option value="cmd_bundle_delete">Удалить бандл</option>
                                    </optgroup>
                                </select>
                            </td>
                            <!-- Bundle Number row -->
                            <td>
                                <?php
                                include("inc/config.php");
                                $statement = $db->prepare("SELECT `id_bundle_shop` FROM bundle_shop ORDER BY `id_bundle_shop`");
                                $statement->execute();
                                $bundles = $statement->get_result();

                                echo ('<select class="form-control bg-dark text-success" id="target_bundle" name="target_bundle" required="required">');
                                echo ("<option selected='all'>ВСЕ БАНДЛЫ</option>");
                                echo ("<option disabled selected>Выберите номер бандла</option>");

                                #Output bundle id
                                while ($bundlerow = $bundles->fetch_array()) {
                                    echo ("<option>" . $bundlerow[0] . "</option>");
                                }
                                ?>
                            </td>
                            <!-- Execute row -->
                            <td>
                                <button type="submit" name="Form_tobundle" for="Form_tobundle"
                                    class="btn btn-block btn-success text-dark">
                                    Выполнить команду
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <!-- Bundle options -->
                <!-- Create bundle -->
                <p><input id="add_bundle_name" type="text"
                        class="form-control form-control-sm bg-secondary text-success" placeholder="Укажите имя бандла"
                        name="add_bundle_name" style="display: none">
                    <input id="add_tokens_amount" type="number"
                        class="form-control form-control-sm bg-secondary text-success"
                        placeholder="Укажите кол-во токенов" name="add_tokens_amount" style="display: none">
                    <input id="add_price_value" type="number"
                        class="form-control form-control-sm bg-secondary text-success" placeholder="Укажите цену бандла"
                        name="add_price_value" style="display: none">
                    <select id="add_bundle_status_input" class="form-control form-control-sm bg-secondary text-success"
                        name="add_bundle_status_input" style="display: none">
                        <option value="0" disabled selected>Укажите статус бандла</option>
                        <option value="1" class="form-control form-control-sm bg-secondary text-primary">Активировать
                        </option>
                        <option value="0" class="form-control form-control-sm bg-secondary text-danger">Выключить
                        </option>
                    </select>
                </p>
                <!-- Edit bundle -->
                <p><input id="edit_bundle_name" type="text"
                        class="form-control form-control-sm bg-secondary text-success" placeholder="Укажите имя бандла"
                        name="edit_bundle_name" style="display: none">
                    <input id="edit_tokens_amount" type="number"
                        class="form-control form-control-sm bg-secondary text-success"
                        placeholder="Укажите кол-во токенов" name="edit_tokens_amount" style="display: none">
                    <input id="edit_price_value" type="number"
                        class="form-control form-control-sm bg-secondary text-success" placeholder="Укажите цену бандла"
                        name="edit_price_value" style="display: none">
                    <select id="edit_bundle_status_input" class="form-control form-control-sm bg-secondary text-success"
                        name="edit_bundle_status_input" style="display: none">
                        <option value="0" disabled selected>Укажите статус бандла</option>
                        <option value="1" class="form-control form-control-sm bg-secondary text-primary">Активировать
                        </option>
                        <option value="0" class="form-control form-control-sm bg-secondary text-danger">Выключить
                        </option>
                    </select>
                </p>

                <!-- Bundle options check -->
                <script type="text/javascript">
                    var doc = document,
                        sel = doc.getElementById('select1'),
                        adds1 = doc.getElementById('add_bundle_name'),
                        adds2 = doc.getElementById('add_tokens_amount'),
                        adds3 = doc.getElementById('add_price_value'),
                        adds4 = doc.getElementById('add_bundle_status_input'),
                        adds5 = doc.getElementById('edit_bundle_name'),
                        adds6 = doc.getElementById('edit_tokens_amount'),
                        adds7 = doc.getElementById('edit_price_value'),
                        adds8 = doc.getElementById('edit_bundle_status_input');
                    sel.addEventListener('change', function () {
                        adds1.style.display = this.value == "cmd_bundle_add" ? 'block' : 'none';
                        adds2.style.display = this.value == "cmd_bundle_add" ? 'block' : 'none';
                        adds3.style.display = this.value == "cmd_bundle_add" ? 'block' : 'none';
                        adds4.style.display = this.value == "cmd_bundle_add" ? 'block' : 'none';
                        adds5.style.display = this.value == "cmd_bundle_edit" ? 'block' : 'none';
                        adds6.style.display = this.value == "cmd_bundle_edit" ? 'block' : 'none';
                        adds7.style.display = this.value == "cmd_bundle_edit" ? 'block' : 'none';
                        adds8.style.display = this.value == "cmd_bundle_edit" ? 'block' : 'none';
                    },
                        false);
                </script>
            </div>
        </div>
    </div>
</div>