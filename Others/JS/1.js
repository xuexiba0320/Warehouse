bt = (vt(),
        t["_encrypt"] = function() {
            return (t["_encrypt"] = t["asm"]["encrypt"]).apply(null, arguments)
        }
        ,
        t["__initialize"] = function() {
            return (t["__initialize"] = t["asm"]["_initialize"]).apply(null, arguments)
        }
        ,
        t["stackSave"] = function() {
            return (bt = t["stackSave"] = t["asm"]["stackSave"]).apply(null, arguments)
        }
), _t = t["stackRestore"] = function() {
    return (_t = t["stackRestore"] = t["asm"]["stackRestore"]).apply(null, arguments)
}
    , xt = t["stackAlloc"] = function() {
    return (xt = t["stackAlloc"] = t["asm"]["stackAlloc"]).apply(null, arguments)
}
;