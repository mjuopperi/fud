'use strict';

var gulp        = require('gulp');
var watch       = require('gulp-watch');
var sass        = require('gulp-sass');
var uglify      = require('gulp-uglify');
var copy        = require('gulp-copy');
var source      = require('vinyl-source-stream');
var glob        = require('glob');
var es          = require('event-stream');
var browserify  = require('browserify');
var rename      = require('gulp-rename');
var buffer      = require('vinyl-buffer');
var notify      = require('gulp-notify');
var del         = require('del');

var path = {
    js_src: './restaurants/static/src/js/**/!(_)*.js',
    js_dest: './restaurants/static/restaurants/js',
    js_extras: './restaurants/static/src/js/**/_*.js',
    sass_src: './restaurants/static/src/sass/**/*.scss',
    sass_dest: './restaurants/static/restaurants/css',
    image_src: './restaurants/static/src/img/**/*.{svg,png,jpg,jpeg,gif}',
    image_dest: './restaurants/static/restaurants/img'
};

gulp.task('clean', function() {
    return del([
        path.js_dest + '/**/*',
        path.sass_dest + '/**/*',
        path.image_dest + '/**/*'
    ]);
});

gulp.task('sass', function () {
    gulp.src(path.sass_src)
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(path.sass_dest))
        .pipe(notify({ message: "sass done!", onLast: true}));
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
        es.merge(tasks).on('end', done)
          .pipe(notify({ message: "js done!", onLast: true}));
    })
});

gulp.task('watch', function () {
    gulp.watch(path.sass_src, ['sass']);
    gulp.watch(path.js_src, ['js']);
    gulp.watch(path.js_extras, ['js']);
    gulp.watch(path.image_src, ['copy-images']);
});

gulp.task('copy-images', function () {
    return gulp.src(path.image_src)
        .pipe(copy(path.image_dest, { prefix: 5 }))
        .pipe(notify({ message: "copy-images done!", onLast: true}));
});

gulp.task('default', ['sass', 'js', 'copy-images', 'watch']);

gulp.task('build', ['clean', 'sass', 'js', 'copy-images']);
