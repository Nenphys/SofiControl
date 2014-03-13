<html>
<?php
	// Coneccion
	$con=mysql_connect("localhost","admin","petrolog");
	$db =Mysql_select_db("sofi",$con);
	mysql_query("UPDATE Eventos SET dia_de_paro=".$_POST['diaParo']);
	mysql_query("UPDATE Eventos SET hora_paro=".$_POST['horaParo'].$_POST['minutoParo']);
	
	mysql_query("UPDATE Eventos SET dia_de_arranque=".$_POST['diaEncendido']);
	if($_POST[minutoEncendido]<10){
		mysql_query("UPDATE Eventos SET hora_arranque=".$_POST['horaEncendido']."0".$_POST['minutoEncendido']);
	}else{
		mysql_query("UPDATE Eventos SET hora_arranque=".$_POST['horaEncendido'].$_POST['minutoEncendido']);
	}
	mysql_query("UPDATE Eventos SET tx=1");
	if(mysql_affected_rows!=-1){
		sleep(1);
		header('Location: index.php');
		mysql_close($con);
	}else{
		header('Location: error.html');
		mysql_close($con);
	}
	
	
?>
</html>
