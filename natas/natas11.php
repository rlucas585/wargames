<?php
function xor_encrypt($in, $key) {
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

function find_xor_key($in) {
    $key = '';
    $text = $in;
    $outText = 'x';
	$firstChars = "{\"showpassword\":\"no\"";
	$testcharbyte = 32;
	$i = 0;
	$keylenfound = 0;

	while ($outText[$i] != $firstChars[$i] && $i < strlen($firstChars))
	{
		$outText = substr($outText, 0, -1);
		$key[$i] = '' . chr($testcharbyte);
		$outText .= $text[$i] ^ $key[$i % strlen($key)];
		if ($outText[$i] == $firstChars[$i]) {
			$outText .= 'x';
			if ($key[0] == chr($testcharbyte) && $i > 0) {
				$testResult = xor_encrypt($text, substr($key, 0, -1));
				if ($testResult[strlen($testResult) - 1] == '}')
					return substr($key, 0, -1);
			}
			$i++;
			continue ;
		}
		$testcharbyte++;
		if ($testcharbyte == 126) {
			$testcharbyte = 32;
		}
	}

    return $key;
}

// $testarray = array( "showpassword"=>"no", "bgcolor"=>"#424242" );
// $jsonArray = json_encode($testarray);
// $testencrypt1 = base64_encode(xor_encrypt($jsonArray, 'Passw!rd'));
// echo $testencrypt1 . "\n";
// $keyValue = find_xor_key(base64_decode(urldecode($testencrypt1)));
// echo $keyValue . "\n";

// $cookiedata = "ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw%3D";
$cookiedata = "ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSQwp%2BQ0MKaAw%3D";

$keyValue = find_xor_key(base64_decode(urldecode($cookiedata)));
echo $keyValue . "\n";

echo xor_encrypt(base64_decode(urldecode($cookiedata)), 'qw8J') . "\n";

$targetarray = array( "showpassword"=>"yes", "bgcolor"=>"#424242" );
echo urlencode(base64_encode(xor_encrypt(json_encode($targetarray), 'qw8J'))) .
	"\n";
?>
