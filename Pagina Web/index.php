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
  mysql_query("UPDATE Eventos SET refresh=1");
  sleep(2);
  
  
  
  //Resultado del Nombre de la estacion;
  $resultDisp = mysql_query("SELECT nombre_disp FROM Dispositivo");
  while($row = mysql_fetch_array($resultDisp)){
  echo "<h1 align='center'>Nombre de Estaci&oacute;n: $row[0]<h1>";
  echo "<br>";
  } 
  //Resultado del estado del motor.
  $resultEdo = mysql_query("SELECT estado FROM Estado");
  while($row = mysql_fetch_array($resultEdo)){
  if($row[0]=="0"){
	echo "<h2 align='center'>Estado: Apagado<h1>";
	echo "<br>";
  }
  else{
	echo "<h2 align='center'>Estado: Prendido<h1>";
	echo "<br>";
  }
  
  }
 
 
 //Resultado de la configuracion Actual
 $resultConf = mysql_query("SELECT * FROM Eventos");
  echo "<h3>";
  echo "<table border='1' align='center'>
  <tr>
  <th>Fecha de Apagado</th>
  <th>Fecha de Encendido</th>
  </tr>";
  while($row = mysql_fetch_array($resultConf)){
switch ($row[2]) {
  case 1:
      $diaParo ="Domingo";
      break;
  case 2:
      $diaParo ="Lunes";
      break;
  case 3:
      $diaParo ="Martes";
      break;
case 4:
      $diaParo ="Miercoles";
      break;
  case 5:
      $diaParo ="Jueves";
      break;
  case 6:
      $diaParo ="Viernes";
      break;
  case 7:
      $diaParo ="Sabado";
      break;
  }
switch ($row[4]) {
  case 1:
      $diaEncendido ="Domingo";
      break;
  case 2:
      $diaEncendido ="Lunes";
      break;
  case 3:
      $diaEncendido ="Martes";
      break;
case 4:
      $diaEncendido ="Miercoles";
      break;
  case 5:
      $diaEncendido ="Jueves";
      break;
  case 6:
      $diaEncendido ="Viernes";
      break;
  case 7:
      $diaEncendido ="Sabado";
      break;
}
  echo "<tr>";
  $minp			= substr($row['hora_paro'], -2);
  $hrp 			= substr($row['hora_paro'], 0,2);
  
  $minA 		= substr($row['hora_arranque'], -2);
  $hrA 			= substr($row['hora_arranque'], 0,2);
  
  echo "<td>".$diaParo." ".$hrp.":".$minp."</td>";
  echo "<td>" .$diaEncendido." ".$hrA.":".$minA. "</td>";
  echo "</tr>";
  }
  echo "</table>";
  echo "</h3>";
  
  echo "<form name='editar'  action='editar_parametros.html' method='POST'>";
	echo "<div name='algo' align='center'>";
		echo "<input type='submit'  id='botonEditar' type='button' value = 'Editar'/>";
	echo "</div>";
  echo "</form>";
  
  mysql_close($con);
?>
</body>
</html>