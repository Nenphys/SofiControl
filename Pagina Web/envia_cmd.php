<html>
<head>
	<style>
		body
		{ 
		background: #1975FF ; 
		}
	</style>
</head>
<body>
<?php
  
  $con=mysql_connect("localhost","admin","petrolog");
  $db =Mysql_select_db("sofi",$con);
  
  
  $resultDisp = mysql_query("INSERT INTO Comandos VALUES (1,01,'01".$_POST['cmd']."','0')");
  
  echo "<h1 align='center'>Consola</h1>";
  echo "<br>"; 
  echo "<h2 align='center'><p><b> Comando: 01".$_POST['cmd']."</p></b></h2>";
	sleep(2);
	$result_cmd = mysql_query("SELECT * FROM Comandos");	
	$row = mysql_fetch_row($result_cmd);
		 
	if($row[3] == "0" ){
		echo "No Tenemos Respuesta press F5";
	// no hacermos nada por que no hay respuesta
	}elseif(preg_match('Error',$row[3])){
		echo "<h2 align='center'><p><b> Respuesta: $row[3]: trate con otro comando</p></b>";
		mysql_query("DELETE FROM Comandos");
	}
	else{
		echo "<h2 align='center'><p><b> Respuesta: $row[3]</p></b>";
		mysql_query("DELETE FROM Comandos");
	}
  echo "<a href='consola.html' align='center'> <input type='button' name='boton' value='Comando Nuevo' /> </a>" 
?>
</body>
</html>