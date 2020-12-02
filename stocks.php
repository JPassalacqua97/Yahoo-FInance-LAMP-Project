<html>
<body>

<?php

echo '<body style="background-color:grey">';
$conn = new mysqli("localhost", "cs288","cs288pwd", "stocks");

$table = "yahoo_2020_12_02_11_36_45";

echo("<h2><font color=\"purple\">Table: $table </font></h2>\n");

$result = $conn->query("SELECT * From $table");

$table_attrs = "border='1'";

$ncol = mysqli_num_fields($result);

echo("<h3> Connected to database! </h3>");
echo("number of columns = $ncol");
$table_attrs = "border='1'";

echo("<table $table_attrs>");
echo("<tr>");

while($field = $result->fetch_field()){
  $field_name = $field->name;
  echo("<th>$field_name</th>");
}

echo("</tr>");


while($row = $result->fetch_array()){
  echo("<tr>");
  for($col=0; $col < $ncol; $col++){
      echo("<td>$row[$col]</td>");
  }
  echo("</tr>");
}
echo("</table>");


?>
</body>
</html>
