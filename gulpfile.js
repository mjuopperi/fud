'use strict';

var gulp   = require('gulp');
var watch  = require('gulp-watch');
var sass   = require('gulp-sass');
var react  = require('gulp-react');
var uglify = require('gulp-uglify');
var copy   = require('gulp-copy');

var path = {
    js_src: './restaurants/static/src/js/**/*.js',
    js_dest: './restaurants/static/restaurants/js',
    sass_src: './restaurants/static/src/sass/**/*.scss',
    sass_dest: './restaurants/static/restaurants/css',
    images_src: './restaurants/static/src/img/**/*.{svg,png,jpg,jpeg,gif}',
    images_dest: './restaurants/static/restaurants/img'
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

gulp.task('copy-images', function () {
    return gulp.src(path.images_src)
        .pipe(copy(path.images_dest, { prefix: 5 }));
});

gulp.task('default', ['sass', 'js', 'watch', 'copy-images']);
