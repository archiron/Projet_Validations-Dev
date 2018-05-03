<!DOCTYPE HTML PUBLIC >
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
<title>releases list webpage</title>
</head>
<h1><center><b><font color=red>electron validation webpage</font></b></center></h1>

<body>
<script>
function recupvaleur() {
   var x = document.getElemlentById("id_test");
}
</script>

<?php
// Affichage de quelque chose comme : Wednesday the 15th
echo date('l, \t\h\e jS M Y') . "<br>";

include '../php_inc/fonctions.inc.php';

echo '<br>';
$web_roots="http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/Releases";
$racine_eos="/eos/project/c/cmsweb/www/egamma/";
$racine_html="http://cms-egamma.web.cern.ch/cms-egamma/";
$image_up="http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/img/up.gif";
$image_point="http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/img/point.gif";

$chemin = $web_roots;

$url =  "//{$_SERVER['HTTP_HOST']}{$_SERVER['REQUEST_URI']}"; # url of the folder in order to use without index.php
$escaped_url = htmlspecialchars( $url, ENT_QUOTES, 'UTF-8' );
$escaped_url = str_replace("/index.php?action=/", "/", $escaped_url);
$classical_roots = htmlspecialchars( $web_roots, ENT_QUOTES, 'UTF-8' );
$classical_roots = str_replace("/index.php?action=/", "/", $classical_roots);
$classical_path = htmlspecialchars( $url, ENT_QUOTES, 'UTF-8' );
$classical_path = str_replace("/index.php?action=/", "/", $classical_path);
$previous_url = dirname($url);

$dirsList = array();
$filesList = array();
$lineHisto = array();
$gifsDir=False;
$indexHtml=False;
$histosFile=False;

$action = (isset($_REQUEST['action']) ? $_REQUEST['action'] : '');
$chemin = $chemin . '/' . $action;
$chemin_eos=str_replace($racine_html, $racine_eos, $chemin);

$files = array_slice(scandir($chemin_eos), 2);

# Fill arrays with dirs & files
foreach ($files as $key => $value) 
{
    if (is_dir($chemin_eos . DIRECTORY_SEPARATOR . $value)) 
    {
        $dirsList[] = $value; 
    }
    elseif (is_file($chemin_eos . DIRECTORY_SEPARATOR . $value)) 
    {
        $filesList[] = $value;
    }
    else
    {
        echo "unknown type : $value<br />";
    }
}

foreach ($dirsList as $key => $value) 
{
    if ( $value == "gifs" )
    {
        $gifsDir = True;
    }
}
foreach ($filesList as $key => $value) 
{
    if ( $value == "index.html" )
    {
        $indexHtml = True;
    }
    # test sur histosFile
    elseif ((stristr($value, "ElectronMcFakeHistos") !== FALSE) and (stristr($value, ".txt") !== FALSE))
    {
        # ElectronMcFakeHistos.txt,
        $histosFile = True;
        $histosFileName = 'ElectronMcFakeHistos.txt';
    }
    elseif ((stristr($value, 'ElectronMcSignalHistos') !== FALSE) and (stristr($value, '.txt') !== FALSE))
    {
        # ElectronMcSignalHistosMiniAOD.txt,
        # ElectronMcSignalHistos.txt,
        # ElectronMcSignalHistosPt1000.txt
        $histosFile = True;
        $histosFileName = $value;
    }
}

