<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>Admin Panel - Login</title>
    <?php include_once 'components/css.php'; ?>
</head>

<link rel="stylesheet" type="text/css" href="css/inputs.css">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<body class="bg-dark">
    <div class="card-img-overlay">
        <div class="container">
            <div class="card card-login mx-auto bg-secondary mt-5 border-primary">
                <h5 class="card-header text-success border-primary"><strong>Authorization</strong></h5>
                <div class="card-body">
                    <form method="POST" action="phplogin/authenticate.php">

                        <div class="form-group">
                            <input type="text" id="username" name="username"
                                class="form-control bg-dark text-success border-white" placeholder="Username"
                                required="required">
                        </div>
                        <div class="form-group">
                            <input type="password" id="password" name="password"
                                class="form-control bg-dark text-success border-white" placeholder="Password"
                                required="required">
                        </div>
                        <div class="align-content-center text-center">
                        </div>
                        <button type="submit" class="btn btn-primary btn-block text-white border-dark">Login</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</body>

</html>