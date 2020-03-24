<?php
// $user1 = "user";
$user2 = "user\" OR \"1=1\" UNION SELECT * from * where \"1=1";
$user3 = "natas18\" ; SELECT * from users where \"1=1";
$query = "SELECT * from users where username=\"".$user3."\"" . "\n";
echo $query;
// echo $user2;
// echo "\n";
?>