if ( $gifsDir and $indexHtml and $histosFile ) # histos web page construction
{
    echo '<form action="" method="post">';
    echo '<table border="0" cellpadding="5" width="20%">';
    echo '<td align="center">';
    echo  '&nbsp;Filter';
    echo '</td>';
    echo '<td align="center"';
    echo '<br>';
    echo '<input type="text" name="choiceValue" id="other_test" onkeyup="recupvaleur()">';
    echo '</td>';
    echo '<td>&nbsp; </td>';
    echo '<td align="center"';
    echo "<br>";
    echo "<a href=\"$url\">Clear filter</a>";
    echo '</td>';
    echo '</table>';
    echo '</form>';

    $choiceValue = $_REQUEST['choiceValue'];
    #$choiceSelected = $_REQUEST['buttonChoice'];
    echo "value  : " . $choiceValue . "<br>";
    
    echo "<br /><a href=\"$web_roots/index.php\">Back to roots</a>";
    echo "$nbsp - $nbsp\n";
    echo "<a href=\"$classical_path\">Classical view (without php).</a>\n";

    $handle = fopen($chemin_eos . "/index.html", "r");
    if ($handle) 
    {
        for ($i = 0; $i <= 5; $i++) {
            $lineRead = fgets($handle);
        }
        $lineRead = fgets($handle);
        $lineRead = str_replace("../../../../img/up.gif", $image_up, $lineRead);
        $lineRead = str_replace("<a href=\"../\">", "<a href='" . $previous_url . "'>", $lineRead);
        echo $lineRead;
        $lineRead = fgets($handle);
        $lineRead = str_replace("<a href=\"gifs/\">", "<a href='" . $escaped_url . "/gifs/'>", $lineRead);
        $lineRead = str_replace("<a href=\"electronCompare.C\">", "<a href='" . $escaped_url . "/electronCompare.C'>", $lineRead);
        $lineRead = str_replace("<a href=\"ElectronMcSignalHistos.txt\">", "<a href='" . $escaped_url . "/ElectronMcSignalHistos.txt'>", $lineRead);
        echo $lineRead;
        fclose($handle);
    } 
    else {
        // error opening the file.
        echo "error while trying to open the index.html file";
    }
    
    $handle_2 = fopen($chemin_eos . "/" . $histosFileName, "r");
    if ($handle_2)
    {
        while(!feof($handle_2)) 
        {
            $lineHisto[] = fgets($handle_2);
        }
        fclose($handle_2);
    
    }

    #echo "remplissage tableau" . "<br>";
    $histoArray_0 = array();
    $key = "";
    $tmp = array();
    foreach ($lineHisto as $line) {
        if ( iconv_strlen($line) == 1 ) # len == 0, empty line
        {
            if ( (iconv_strlen($key) != 0) and (count($tmp) != 0) ) {
                $histoArray_0[strval($key)] = $tmp;
                $key = "";
                $tmp = array();
            } 
        }
        else { # len <> 0
            if ( iconv_strlen($key) == 0 ) {
                $key = $line; # get title
            }
            else {
                $tmp[] = $line; # histo name
                $t1 = explode("/", $line);
                $t2 = $t1[1];
                $short_positions = preg_split("/[\s,]+/", $t2);
                #echo $short_positions[3] . "/" . $short_positions[4] . "<br>";
                if ( $short_positions[3] == 1 ) {
                    $tmp[] = "endLine";
                }
            }
        }
    }
    #echo "fin remplissage" . "<br>";

$clefs_0 = array_keys($histoArray_0);

##### test with Title/Histo name choice
    $histoArray = $histoArray_0;
    $clefs = array_keys($histoArray);
if ( $choiceValue != '' ) {
    for ($i = 0; $i < count($clefs); $i++) {
        if ( stristr($clefs[$i], $choiceValue) != FALSE ) {
            echo $clefs[$i] . "<br>";
        }
        else {
            $j = 0;
            foreach ($histoArray[$clefs[$i]] as $elem ) {
                if ( $elem == "endLine" ) {
                    ;
                }
                elseif ( stristr($elem, $choiceValue) != FALSE ) {
                }
                else {
                    unset($histoArray[$clefs[$i]][$j]);
                }
                $j++;
            }
        }
    }
    echo "<br>";
}
##### end test with Title/Histo name choice

echo "<table border=\"1\" cellpadding=\"5\" width=\"100%\">";
for ($i = 0; $i < count($clefs); $i++) {
    if ( $i % 5  == 0 ) {
        echo "\n<tr valign=\"top\">";
    }
    $textToWrite = "";
    echo "\n<td width=\"10\">\n<b> " . $clefs[$i] . "</b>";
    $titles = explode(" ", $clefs[$i]);
    $titleShortName = $titles[0] . "_" . $titles[1];
    $titleShortName = substr($titleShortName, 0, -1);
    echo "&nbsp;&nbsp;" . "<a href=\"#" . $titleShortName . "\">" ; # write group title
    echo "<img width=\"18\" height=\"15\" border=\"0\" align=\"center\" src=" . $image_point . " alt=\"Top\"/>" . "<br><br>";
    $textToWrite .= "</a>";
    $histoPrevious = "";
    $numLine = 0;
    
    foreach ($histoArray[$clefs[$i]] as $elem) {
        $otherTextToWrite = "";
        $histo_names = explode("/", $elem);
        $histo_name = $histo_names[0];
        $histoShortNames = $histo_names[1];
        $histo_pos = $histoShortNames;
        $histo_positions = preg_split("/[\s,]+/", $histo_pos);
        $short_histo_names = explode(" ", $histoShortNames);
        $short_histo_name = str_replace("h_", "", $short_histo_names[0]);
        if ( stristr($short_histo_name, 'ele_') !== FALSE) {
                $short_histo_name = str_replace("ele_", "", $short_histo_name);
            }
        if ( stristr($short_histo_name, 'scl_') !== FALSE) {
            $short_histo_name = str_replace("scl_", "", $short_histo_name);
        }
        if ( stristr($short_histo_name, 'bcl_') !== FALSE) {
            $short_histo_name = str_replace("bcl_", "", $short_histo_name);
        }

        list ($after, $before, $common) = testExtension($short_histo_name, $histoPrevious); #STOP ICI POUR PYTHON
        print list
        
        if ( $elem == "endLine" ) {
            $otherTextToWrite .= "<br>";
        }
        elseif ( $histo_positions[3] == "0" ) {
            if ($numLine == 0) {
                $otherTextToWrite .= "<a href=\"#" . $short_histo_name . "\"><font color=green>" . $short_histo_name . "</font></a>" . "&nbsp;\n";
                $common = $short_histo_name;
                $numLine += 1;
            }
            else { # $numLine > 0
                if ( $after == "" ) {
                    $otherTextToWrite .= "<a href=\"#" . $short_histo_name . "\"><font color=green>" . $before . "</font></a>" . "&nbsp;\n";
                }
                else{ # $after != ""
                    $otherTextToWrite .= "<a href=\"#" . $short_histo_name . "\"><font color=green>" . $after . "</font></a>" . "&nbsp;\n";
                }
                $common = $before;
            }
        }
        else { #$histo_positions[3] == "1"
            if ($numLine == 0) {
                $otherTextToWrite .= "<a href=\"#" . $short_histo_name . "\"><font color=grey>" . $short_histo_name . "</font></a>" . "&nbsp;\n"; # "<br>\n";
                $common = $short_histo_name;
            }
            else { # $numLine > 0
                if ( $after == "" ) {
                    $otherTextToWrite .= "<a href=\"#" . $short_histo_name . "\"><font color=blue>" . $before . "</font></a>" . "&nbsp;\n"; # "<br>\n";
                }
                else{ # $after != ""
                    $otherTextToWrite .= "<a href=\"#" . $short_histo_name . "\"><font color=blue>" . $after . "</font></a>" . "&nbsp;\n"; # "<br>\n";
                }
            }
            $numLine = 0;
        }

        $histoPrevious = $common;
        
        if ( $histo_positions[4] == "1" ) {
            $otherTextToWrite .= "<br>";
        }
        $otherTextToWrite = str_replace("<br><br>", "<br>", $otherTextToWrite);
        $textToWrite .= $otherTextToWrite ;#. "\n";
    }
    $textReplace = TRUE;
    while ( $textReplace ) {
        $textToWrite = str_replace("<br><br>", "<br>", $textToWrite);
        if ( substr_count($textToWrite, '<br><br>') >= 1 ) {
            $textReplace = TRUE;
        }
        else {
            $textReplace = FALSE;
        }
    }
    if ( substr_count($textToWrite, "</a><br><a") >= 1 ) {
            $textToWrite = str_replace("</a><br><a", "</a><a", $textToWrite);
    }
    echo $textToWrite;
    }
    echo "</td>";
    if ( $i % 5 == 4 ) {
        echo "</tr>";
    }

echo  "</table>\n";
echo "<br>";

$lineFlag = True;
echo "<table border=\"0\" cellpadding=\"5\" width=\"100%\">";
for ($i = 0; $i < count($clefs); $i++) {
    echo "\n<tr valign=\"top\">";
    echo "\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" . $image_up . " alt=\"Top\"/></a></td>\n";
    $titles = explode(" ", $clefs[$i]);
    $titleShortName = $titles[0] . "_" . $titles[1];
    $titleShortName = substr($titleShortName, 0, -1);
    echo "\n<td>\n<b> ";
    echo "<a id=\"" . $titleShortName . "\" name=\"" . $titleShortName . "\"></a>";
    echo $clefs[$i] . "</b></td>";
    echo "</tr><tr valign=\"top\">";
    foreach ($histoArray[$clefs[$i]] as $elem) {
        if ( $elem != "endLine" ) { 
            $histo_names = explode("/", $elem);
            $histo_name = $histo_names[0];
            $histoShortNames = $histo_names[1];
            $histo_pos = $histoShortNames;
            $histo_positions = preg_split("/[\s,]+/", $histo_pos);
            $short_histo_names = explode(" ", $histoShortNames);
            $short_histo_name = str_replace("h_", "", $short_histo_names[0]);
            if ( stristr($short_histo_name, 'ele_') !== FALSE) {
                $short_histo_name = str_replace("ele_", "", $short_histo_name);
            }
            if ( stristr($short_histo_name, 'scl_') !== FALSE) {
                $short_histo_name = str_replace("scl_", "", $short_histo_name);
            }
            $gif_name = $escaped_url . "/gifs/" . $short_histo_names[0] . ".gif"; # ARRET
            if ( $lineFlag ) {
                echo "\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" . $image_up . " alt=\"Top\"/></a></td>\n";
            }
            if (  $histo_positions[3] == "0" ) {
                echo "<td>";
                echo "<a id=\"" . $short_histo_name . "\" name=\"" . $short_histo_name . "\"></a>";
                echo "<a href=\"" . $gif_name . "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" . $gif_name . "\"></a>";
                echo " </td>\n";
                $lineFlag = False;
            }
            else { # line_sp[3]=="1"
                echo "<td>";
                echo "<a id=\"" . $short_histo_name . "\" name=\"" . $short_histo_name . "\"></a>";
                echo "<a href=\"" . $gif_name . "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" . $gif_name . "\"></a>";
                echo "</td></tr><tr valign=\"top\">";
                $lineFlag = True;
            }
        }
    }
}
echo  "</tr></table>\n";

} # end of web page construction of histos
else { # construction of folders list web page 
    foreach ($dirsList as $key => $value)
    {
        echo "<a href='$_SERVER[PHP_SELF]?action=".$action.'/'.$value."'>$value</a><br />";
    } 
} # end of folders list web page construction

echo "<br /><a href=\"$web_roots/index.php\">Back to roots</a>";
echo "$nbsp - $nbsp\n";
echo "<a href=\"$classical_path\">Classical view (without php).</a>";

?>


</body>
</html>
