source 'https://rubygems.org'

gem "jekyll", "~> 4.0"
gem "rake"
gem "webrick", "~> 1.7"

# _config.yml 의 plugins: 목록과 반드시 일치해야 한다.
# 누락되면 로컬 `jekyll build` 가 Dependency Error 로 죽는다.
group :jekyll_plugins do
  gem 'jekyll-paginate'
  gem 'jekyll-sitemap'
  gem 'jekyll-seo-tag'
  gem 'jekyll-feed'
end
