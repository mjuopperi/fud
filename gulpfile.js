'use strict';

var gulp        = require('gulp');
var watch       = require('gulp-watch');
var sass        = require('gulp-sass');
var uglify      = require('gulp-uglify');
var source      = require('vinyl-source-stream');
var glob        = require('glob');
var es          = require('event-stream');
var browserify  = require('browserify');
var rename      = require('gulp-rename');
var buffer      = require('vinyl-buffer');
var del         = require('del');
var RevAll      = require('gulp-rev-all');

var path = {
    base: './restaurants',
    dest_base: './restaurants/static/restaurants',
    js_src: './restaurants/static/src/js/**/!(_)*.js',
    js_dest: './restaurants/static/restaurants/js',
    js_extras: './restaurants/static/src/js/**/_*.js',
    sass_src: './restaurants/static/src/sass/**/*.scss',
    sass_dest: './restaurants/static/restaurants/css',
    image_src: './restaurants/static/src/img/**/*.{svg,png,jpg,jpeg,gif}',
    image_dest: './restaurants/static/restaurants/img'
};

gulp.task('clean', function() {
    return del([path.dest_base + '/**']);
});

gulp.task('clean-rev', ['rev'], function() {
    return del([
        path.dest_base + '/**',
        '!' + path.dest_base,  // Have to ignore all folders in the path as the glob
        '!' + path.sass_dest,  // pattern will delete them even if their children are ignored.
        '!' + path.js_dest,    // https://www.npmjs.com/package/del#beware
        '!' + path.image_dest,
        '!' + path.dest_base + '/**/*.rev.*',
        '!' + path.dest_base + '/rev-manifest.json'
    ])
});

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
    gulp.watch(path.js_extras, ['js']);
    gulp.watch(path.image_src, ['images']);
});

gulp.task('images', function () {
    return gulp.src(path.image_src)
        .pipe(gulp.dest(path.image_dest));
});

gulp.task('rev', ['sass', 'js', 'images'], function () {
    var revAll = new RevAll({
        dontRenameFile: [/^\/favicon.ico$/g],
        transformFilename: function (file, hash) {
            return file.revFilenameOriginal + '.rev.' + hash.substr(0, 5) + file.revFilenameExtOriginal;
        }
    });

    return gulp.src(path.dest_base + '/**', {base : path.base})
        .pipe(revAll.revision())
        .pipe(gulp.dest(path.base))
        .pipe(revAll.manifestFile())
        .pipe(gulp.dest(path.dest_base))
});

gulp.task('default', ['sass', 'js', 'images', 'watch']);

gulp.task('build', ['sass', 'js', 'images', 'rev', 'clean-rev']);
