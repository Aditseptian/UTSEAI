var express = require('express');
const conn = require('../db');
var router = express.Router();

/* GET armada listing. */
router.get('/', function(req, res, next) {
  var sqlQueryGetAll = `SELECT Armada.ID_Kendaraan, Armada.Jenis, Armada.Status, (IFNULL(NewTable.Tingkat, 'Good')) AS Kondisi
      FROM Armada
      LEFT JOIN (SELECT DISTINCT Masalah.ID_Kendaraan, x.Tingkat
        FROM Masalah
        LEFT JOIN (SELECT Masalah.ID_Kendaraan, t.Tingkat
          FROM Masalah
          JOIN(
            SELECT
              ID_Kendaraan,
              CASE
                WHEN MAX(CASE WHEN Tingkat = 'Parah' THEN 1 ELSE 0 END) = 1 THEN 'Service'
                ELSE 'ok'
              END AS Tingkat
            FROM
              Masalah
            GROUP BY
              ID_Kendaraan) AS t 
            ON Masalah.ID_Kendaraan = t.ID_Kendaraan) AS x 
          ON Masalah.ID_Kendaraan = x.ID_Kendaraan) AS NewTable
      ON Armada.ID_Kendaraan = NewTable.ID_Kendaraan;`;
  conn.query(sqlQueryGetAll, function(err, result, fields) {
    if (err) throw err;
    res.send(result);
  });
});

module.exports = router;
