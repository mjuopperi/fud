'use strict';

var gulp   = require('gulp');
var watch  = require('gulp-watch');
var sass   = require('gulp-sass');
var uglify = require('gulp-uglify');
var copy   = require('gulp-copy');
var source      = require('vinyl-source-stream');
var glob        = require('glob');
var es          = require('event-stream');
var browserify  = require('browserify');
var rename      = require('gulp-rename');
var buffer      = require('vinyl-buffer');

var path = {
    js_src: './restaurants/static/src/js/**/!(_)*.js',
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

gulp.task('js', function(done) {
    glob(path.js_src, function(err, files) {
        if(err) done(err);

        var tasks = files.map(function(entry) {
            return browserify({ entries: [entry] })
              .bundle()
              .pipe(source(entry))
              .pipe(buffer())
              .pipe(rename({dirname : ''}))
              .pipe(uglify())
              .pipe(gulp.dest(path.js_dest));
        });
        es.merge(tasks).on('end', done);
    })
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

gulp.task('build', ['sass', 'js', 'copy-images']);
