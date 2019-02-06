<?php
 
echo "ok";


$indicesServer = array('PHP_SELF',
'argv',
'argc',
'GATEWAY_INTERFACE',
'SERVER_ADDR',
'SERVER_NAME',
'SERVER_SOFTWARE',
'SERVER_PROTOCOL',
'REQUEST_METHOD',
'REQUEST_TIME',
'REQUEST_TIME_FLOAT',
'QUERY_STRING',
'DOCUMENT_ROOT',
'HTTP_ACCEPT',
'HTTP_ACCEPT_CHARSET',
'HTTP_ACCEPT_ENCODING',
'HTTP_ACCEPT_LANGUAGE',
'HTTP_CONNECTION',
'HTTP_HOST',
'HTTP_REFERER',
'HTTP_USER_AGENT',
'HTTPS',
'REMOTE_ADDR',
'REMOTE_HOST',
'REMOTE_PORT',
'REMOTE_USER',
'REDIRECT_REMOTE_USER',
'SCRIPT_FILENAME',
'SERVER_ADMIN',
'SERVER_PORT',
'SERVER_SIGNATURE',
'PATH_TRANSLATED',
'SCRIPT_NAME',
'REQUEST_URI',
'PHP_AUTH_DIGEST',
'PHP_AUTH_USER',
'PHP_AUTH_PW',
'AUTH_TYPE',
'PATH_INFO',
'ORIG_PATH_INFO') ;

$msg = "##################\r\n";
$msg .= "## _SERVER\r\n";
foreach ($indicesServer as $arg) {
    if (isset($_SERVER[$arg])) {
        $msg .= $arg.": " . $_SERVER[$arg] . "\r\n" ;
    }
    else {
        $msg .= $arg.": None\r\n" ;
    }
}

$msg .= "\r\n";

//First you need to create an folder called access and execute chown www-data: access; chmod o+w access
$fp = fopen('access//'.round(microtime(true) * 1000).'.txt', 'w');
fwrite($fp, $msg);
fclose($fp);

// send email
mail("your_email@company.com","Request Received",$msg);

?>
