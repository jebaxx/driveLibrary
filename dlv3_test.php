<?php
    include "driveLibraryV3.php";

    $parent =  "0BwEMWPU5Jp9SN0cyM0N6ZWN1Wk0";		#// log directory

    if (($service = GD_createService()) == NULL) {
    	echo "Could not acquire the service instance.\n";
    	exit;
    }

    $files = GD_searchFiles($service, "ilm2", $parent);

    if (count($files) > 0) {
    	foreach ($files as $FileItem) {
	    echo "-- ". $FileItem->getName()."\n";
	}
    }
    else {
	echo "file not found...\n";
    }

    $description = "This is test.";
    $mimeType = "text/plain";

    GD_uploadFile("driveLibraryV3.php", $service, "driveLibraryV3.php", $parent, $description, $mimeType);

    $content = GD_downloadFile($service, "driveLibraryV3.php", $parent);

    echo __DIR__."/downloaded_file\n";
    file_put_contents(__DIR__."/downloaded_file", $content);
//    echo $content;

    GD_renameFile($service, $parent, "driveLibraryV3.php", "_driveLibraryV3.php");
 ?>
