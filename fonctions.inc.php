<?php

function testExtension($histoName, $histoPrevious){

    $after = ""; # $histoName;
    $before = stristr($histoName, '_', true);
    if ( $before == '' ) { # no _ in histo name
        $before = $histoName;
        $common = $histoName;
    }
    else {
        $afters = explode('_', $histoName); # ARRET
        $before = $afters[0];
        $nMax = count($afters);

        if ( $afters[$nMax - 1] == "endcaps" ) {
            $after = "endcaps";
            print "endcaps"
            for ( $i = 1; $i < $nMax-1; $i++) {
                $before .= "_" . $afters[$i];
            }
        }
        elseif ( $afters[$nMax - 1] == "barrel" ) {
            $after = "barrel";
            print "barrel"
            for ( $i = 1; $i < $nMax-1; $i++) {
                $before .= "_" . $afters[$i];
            }
        }
        else {
            print "global"
            if ( $histoPrevious = "" ) {
                $before = $histoName;
                $after = ""; 
                $common = $histoName;
            }
            else {
                $avant =  $afters[0];
                $after = "";
                for ( $i = 1; $i < $nMax-1; $i++) {
                    $avant = $avant . "_" . $afters[$i];
                    if ( $avant == $histoPrevious ) {
                        $before = $avant;
                        $common = $histoPrevious;
                        break;
                    }
                }
                for ( $j = $nMax - $i; $j < $nMax; $j++ ) {
                    $after .= "_" . $afters[$j]; 
                }
                $after = substr($after, 1);
            }
        }

    }

    return array($after, $before, $common);
}

?>

