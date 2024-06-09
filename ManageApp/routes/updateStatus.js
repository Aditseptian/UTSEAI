var express = require('express');
const conn = require('../db');
var router = express.Router();

/* GET armada listing. */
router.put('/', function(req, res){
    var sqlQueryPost = `UPDATE Armada SET Status = 'On The Road' WHERE ID_Kendaraan = ${req.body.id}`;
    conn.query(sqlQueryPost, function(err, result) {
      if (err) throw err;
      res.send('Success');
    });
  }
);

module.exports = router;
