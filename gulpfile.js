'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');

gulp.task('sass', function () {
    gulp.src('./restaurants/static/src/sass/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./restaurants/static/restaurants/css'));
});

gulp.task('compress', function() {
    return gulp.src('./restaurants/static/src/js/**/*.js')
        .pipe(uglify({compress : {hoist_vars : true}}))
        .pipe(gulp.dest('./restaurants/static/restaurants/js'));
});

gulp.task('src:watch', function () {
    gulp.watch('./restaurants/src/static/sass/**/*.scss', ['sass']);
    gulp.watch('./restaurants/static/src/js/**/*.js', ['compress']);
});

gulp.task('default', ['sass', 'compress', 'src:watch']);
