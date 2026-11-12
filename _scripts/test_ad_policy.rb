require 'jekyll'
require 'tmpdir'
require 'fileutils'
require 'cgi'

# Render the real layouts/includes so nested post -> default layout order and
# redirect-generator output are covered, rather than checking template strings.
root = File.expand_path('..', __dir__)
config = Jekyll.configuration('source' => root, 'quiet' => true)

Dir.mktmpdir('blog-ad-policy-') do |tmp|
  source = File.join(tmp, 'source')
  destination = File.join(tmp, 'site')
  FileUtils.mkdir_p(source)
  %w[_includes _layouts].each { |dir| FileUtils.cp_r(File.join(root, dir), source) }
  %w[404.html offline.html sitemap.xml search.json].each do |file|
    FileUtils.cp(File.join(root, file), source)
  end
  %w[index about archive privacy contact terms tags].each do |name|
    url = name == 'index' ? '/' : "/#{name}/"
    File.write(File.join(source, "#{name}.html"), <<~PAGE)
      ---
      layout: default
      title: "#{name}"
      permalink: "#{url}"
      ---
      <p>Navigation or information page.</p>
    PAGE
  end
  post_dir = File.join(source, 'okf', '_posts', '2020')
  FileUtils.mkdir_p(post_dir)
  {
    'article' => "status: stable\nredirect_from: /old-article/",
    'draft' => 'status: draft',
    'opt-out' => 'ads: false',
    'noindex' => 'noindex: true',
    'no-sitemap' => 'sitemap: false'
  }.each do |slug, extra|
    File.write(File.join(post_dir, "2020-01-01-#{slug}.md"), <<~POST)
      ---
      title: "#{slug}"
      date: "2020-01-01"
      #{extra}
      ---
      ## Article content

      A complete paragraph for the fixture article.
    POST
  end

  build = lambda do |overrides = {}|
    options = config.merge('source' => source, 'destination' => destination,
                           'cache_dir' => File.join(tmp, 'cache'), 'incremental' => false)
    Jekyll::Site.new(options.merge(overrides)).process
  end
  read = ->(path) { File.read(File.join(destination, path)) }
  post_path = ->(slug) { "2020/01/01/#{slug}/index.html" }
  assert = ->(condition, message) { raise message unless condition }
  google = ->(html) { html.include?('pagead2.googlesyndication.com/pagead/js/adsbygoogle.js') }
  kakao = ->(html) { html.include?('t1.kakaocdn.net/kas/static/ba.min.js') }
  manual = ->(html) { html.include?('data-ad-slot=') }

  build.call
  article = read.call(post_path.call('article'))
  assert.call(google.call(article) && kakao.call(article), 'Published article lost ad loaders')
  assert.call(!manual.call(article), 'Unconfigured manual ad was rendered')
  assert.call(article.include?('name="google-adsense-account"'), 'AdSense verification missing')
  blocked = %w[index.html about/index.html archive/index.html privacy/index.html
               contact/index.html terms/index.html tags/index.html 404.html offline.html]
  blocked += %w[draft opt-out noindex].map { |slug| post_path.call(slug) }
  blocked.each do |path|
    html = read.call(path)
    assert.call(!google.call(html) && !kakao.call(html) && !manual.call(html), "Ads on #{path}")
    assert.call(html.include?('name="google-adsense-account"'), "Verification missing on #{path}")
  end
  %w[404.html offline.html].each do |path|
    assert.call(read.call(path).include?('content="noindex,follow"'), "Missing noindex on #{path}")
  end

  sitemap = read.call('sitemap.xml')
  urls = sitemap.scan(%r{<loc>(.*?)</loc>}).flatten.map { |url| CGI.unescapeHTML(url) }
  assert.call(urls.count("#{config['url']}/") == 1, 'Duplicate sitemap home URL')
  %w[/404.html /offline.html /search.json /redirects.json /old-article/
     /2020/01/01/noindex/ /2020/01/01/no-sitemap/].each do |path|
    assert.call(!urls.include?("#{config['url']}#{path}"), "Sitemap includes #{path}")
  end
  assert.call(urls.include?("#{config['url']}/2020/01/01/article/"), 'Article missing from sitemap')
  assert.call(urls.include?("#{config['url']}/about/"), 'Information page missing from sitemap')
  assert.call(read.call('old-article/index.html').include?('http-equiv="refresh"'), 'Redirect lost')
  puts 'Ad policy: published articles, non-article pages, drafts, opt-out, verification and sitemap PASS'

  build.call('adsense_in_article_slot' => '1234567890')
  article = read.call(post_path.call('article'))
  assert.call(article.include?('data-ad-slot="1234567890"'), 'Issued manual ad ID not rendered')
  blocked.each do |path|
    html = read.call(path)
    assert.call(!google.call(html) && !kakao.call(html) && !manual.call(html), "Manual ads on #{path}")
  end

  build.call('adsense_in_article_slot' => 'auto')
  assert.call(!manual.call(read.call(post_path.call('article'))), 'Invalid auto ad slot rendered')

  build.call('review_preview' => true, 'review_pr' => 1, 'review_sha' => 'test',
             'adsense_in_article_slot' => '1234567890')
  Dir.glob(File.join(destination, '**', '*.html')).each do |path|
    html = File.read(path)
    assert.call(!google.call(html) && !kakao.call(html) && !manual.call(html), "Ads in preview #{path}")
  end
  article = read.call(post_path.call('article'))
  assert.call(article.include?('content="noindex,nofollow"'), 'Preview lost noindex')
  puts 'Ad policy: issued manual IDs, invalid auto IDs and preview isolation PASS'
end
