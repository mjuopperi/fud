'use strict';

var gulp   = require('gulp');
var watch  = require('gulp-watch');
var sass   = require('gulp-sass');
var react  = require('gulp-react');
var uglify = require('gulp-uglify');

var path = {
    js_src: './restaurants/static/src/js/**/*.js',
    js_dest: './restaurants/static/restaurants/js',
    sass_src: './restaurants/static/src/sass/**/*.scss',
    sass_dest: './restaurants/static/restaurants/css'
};


gulp.task('sass', function () {
    gulp.src(path.sass_src)
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(path.sass_dest));
});

gulp.task('js', function () {
    return gulp.src(path.js_src)
        .pipe(react())
        .pipe(uglify())
        .pipe(gulp.dest(path.js_dest));
});

gulp.task('watch', function () {
    gulp.watch(path.sass_src, ['sass']);
    gulp.watch(path.js_src, ['js']);
});

gulp.task('default', ['sass', 'js', 'watch']);
