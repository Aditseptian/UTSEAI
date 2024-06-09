var express = require('express');
const conn = require('../db');
var router = express.Router();

/* GET armada listing. */
router.post('/', function(req, res){
    var sqlQueryPost = `INSERT INTO Armada ('Jenis_Kendaraan') VALUES ('${req.body.jenis})`;
    conn.query(sqlQueryPost, function(err, result) {
      if (err) throw err;
      res.send('Success');
    });
  }
);

module.exports = router;



