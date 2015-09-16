'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('sass', function () {
    gulp.src('./restaurants/static/src/sass/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./restaurants/static/restaurants/css'));
});

gulp.task('sass:watch', function () {
    gulp.watch('./restaurants/src/static/sass/**/*.scss', ['sass']);
});

gulp.task('default', ['sass', 'sass:watch']);
