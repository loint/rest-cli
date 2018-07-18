<?php
namespace Rest\Abstraction;

abstract class IO {
    /**
     * Dump data content inside output
     *
     * @return array
     */
    public function toArray()
    {
        $dumpContent = var_export($this, true);
        $dumpContent = explode('__set_state(', $dumpContent)[1];
        $dumpContent = trim($dumpContent);
        $dumpResult = array();
        $evalString = '$dumpResult = (' . $dumpContent . ';';
        eval($evalString);
        return $dumpResult;
    }
}