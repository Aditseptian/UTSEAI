var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var armadaRouter = require('./routes/armada');
var masalahRouter = require('./routes/masalah');
var tambahArmadaRouter = require('./routes/tambahArmada');
var updateStatusRouter = require('./routes/updateStatus');
var deleteArmadaRouter = require('./routes/deleteArmada');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/armada', armadaRouter);
app.use('/tambah-armada', tambahArmadaRouter);
app.use('/hapus-armada', deleteArmadaRouter);
app.use('/armada', masalahRouter);
app.use('/update-status', updateStatusRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
