var express = require('express');
const conn = require('../db');
var router = express.Router();

/* GET armada listing. */
router.delete('/', function(req, res){
    var sqlQueryPost = `DELETE FROM Armada WHERE ID_Kendaraan = ${req.body.id}`;
    conn.query(sqlQueryPost, function(err, result) {
      if (err) throw err;
      res.send('Success');
    });
  }
);

module.exports = router;
