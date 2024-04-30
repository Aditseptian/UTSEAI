var express = require('express');
const conn = require('../db');
var router = express.Router();

/*GET Masalah by ID */

router.get('/:idKendaraan', function (req, res) {
    var idKendaraan = req.params.idKendaraan;
    var sqlQueryGetMasalah = `SELECT Masalah FROM Masalah WHERE ID_Kendaraan = '${idKendaraan}'`;
    conn.query(sqlQueryGetMasalah, function (err, result) {
        if (err) throw err;
        res.json(result);
    });
});

module.exports = router;