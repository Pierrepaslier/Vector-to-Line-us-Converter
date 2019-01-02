<?php
/**
 * Invoke the script with a filename to parse:
 *
 *     php script.php test.plt
 */

if (!isset($argv[1])) {
    echo 'Please provide a file name an argument, for example:' . PHP_EOL;
    echo 'php script.php test.plt' . PHP_EOL;
    exit(1);
}

$filename = $argv[1];

if (!file_exists($filename)) {
    echo "The file $filename does not exist" . PHP_EOL;
    exit(1);
}

// Read the file
$fileContent = file_get_contents($filename);

// Write header
echo "G54 X437 Y574 S0.1" . PHP_EOL;


// Split on the ';' separator
$instructions = explode(';', $fileContent);

foreach ($instructions as $instruction) {
    if (empty($instruction) || ($instruction == 'IN')) {
        // Ignore empty lines and IN
        continue;
    }

    // 2 first characters
    $penAction = substr($instruction, 0, 2);
    if ($penAction == 'PU') {
        // Pen UP
        $penAction   = 'Z1000';
        $coordinates = substr($instruction, 2);
        if (empty($coordinates)) {
            // No coordinates?
            echo 'G01 ' . $penAction . PHP_EOL;
            continue;
        }
        $coordinates = explode(',', $coordinates);

        $x = $coordinates[0];
        $y = $coordinates[1];
        echo 'G01 X' . $x . ' Y' . $y . ' ' . $penAction . PHP_EOL;
        $penAction = 'Z0';
        echo 'G01 X' . $x . ' Y' . $y . ' ' . $penAction . PHP_EOL;


    } else {
        // Pen DOWN
        $penAction = 'Z0';


        $coordinates = substr($instruction, 2);
        if (empty($coordinates)) {
            // No coordinates?
            echo 'G01 ' . $penAction . PHP_EOL;
            continue;
        }
        $coordinates = explode(',', $coordinates);

        $x = $coordinates[0];
        $y = $coordinates[1];

        echo 'G01 X' . $x . ' Y' . $y . ' ' . $penAction . PHP_EOL;
    }
}
