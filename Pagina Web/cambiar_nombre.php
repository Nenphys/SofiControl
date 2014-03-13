<html>
<?php
	// Coneccion
	$con=mysql_connect("localhost","admin","petrolog");
	$db =Mysql_select_db("sofi",$con);
	mysql_query("UPDATE Dispositivo SET nombre_disp='".$_POST['nombre']."'");
	if(mysql_affected_rows!=-1){
		sleep(2);
		header('Location: index.php');
		mysql_close($con);
	}else{
		header('Location: error.html');
		mysql_close($con);
	}
?>
</html>
