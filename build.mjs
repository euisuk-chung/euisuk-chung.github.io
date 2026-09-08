/**
 * Asset build for 서쿠 개발노트.
 *
 * Replaces the previous Grunt pipeline (uglify + contrib-less + banner).
 * The `cleancss` option this theme relied on was removed in grunt-contrib-less v2,
 * which silently left css/*.min.css unminified — esbuild handles both now.
 *
 *   node build.mjs           build once
 *   node build.mjs --watch   rebuild on change
 */

import { readFile, writeFile } from 'node:fs/promises'
import { watch } from 'node:fs'
import path from 'node:path'
import less from 'less'
import * as esbuild from 'esbuild'

const pkg = JSON.parse(await readFile('package.json', 'utf8'))

// Retained per Apache-2.0 §4(b)/(c): attribution plus a modification notice.
// See NOTICE for the full third-party list.
const banner =
    `/*!\n` +
    ` * ${pkg.title} v${pkg.version} (${pkg.homepage})\n` +
    ` * Copyright ${new Date().getFullYear()} ${pkg.author}\n` +
    ` * Licensed under Apache 2.0 — see LICENSE and NOTICE.\n` +
    ` *\n` +
    ` * Based on Hux Blog (https://github.com/Huxpro/huxpro.github.io)\n` +
    ` * Copyright Hux <huxpro@gmail.com>, licensed under Apache 2.0,\n` +
    ` * itself derived from Clean Blog (http://startbootstrap.com).\n` +
    ` * Modified by ${pkg.author}.\n` +
    ` */\n`

const LESS_ENTRY = 'less/blog.less'
const CSS_OUT = 'css/blog.css'
const CSS_MIN = 'css/blog.min.css'
const JS_ENTRY = 'js/blog.js'
const JS_MIN = 'js/blog.min.js'

/** Strip any pre-existing banner so rebuilds don't stack them. */
function stripBanner(src) {
    return src.replace(/^\/\*![\s\S]*?\*\/\n*/, '')
}

async function buildCss() {
    const src = await readFile(LESS_ENTRY, 'utf8')
    const { css } = await less.render(src, {
        filename: path.resolve(LESS_ENTRY),
        paths: ['less', 'css'],
    })
    await writeFile(CSS_OUT, banner + css)

    const min = await esbuild.transform(css, { loader: 'css', minify: true })
    await writeFile(CSS_MIN, banner + min.code)
    return [CSS_OUT, CSS_MIN]
}

async function buildJs() {
    const src = stripBanner(await readFile(JS_ENTRY, 'utf8'))
    const min = await esbuild.transform(src, { loader: 'js', minify: true })
    await writeFile(JS_MIN, banner + min.code)
    return [JS_MIN]
}

async function build() {
    const t = Date.now()
    try {
        const out = [...(await buildCss()), ...(await buildJs())]
        console.log(`built ${out.join(', ')} in ${Date.now() - t}ms`)
    } catch (err) {
        console.error(`build failed: ${err.message}`)
        if (!process.argv.includes('--watch')) process.exitCode = 1
    }
}

await build()

if (process.argv.includes('--watch')) {
    let pending
    const rebuild = () => {
        clearTimeout(pending)
        pending = setTimeout(build, 50) // debounce editor multi-writes
    }
    watch('less', { recursive: true }, rebuild)
    watch('js', (_, file) => file === path.basename(JS_ENTRY) && rebuild())
    console.log('watching less/ and js/blog.js …')
}
